from oauth2client import client
from oauth2client import tools
from oauth2client import transport
from oauth2client.file import Storage
from urllib.parse import urlparse
from . import context
import os

CREDS_FILENAME = "{}/access"


def get_credentials(ctx, refresh=None):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.join(os.path.expanduser("~") + "/.agilicus")
    issuer_dir = urlparse(context.get_issuer(ctx)).netloc
    creds_file = CREDS_FILENAME.format(context.get_client_id(ctx))
    store = Storage(home_dir + "/" + issuer_dir + "/" + creds_file)
    crd = store.get()

    # Configure the ouath2 flow to trust the api if a certificate is
    # provided.
    http = None
    cacert = context.get_cacert(ctx)

    # Unfortunately, cacert is a boolean or a string. Some libraries
    # accept a boolean or a string, but httplib2 does not.
    if isinstance(cacert, str):
        http = transport.get_http_object(ca_certs=cacert)
        # Dex is redirecting us. Let it go through.
    else:
        http = transport.get_http_object()
    http.follow_redirects = True
    http.follow_all_redirects = True

    if crd and crd.access_token_expired:
        try:
            crd.refresh(http)
            return crd
        except client.HttpAccessTokenRefreshError:
            crd = None

    if crd and refresh:
        crd.refresh(http)
        return crd

    if not crd:
        client_info = {}
        client_info["client_id"] = context.get_client_id(ctx)
        client_info["auth_uri"] = context.get_issuer(ctx) + "/auth"
        client_info["token_uri"] = context.get_issuer(ctx) + "/token"

        scopes = [
            "openid",
            "profile",
            "email",
            "federated:id",
            "offline_access",
        ]
        client_info["redirect_uri"] = ["http://localhost:4200"]

        constructor_kwargs = {
            "redirect_uri": client_info["redirect_uri"],
            "auth_uri": client_info["auth_uri"],
            "token_uri": client_info["token_uri"],
        }

        flow = client.OAuth2WebServerFlow(
            client_info["client_id"],
            client_secret="",
            scope=scopes,
            pkce=True,
            **constructor_kwargs,
        )

        flow.user_agent = "agilicus-sdk"
        kwargs = {}
        # kwargs = ['--auth_host_port', '5000', '5001', '5002', '5003', '5004',
        #          '--auth_host_name', 'localhost']
        kwargs = [
            "--auth_host_port",
            "4200",
            "4201",
            "4202",
            "4203",
            "4204",
            "--auth_host_name",
            "localhost",
        ]
        flags = tools.argparser.parse_args(kwargs)

        credentials = tools.run_flow(flow, store, flags, http=http)
        return credentials

    return crd
