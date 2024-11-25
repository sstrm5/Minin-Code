from functools import lru_cache
from core.apps.customers.services.auth import AuthService, BaseAuthService
from core.apps.customers.services.codes import BaseCodeService, DjangoCacheCodeService
from core.apps.customers.services.customers import BaseCustomerService, ORMCustomerService
from core.apps.customers.services.senders import BaseSenderService, MailSenderService
from core.apps.questions.services.attempts import BaseAttemptService, ORMAttemptService
from core.apps.questions.services.questions import BaseQuestionService, BaseTestService, ORMQuestionService, ORMTestService
import punq


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container():
    container = punq.Container()
    container.register(BaseTestService, ORMTestService)
    container.register(BaseQuestionService, ORMQuestionService)
    container.register(BaseAttemptService, ORMAttemptService)
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(BaseSenderService, MailSenderService)
    container.register(BaseAuthService, AuthService)
    return container
