# from django.contrib import admin
# import nested_admin

# from core.apps.questions.models.attempts import Attempt

# from .models.questions import Test, Question, Answer
# from .models.subjects import Subject

# # Register your models here.


# @admin.register(Question)
# class ProductAdmin2(admin.ModelAdmin):
#     list_display = ('id', 'title', 'test', 'test_id', 'created_at',
#                     'updated_at', 'description', 'subject', 'is_visible')


# @admin.register(Answer)
# class ProductAdmin3(admin.ModelAdmin):
#     list_display = ('id', 'question', 'text', 'created_at',
#                     'updated_at', 'is_correct')


# @admin.register(Subject)
# class ProductAdmin4(admin.ModelAdmin):
#     list_display = ('id', 'subject', 'is_visible')


# @admin.register(Attempt)
# class ProductAdmin5(admin.ModelAdmin):
#     list_display = ('id', 'user', 'test', 'end_time',
#                     'user_answers', 'total_score', 'attempt_number')


# # Or StackedInline for a different layout
# class AnswerInline(nested_admin.NestedTabularInline):
#     model = Answer
#     extra = 1  # Number of empty answer forms to display
#     show_change_link = True


# class QuestionInline(nested_admin.NestedTabularInline):
#     model = Question
#     extra = 1
#     show_change_link = True
#     inlines = (AnswerInline,)


# @admin.register(Test)
# class ProductAdmin1(nested_admin.NestedModelAdmin):
#     list_display = ('id', 'title', 'subject', 'created_at',
#                     'question_count', 'description', 'is_visible')
#     inlines = (QuestionInline,)
