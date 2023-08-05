from . import access
from . import context


def query_top(
    ctx,
    org_id=None,
    dt_from=None,
    dt_to=None,
    app_id=None,
    sub_org_id=None,
    interval=None,
    limit=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    apiclient = context.get_apiclient(ctx, token)

    params = {}
    params["dt_from"] = dt_from
    params["dt_to"] = dt_to
    params["sub_org_id"] = sub_org_id

    if app_id:
        params["app_id"] = app_id
    if interval:
        params["interval"] = int(interval)
    if limit:
        params["limit"] = int(limit)

    resp = apiclient.metrics_api.metrics_metrics_query_top(org_id, **params)

    return resp.top_n_users


def query_active(
    ctx,
    org_id=None,
    dt_from=None,
    dt_to=None,
    app_id=None,
    sub_org_id=None,
    interval=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    apiclient = context.get_apiclient(ctx, token)

    params = {}
    params["dt_from"] = dt_from
    params["dt_to"] = dt_to
    params["sub_org_id"] = sub_org_id

    if app_id:
        params["app_id"] = app_id
    if interval:
        params["interval"] = int(interval)

    resp = apiclient.metrics_api.metrics_metrics_query_active(org_id, **params)

    return resp.active_users
