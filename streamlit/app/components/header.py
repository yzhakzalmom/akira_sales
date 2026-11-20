import json

from utils.helpers import get_asset_file_path, image_to_base64
from utils.constants import *


def _logo_src(file_name: str) -> str:
    logo_path = get_asset_file_path(ASSET_TYPE_ICONS, file_name)
    return "data:image/png;base64," + image_to_base64(logo_path)


# Light mode shows the black logo. Dark mode swaps in white_logo.png
# after the page background is known, so a stale theme value cannot
# leave the white mark on a light screen.
def render_header(container, header_text, logo_width: int = 100) -> None:
    black_logo = json.dumps(_logo_src(BLACK_LOGO_FILE_NAME))
    white_logo = json.dumps(_logo_src(WHITE_LOGO_FILE_NAME))
    container.html(
        f"""
        <div style="text-align: center;">
            <img id="akira-header-logo" src={black_logo} width="{logo_width}" alt="Akira">
            <h1 style="text-align: center; margin: 0.35rem 0 0.75rem;">{header_text}</h1>
        </div>
        <script>
        (() => {{
            const blackSrc = {black_logo};
            const whiteSrc = {white_logo};
            const img = document.getElementById("akira-header-logo");
            const apply = () => {{
                const app = document.querySelector(".stApp");
                if (!app || !img) return;
                const match = getComputedStyle(app).backgroundColor.match(/[\\d.]+/g);
                if (!match) return;
                const [red, green, blue] = match.slice(0, 3).map(Number);
                const dark = (0.2126 * red) + (0.7152 * green) + (0.0722 * blue) < 140;
                img.src = dark ? whiteSrc : blackSrc;
                const root = document.documentElement;
                root.style.setProperty("--akira-login-bg", dark ? "#ffffff" : "#111111");
                root.style.setProperty("--akira-login-fg", dark ? "#111111" : "#ffffff");
                root.style.setProperty("--akira-login-hover", dark ? "#e6e6e6" : "#333333");
            }};
            apply();
            requestAnimationFrame(apply);
            const app = document.querySelector(".stApp");
            if (app) {{
                new MutationObserver(apply).observe(app, {{
                    attributes: true,
                    attributeFilter: ["class", "style"],
                }});
            }}
        }})();
        </script>
        """,
        unsafe_allow_javascript=True,
    )
