"""
Application entry point.

Every URL runs this file before the selected page. The login screen is
rendered here, and navigation is registered only after Microsoft sign-in.
"""

import os

import streamlit as st
from authlib.integrations.base_client.async_openid import AsyncOpenIDMixin
from authlib.integrations.base_client.sync_openid import OpenIDMixin

from components import header
from utils.constants import *
from utils.helpers import load_env_file
from views.execucao import render as render_execucao
from views.opcoes import render as render_opcoes
from views.uploads import render as render_uploads

load_env_file()


def allowed_tenant_ids() -> set[str]:
    raw = os.getenv("ENTRA_ALLOWED_TENANT_IDS", "")
    return {item.strip() for item in raw.split(",") if item.strip()}


def _allowed_issuer_claims(metadata_issuer: object) -> dict | None:
    """Microsoft's organizations metadata publishes iss as the literal {tenantid}.

    Authlib compares that placeholder with the token issuer and rejects a real
    tenant URL. Accept the v2 issuer of each tenant in ENTRA_ALLOWED_TENANT_IDS.
    """
    if not isinstance(metadata_issuer, str) or "{tenantid}" not in metadata_issuer:
        return None
    issuers = [
        f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        for tenant_id in allowed_tenant_ids()
    ]
    if not issuers:
        return None
    return {"iss": {"values": issuers}}


def _accept_allowed_tenant_issuers(parse_id_token):
    def parse_id_token_with_allowed_issuers(
        self, token, nonce, claims_options=None, claims_cls=None, leeway=120
    ):
        if claims_options is None:
            claims_options = _allowed_issuer_claims(
                self.load_server_metadata().get("issuer")
            )
        return parse_id_token(
            self,
            token,
            nonce,
            claims_options=claims_options,
            claims_cls=claims_cls,
            leeway=leeway,
        )

    return parse_id_token_with_allowed_issuers


def _accept_allowed_tenant_issuers_async(parse_id_token):
    async def parse_id_token_with_allowed_issuers(
        self, token, nonce, claims_options=None, claims_cls=None, leeway=120
    ):
        if claims_options is None:
            metadata = await self.load_server_metadata()
            claims_options = _allowed_issuer_claims(metadata.get("issuer"))
        return await parse_id_token(
            self,
            token,
            nonce,
            claims_options=claims_options,
            claims_cls=claims_cls,
            leeway=leeway,
        )

    return parse_id_token_with_allowed_issuers


def _patch_parse_id_token(mixin, wrapper):
    original = getattr(
        mixin, "_akira_original_parse_id_token", mixin.parse_id_token
    )
    mixin._akira_original_parse_id_token = original
    mixin.parse_id_token = wrapper(original)


# The OAuth callback runs in the Starlette server and uses the async client.
# Patching only the sync mixin leaves that callback validating {tenantid}.
_patch_parse_id_token(OpenIDMixin, _accept_allowed_tenant_issuers)
_patch_parse_id_token(AsyncOpenIDMixin, _accept_allowed_tenant_issuers_async)

st.set_page_config(
    page_title=LOGIN_PAGE_TITLE,
    page_icon=MAIN_ICON,
    layout=MAIN_PAGE_LAYOUT,
)


def user_claim(key: str) -> str | None:
    try:
        value = st.user[key]
    except Exception:
        value = None
    if value:
        return str(value)
    return None


allowed = allowed_tenant_ids()
if not allowed:
    st.error(MSG_AUTH_TENANTS_MISSING)
    st.stop()

if st.user.is_logged_in and user_claim("tid") not in allowed:
    st.logout()
    st.stop()

if not st.user.is_logged_in:
    st.markdown(
        """
        <style>
        [data-testid="stMain"] [data-testid="stElementContainer"]:has(.stButton) {
            width: 100%;
        }
        [data-testid="stMain"] div.stButton {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 0.25rem;
        }
        [data-testid="stMain"] div.stButton > button,
        [data-testid="stMain"] div.stButton > button:hover,
        [data-testid="stMain"] div.stButton > button:focus,
        [data-testid="stMain"] div.stButton > button:active {
            width: fit-content;
            padding-left: 1.6rem;
            padding-right: 1.6rem;
            background-color: var(--akira-login-bg, #111111);
            color: var(--akira-login-fg, #ffffff);
            border: 1px solid var(--akira-login-bg, #111111);
        }
        [data-testid="stMain"] div.stButton > button:hover {
            background-color: var(--akira-login-hover, #333333);
            border-color: var(--akira-login-hover, #333333);
            color: var(--akira-login-fg, #ffffff);
        }
        [data-testid="stMain"] div.stButton > button:focus {
            box-shadow: 0 0 0 0.2rem var(--akira-login-bg, #111111);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 4vh;'></div>", unsafe_allow_html=True)
    header.render_header(st, LOGIN_HEADER, logo_width=120)
    st.markdown(
        (
            "<p style='text-align: center; font-size: 0.9rem; "
            "line-height: 1.45; opacity: 0.8; max-width: 34rem; "
            "margin: 0 auto 0.75rem;'>"
            f"{LOGIN_HELP}</p>"
        ),
        unsafe_allow_html=True,
    )
    if st.button(LOGIN_BUTTON):
        st.login()
    st.stop()

with st.sidebar:
    display_name = user_claim("name") or user_claim("email")
    if display_name:
        st.caption(display_name)
    if st.button(LOGOUT_BUTTON):
        st.logout()

navigation = st.navigation(
    [
        st.Page(
            render_uploads,
            title=MAIN_PAGE_TITLE,
            default=True,
            url_path="uploads",
        ),
        st.Page(
            render_opcoes,
            title=CONFIG_PAGE_TITLE,
            url_path="opcoes",
        ),
        st.Page(
            render_execucao,
            title=JOBS_PAGE_TITLE,
            url_path="execucao",
        ),
    ]
)
navigation.run()
