from http.client import NOT_FOUND

from fastapi import Request, Response
from starlette.datastructures import QueryParams

from ui_fast_utils import has_cookie, redirect_to_page, has_authorization, redirect_to_page_with_cookie


class MyMiddleware:
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute
        self.allowed_paths = ['/login', '/signup', '/static', '/images', '/logout']
        self.paths_for_theme = ['/inference', '/admin']

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        if request.url.path in self.allowed_paths:
            return await call_next(request)
        if not has_cookie(request) and not has_authorization(request):
            return redirect_to_page('/login')
        # if request.url.path in self.paths_for_theme:
        #     request.query_params = QueryParams({'__theme': 'dark'})
        # process the request and get the response
        response = await call_next(request)
        if response.status_code == NOT_FOUND:
            return redirect_to_page_with_cookie('/login', value='', expires=0)
        return response
