from core.api.schemas import ApiResponse, ListResponse
from django.http import HttpRequest
from core.api.v1.events.schemas import AddEventSchema, EventListOutSchema, SignSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.customers.services.senders import MailSenderService
from core.apps.events.services import ORMEventsAdminService, ORMEventsService
from ninja import Router, Header

from core.apps.events.use_cases import GetEventsAdminUseCase, PublishEventAdminUseCase, UnpublishEventAdminUseCase

router = Router(tags=['Events for admins'])


@router.get('/get_events', response=ApiResponse)
def get_list_events(
    request: HttpRequest,
):
    token = request.META['HTTP_AUTH_TOKEN']
    use_case = GetEventsAdminUseCase(
        event_service=ORMEventsAdminService(),
        customer_service=ORMCustomerService(),
    )
    events_list = use_case.execute(token=token)
    items = [EventListOutSchema.from_entity(item) for item in events_list]
    return ApiResponse(data=ListResponse(items=items))


@router.post('/publish_event/{event_id}', response=ApiResponse)
def publish_event(
    request: HttpRequest,
    event_id: int,
    token: str = Header(alias='Auth-Token'),
):
    use_case = PublishEventAdminUseCase(
        event_admin_service=ORMEventsAdminService(),
        event_service=ORMEventsService(),
        customer_service=ORMCustomerService(),
    )
    event = use_case.execute(token=token, event_id=event_id)
    return ApiResponse(data=event)


@router.post('/unpublish_event/{event_id}', response=ApiResponse)
def unpublish_event(
    request: HttpRequest,
    event_id: int,
    token: str = Header(alias='Auth-Token'),
):
    use_case = UnpublishEventAdminUseCase(
        event_admin_service=ORMEventsAdminService(),
        event_service=ORMEventsService(),
        customer_service=ORMCustomerService(),
    )
    event = use_case.execute(
        token=token, event_id=event_id)
    return ApiResponse(data=event)
