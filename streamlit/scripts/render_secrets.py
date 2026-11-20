"""Write Streamlit auth secrets from the process environment.

Streamlit reads `.streamlit/secrets.toml` before the app script runs, so this
file has to exist before `streamlit run`. The environment is the source of
truth. AUTH_COOKIE_SECRET is never generated here: a new value on each start
would sign out every user.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"
METADATA_URL = (
    "https://login.microsoftonline.com/organizations/v2.0/"
    ".well-known/openid-configuration"
)
REQUIRED = (
    "ENTRA_CLIENT_ID",
    "ENTRA_CLIENT_SECRET",
    "ENTRA_ALLOWED_TENANT_IDS",
    "AUTH_REDIRECT_URI",
    "AUTH_COOKIE_SECRET",
)


def main() -> None:
    import os

    missing = [name for name in REQUIRED if not os.getenv(name, "").strip()]
    if missing:
        print(
            "Variáveis de login ausentes: " + ", ".join(missing),
            file=sys.stderr,
        )
        if "AUTH_COOKIE_SECRET" in missing:
            import secrets

            print(
                "Gere AUTH_COOKIE_SECRET uma vez e cole no .env:\n"
                f"AUTH_COOKIE_SECRET={secrets.token_urlsafe(32)}",
                file=sys.stderr,
            )
        sys.exit(1)

    tenant_ids = [
        item.strip()
        for item in os.environ["ENTRA_ALLOWED_TENANT_IDS"].split(",")
        if item.strip()
    ]
    if len(tenant_ids) < 2:
        print(
            "ENTRA_ALLOWED_TENANT_IDS precisa dos dois tenant IDs, separados por vírgula.",
            file=sys.stderr,
        )
        sys.exit(1)

    redirect_uri = os.environ["AUTH_REDIRECT_URI"].strip()
    if not redirect_uri.startswith(("http://", "https://")):
        print(
            "AUTH_REDIRECT_URI precisa ser uma URL absoluta terminando em /oauth2callback.",
            file=sys.stderr,
        )
        sys.exit(1)

    contents = "\n".join(
        [
            "[auth]",
            f"redirect_uri = {json.dumps(redirect_uri)}",
            f"cookie_secret = {json.dumps(os.environ['AUTH_COOKIE_SECRET'])}",
            f"client_id = {json.dumps(os.environ['ENTRA_CLIENT_ID'].strip())}",
            f"client_secret = {json.dumps(os.environ['ENTRA_CLIENT_SECRET'])}",
            f"server_metadata_url = {json.dumps(METADATA_URL)}",
            'client_kwargs = { "prompt" = "select_account" }',
            "",
        ]
    )
    SECRETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SECRETS_PATH.write_text(contents, encoding="utf-8")


if __name__ == "__main__":
    main()
