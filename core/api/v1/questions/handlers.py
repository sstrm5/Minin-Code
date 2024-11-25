from django.http import HttpRequest
from core.api.filters import PaginationIn, PaginationOut
from core.api.v1.questions.filters import (
    TestFilters,
)
from core.apps.questions.containers import get_container
from core.apps.questions.exceptions.questions import CreateException
from core.apps.questions.services.attempts import BaseAttemptService
from core.apps.questions.services.questions import (
    BaseTestService,
    BaseQuestionService,
)
from ninja import Query, Router
from ninja.errors import HttpError
from core.api.schemas import ApiResponse, ListPaginatedResponse, ListResponse
from core.api.v1.questions.schemas import (
    AnswersOut,
    AttemptSchemaIn,
    AttemptSchemaOut,
    AttemptUpdateSchema,
    TestSchemaIn,
    TestSchemaOut,
    QuestionSchemaOut,
)


router = Router(tags=['Tests'])


@router.get('', response=ApiResponse)
def get_test_list_handler(
    request: HttpRequest,
    filters: Query[TestFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseTestService)
    test_list = service.get_test_list(
        filters=filters, pagination=pagination_in)
    test_count = service.get_test_count(filters=filters)
    items = [TestSchemaOut.from_entity(obj) for obj in test_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=test_count,
    )

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('/{test_id}', response=ApiResponse)
def get_test_handler(request, test_id: int) -> ApiResponse:
    container = get_container()
    question_service = container.resolve(BaseQuestionService)
    test_service = container.resolve(BaseTestService)

    question_list = question_service.get_question_list(test_id=test_id)
    duration = test_service.get_test_duration(test_id=test_id)
    items = [QuestionSchemaOut.from_entity(obj) for obj in question_list]

    return ApiResponse(data=ListResponse(items=items), meta={'duration': duration})


@router.post('/create/new_test', response=ApiResponse)
def create_test_handler(
    request,
    schema: TestSchemaIn,
) -> ApiResponse:
    try:
        container = get_container()
        service = container.resolve(BaseTestService)
        test = service.create_test(data=schema)

        return ApiResponse(data=TestSchemaOut.from_entity(test))
    except CreateException as exception:
        raise HttpError(status_code=400, message=exception.message)


@router.post('/check/test', response=ApiResponse)
def check_test_handler(
    request,
    schema: AttemptSchemaIn,
) -> ApiResponse:
    try:
        container = get_container()
        test_service = container.resolve(BaseTestService)
        question_service = container.resolve(BaseQuestionService)

        questions = question_service.get_question_list(test_id=schema.test_id)
        user_answers, correct_answers, total_score = test_service.check_test(
            user_access_token=request.META['HTTP_AUTHORIZATION'],
            test_id=schema.test_id,
            questions=questions,
        )

        return ApiResponse(data=AnswersOut(
            test_id=schema.test_id,
            user_answers=user_answers,
            correct_answers=correct_answers,
            total_score=total_score,
        ))
    except Exception as exception:
        raise HttpError(status_code=400, message=exception.message)


@router.post('/create/new_attempt', response=ApiResponse)
def create_attempt_handler(
    request,
    schema: AttemptSchemaIn,
) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAttemptService)
    attempt = service.create_attempt(
        user_access_token=request.META['HTTP_AUTHORIZATION'],
        test_id=schema.test_id,
    )

    return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.post('/update/attempt', response=ApiResponse)
def update_attempt_handler(
    request,
    schema: AttemptUpdateSchema,
) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAttemptService)

    attempt = service.update_attempt(
        user_access_token=request.META['HTTP_AUTHORIZATION'],
        test_id=schema.test_id,
        user_answers=schema.user_answers,
    )

    return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.get('/{test_id}/attempts', response=ApiResponse)
def get_attempt_handler(request, test_id: int) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAttemptService)
    attempt_list = service.get_attempt_list(test_id=test_id)
    items = [AttemptSchemaOut.from_entity(obj) for obj in attempt_list]

    return ApiResponse(data=ListResponse(items=items))


@router.get('/hello_world/123')
def hello(request):
    return {'message': f'{request.META['HTTP_AUTHORIZATION']}'}
