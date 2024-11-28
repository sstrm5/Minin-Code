from core.api.schemas import ApiResponse, ListResponse
from django.http import HttpRequest
from core.api.v1.events.schemas import AddEventSchema, EventListOutSchema, SignSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.customers.services.senders import MailSenderService
from core.apps.events.services import ORMEventsService
from ninja import Router, Header, File
from ninja.files import UploadedFile

from core.apps.events.use_cases import AddEventUseCase, SignUseCase

router = Router(tags=['Events'])


@router.get('/get_events', response=ApiResponse)
def get_list_events(
    request: HttpRequest,
):
    service = ORMEventsService()
    events_list = service.get_events_list()
    items = [EventListOutSchema.from_entity(item) for item in events_list]
    return ApiResponse(data=ListResponse(items=items))


@router.get('/get_event/{event_id}', response=ApiResponse)
def get_event(
    request: HttpRequest,
    event_id: int,
):
    service = ORMEventsService()
    event = service.get_event(event_id=event_id)
    return ApiResponse(data=event)


@router.post('/add_event', response=ApiResponse)
def add_event(
    request: HttpRequest,
    schema: AddEventSchema,
    token: str = Header(alias='Auth-Token'),
    file: UploadedFile = File(alias='image'),
):
    use_case = AddEventUseCase(ORMCustomerService(), ORMEventsService())
    event = use_case.execute(token=token, schema=schema, file=file)
    return ApiResponse(data=EventListOutSchema.from_entity(event))


@router.post('/sign_event', response=ApiResponse)
def sign_event(
    request: HttpRequest,
    schema: SignSchema,
    token: str = Header(alias='Auth-Token'),
):
    use_case = SignUseCase(
        customer_service=ORMCustomerService(),
        event_service=ORMEventsService(),
        sender_service=MailSenderService(),
    )
    event = use_case.execute(token=token, event_id=schema.event_id)
    return ApiResponse(data=event)
