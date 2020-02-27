from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles


def homepage(request):
    return PlainTextResponse(f'Hello, world!\nCONFIGA: {CONFIGA}\nCONFIGB: {CONFIGB}')

def user_me(request):
    username = "John Doe"
    return PlainTextResponse('Hello, %s!' % username)

def user(request):
    username = request.path_params['username']
    return PlainTextResponse('Hello, %s!' % username)

def startup():
    print('Ready to go')


routes = [
    Route('/', homepage),
    Route('/user/me', user_me),
    Route('/user/{username}', user),
    Mount('/static', StaticFiles(directory="static")),
]

config = Config(".env")
CONFIGA = config('CONFIGA', cast=bool, default=False)
CONFIGB = config('CONFIGB', cast=bool, default=False)
app = Starlette(debug=True, routes=routes, on_startup=[startup])
