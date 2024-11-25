from django.db import models
from django import forms

from core.apps.common.models import TimedBaseModel
from core.apps.questions.entities.questions import Question as QuestionEntity, Test as TestEntity
from .subjects import Subject


class Test(TimedBaseModel):
    title = models.CharField(
        verbose_name='Название теста',
        max_length=255,
        blank=True,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name='Тема',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='tests',
    )
    work_time = models.IntegerField(
        verbose_name='Время выполнения (мин)',
        blank=True,
    )
    question_count = models.IntegerField(
        verbose_name='Количество вопросов в тесте',
    )
    description = models.TextField(
        verbose_name='Описание теста',
        blank=True,
    )
    picture = models.ImageField(
        verbose_name='Изображение теста',
        blank=True,
        null=True,
        upload_to='questions/tests_pictures',
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли тест в списке',
        default=True,
    )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def to_entity(self) -> TestEntity:
        return TestEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            subject=self.subject.__str__(),
            work_time=self.work_time,
            question_count=self.question_count,
            picture=self.picture.url if self.picture else '',
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return self.title


class Question(TimedBaseModel):
    # class Subjects(models.TextChoices):
    #     RUSSIAN_ART = 'RU', 'Russian'

    test = models.ForeignKey(
        Test,
        verbose_name='Тест',
        on_delete=models.CASCADE,
        blank=True
    )
    title = models.CharField(
        verbose_name='Заголовок вопроса',
        max_length=255,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name='Тема',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # Filter choices to only visible subjects.  # Add this line if you want to restrict choices to visible subjects.  # This is not a recommended practice. It's better to use a separate model for subjects.
        limit_choices_to={'is_visible': True},
    )
    description = models.TextField(
        verbose_name='Описание вопроса',
        blank=True,
    )
    weight = models.PositiveIntegerField(
        verbose_name='Вес вопроса',
        default=1,
    )
    picture = models.ImageField(
        verbose_name='Изображение вопроса',
        blank=True,
        null=True,
        upload_to='questions/questions_pictures',
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли вопрос в списке',
        default=True,
    )

    @property
    def answers_dict(self) -> dict:
        return {answer.text: answer.is_correct for answer in self.answers.all()}

    @property
    def answers_list(self) -> list:
        answers = []
        for answer_index, answer in enumerate(self.answers.all(), 1):
            answers.append({
                'id': str(answer_index),
                'text': answer.text,
            })
        return answers

    def to_entity(self) -> QuestionEntity:
        return QuestionEntity(
            id=self.id,
            title=self.title,
            answers=self.answers_list,
            answers_dict=self.answers_dict,
            test_id=self.test.pk,
            description=self.description,
            subject=self.subject.__str__(),
            weight=self.weight,
            picture=self.picture.url if self.picture else '',
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(TimedBaseModel):

    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    text = models.CharField(
        verbose_name='Ответ',
        max_length=255,
    )
    is_correct = models.BooleanField(
        verbose_name='Правильный ли ответ',
        default=False,
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
