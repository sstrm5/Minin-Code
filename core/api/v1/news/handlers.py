from django.http import HttpRequest
from ninja import Router, Header, File
from ninja.files import UploadedFile
from core.api.schemas import ApiResponse
from core.api.v1.news.schemas import CreateNewsSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.customers.services.senders import MailSenderService
from core.apps.news.services import ORMNewsService
from core.apps.news.use_cases import AddNewsUseCase


router = Router(tags=['News'])


@router.get('/get_published_news', response=ApiResponse, operation_id='get_news')
def get_all_published_news(request: HttpRequest) -> ApiResponse:
    service = ORMNewsService()
    items = service.get_all_published_news()

    return ApiResponse(data=items)


@router.post('/add_news', response=ApiResponse)
def add_news(
    request,
    schema: CreateNewsSchema,
    token: str = Header(alias='Auth-Token'),
    file: UploadedFile = File(alias='image'),
) -> ApiResponse:
    use_case = AddNewsUseCase(
        ORMCustomerService(),
        ORMNewsService(),
    )
    news = use_case.execute(
        token=token,
        title=schema.title,
        text=schema.text,
        additional_text=schema.additional_text,
        file=file,
    )

    return ApiResponse(data=news)
