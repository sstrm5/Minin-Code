from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterable

from core.apps.customers.models import Customer as CustomerModel
from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from core.apps.questions.models.attempts import Attempt as AttemptModel
from core.apps.questions.models.questions import Test as TestModel


class BaseAttemptService(ABC):
    @abstractmethod
    def create_attempt(
        self,
        user_id: int,
        test_id: int,
        start_time: datetime,
        end_time: datetime,
        user_answers: dict[int, Iterable],
        total_score: int,
    ) -> None:
        ...

    @abstractmethod
    def get_attempt_list(self, test_id: int) -> AttemptEntity:
        ...


class ORMAttemptService(BaseAttemptService):
    def create_attempt(
        self,
        user_access_token: str,
        test_id: int,
    ) -> AttemptEntity:
        customer = CustomerModel.objects.get(access_token=user_access_token)
        test = TestModel.objects.get(id=test_id)
        # номер последней попытки = кол-во попыток пользователя пройти тест
        attempt_number = AttemptModel.objects.filter(
            user=customer, test=test).count()
        # проверка наличия попытки для этого пользователя и теста
        if attempt_number:
            attempt_number += 1
        else:
            attempt_number = 1
        current_time = datetime.now()
        end_time = current_time + timedelta(seconds=(test.work_time * 60))
        attempt = AttemptModel.objects.create(
            user=customer,
            test=test,
            end_time=end_time,
            user_answers={},
            total_score=0,
            attempt_number=attempt_number,
            created_at=current_time,
            updated_at=current_time,
        )

        return attempt.to_entity()

    def update_attempt(self, user_access_token: str, test_id: int, user_answers: dict[str, list[str]]):
        customer = CustomerModel.objects.get(access_token=user_access_token)
        test = TestModel.objects.get(id=test_id)
        # номер последней попытки = кол-во попыток пользователя пройти тест
        attempt_number = AttemptModel.objects.filter(
            user=customer, test=test).count()
        attempt = AttemptModel.objects.get(
            user=customer,
            test=test,
            attempt_number=attempt_number)
        if not user_answers:
            return attempt.to_entity()
        attempt.user_answers = user_answers
        attempt.save()

        return attempt.to_entity()

    def get_attempt_list(self, test_id: int) -> list[AttemptEntity]:
        attempts = AttemptModel.objects.filter(test_id=test_id)
        return [attempt.to_entity() for attempt in attempts]
