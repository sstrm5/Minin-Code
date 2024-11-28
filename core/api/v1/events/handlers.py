from core.api.schemas import ApiResponse, ListResponse
from django.http import HttpRequest
from core.api.v1.events.schemas import AddEventSchema, EventListOutSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.events.services import ORMEventsService
from ninja import Router, Header

from core.apps.events.use_cases import AddEventUseCase

router = Router(tags=['Events'])


@router.get('/get_events', response=ApiResponse)
def get_list_events(
    request: HttpRequest,
):
    service = ORMEventsService()
    events_list = service.get_events_list()
    items = [EventListOutSchema.from_entity(item) for item in events_list]
    return ApiResponse(data=ListResponse(items=items))


@router.post('/add_event', response=ApiResponse)
def add_event(
    request: HttpRequest,
    schema: AddEventSchema,
    token: str = Header(alias='Auth-Token'),
):
    use_case = AddEventUseCase(ORMCustomerService(), ORMEventsService())
    event = use_case.execute(token=token, schema=schema)
    return ApiResponse(data=EventListOutSchema.from_entity(event))
