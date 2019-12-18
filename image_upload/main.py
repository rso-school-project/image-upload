from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette_prometheus import metrics, PrometheusMiddleware
from starlette.requests import Request


from . import VERSION, PREFIX
from .routers import upload
from .utils import check_liveness, check_readiness

from image_upload.logger import logger

app = FastAPI(
    title='image-upload',
    description='Microservice for handling image upload.',
    version=VERSION,
    openapi_url='/openapi.json',
    docs_url=None,
    redoc_url=None
)


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f'https://34.65.148.232/{app.title + app.openapi_url}',
        # openapi_url=f'/{app.title + app.openapi_url}',
        title=app.title + ' - Swagger UI'
    )


@app.middleware('http')
async def logger_middleware(request: Request, call_next):
    path = PrometheusMiddleware.get_path_template(request)
    logger.info(f'{path} ENTRY', extra={'unique_log_id': request.headers.get('unique_log_id', 'Not provided')})
    response = await call_next(request)
    logger.info(f'{path} EXIT', extra={'unique_log_id': request.headers.get('unique_log_id', 'Not provided')})
    return response


app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics/', metrics)

app.include_router(
    upload.router, prefix=PREFIX, responses={404: {'description': 'Not found'}},
)

app.add_route('/health/live', check_liveness)
app.add_route('/health/ready', check_readiness)
