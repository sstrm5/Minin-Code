from django.http import HttpRequest
from ninja import Router, Header
from core.api.schemas import ApiResponse
from core.api.v1.news.schemas import CreateNewsSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.news.services import ORMNewsAdminService, ORMNewsService
from core.apps.news.use_cases import AddNewsUseCase, GetNewsAdminUseCase, PublishNewsAdminUseCase, UnpublishNewsAdminUseCase


router = Router(tags=['News for admin'])


@router.get('/get_news', response=ApiResponse, operation_id='get_news')
def get_news(
    request: HttpRequest,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse:
    use_case = GetNewsAdminUseCase(
        news_admin_service=ORMNewsAdminService(),
        customer_service=ORMCustomerService(),
    )
    items = use_case.execute(
        token=token
    )

    return ApiResponse(data=items)


@router.post('/publish_news/{news_id}', response=ApiResponse, operation_id='publish_news')
def publish_news(
    request: HttpRequest,
    news_id: int,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse:
    use_case = PublishNewsAdminUseCase(
        news_admin_service=ORMNewsAdminService(),
        customer_service=ORMCustomerService(),
    )
    news = use_case.execute(
        token=token,
        news_id=news_id,
    )
    return ApiResponse(data=news)


@router.post('/unpublish_news/{news_id}', response=ApiResponse, operation_id='unpublish_news')
def unpublish_news(
    request: HttpRequest,
    news_id: int,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse:
    use_case = UnpublishNewsAdminUseCase(
        news_admin_service=ORMNewsAdminService(),
        customer_service=ORMCustomerService(),
    )
    news = use_case.execute(
        token=token,
        news_id=news_id,
    )
    return ApiResponse(data=news)
