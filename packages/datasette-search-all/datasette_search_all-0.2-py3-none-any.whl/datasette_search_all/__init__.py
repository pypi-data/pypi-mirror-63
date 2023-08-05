from datasette import hookimpl
from .app import asgi_search_page
from .utils import get_searchable_tables


@hookimpl
def extra_template_vars(template, datasette):
    if template != "index.html":
        return
    # Add list of searchable tables
    async def inner():
        searchable_tables = await get_searchable_tables(datasette)
        return {"searchable_tables": searchable_tables}

    return inner


@hookimpl
def asgi_wrapper(datasette):
    def wrap_with_app(app):
        async def wrapped_app(scope, receive, send):
            path = scope["path"]
            if path == "/-/search":
                await asgi_search_page(datasette)(scope, receive, send)
            else:
                await app(scope, receive, send)

        return wrapped_app

    return wrap_with_app
