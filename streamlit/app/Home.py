"""
Application entry point.

Every URL runs this file before the selected page. The login screen is
rendered here, and navigation is registered only after Microsoft sign-in.
"""

import os

import streamlit as st
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


def _accept_allowed_tenant_issuers(parse_id_token):
    """Microsoft's organizations metadata publishes iss as the literal {tenantid}.

    Authlib compares that placeholder with the token issuer and rejects a real
    tenant URL. Accept the v2 issuer of each tenant in ENTRA_ALLOWED_TENANT_IDS.
    """

    def parse_id_token_with_allowed_issuers(
        self, token, nonce, claims_options=None, claims_cls=None, leeway=120
    ):
        if claims_options is None:
            metadata_issuer = self.load_server_metadata().get("issuer")
            if isinstance(metadata_issuer, str) and "{tenantid}" in metadata_issuer:
                issuers = [
                    f"https://login.microsoftonline.com/{tenant_id}/v2.0"
                    for tenant_id in allowed_tenant_ids()
                ]
                if issuers:
                    claims_options = {"iss": {"values": issuers}}
        return parse_id_token(
            self,
            token,
            nonce,
            claims_options=claims_options,
            claims_cls=claims_cls,
            leeway=leeway,
        )

    return parse_id_token_with_allowed_issuers


_original_parse_id_token = getattr(
    OpenIDMixin, "_akira_original_parse_id_token", OpenIDMixin.parse_id_token
)
OpenIDMixin._akira_original_parse_id_token = _original_parse_id_token
OpenIDMixin.parse_id_token = _accept_allowed_tenant_issuers(_original_parse_id_token)

st.set_page_config(
    page_title=MAIN_PAGE_TITLE,
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
    login_container = st.container()
    header.render_header(login_container, LOGIN_HEADER)
    _, login_col, __ = login_container.columns(MAIN_PAGE_COLUMN_LAYOUT)
    with login_col:
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
