from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CreateException(ServiceException):
    @property
    def message(self):
        return 'Create test error occured'


@dataclass(eq=False)
class SubjectException(CreateException):
    @property
    def message(self):
        return 'Subject error occured'
    

@dataclass(eq=False)
class QuestionException(CreateException):
    @property
    def message(self):
        return 'Question error occured'
