import os
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer
from core.apps.news.models import News
from core.apps.news.entities import News as NewsEntity


class ORMNewsService:
    def get_all_published_news(self) -> list[NewsEntity]:
        news = News.objects.filter(is_published=True)
        return [news.to_entity() for news in news]

    def add_picture_to_news(self, file):
        if not os.path.exists("media/news"):
            os.makedirs("media/news")
        file_path = f"news/{file.name}"
        with open("media/" + file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return file_path

    def create_news(
            self,
            title: str,
            text: str,
            additional_text: str,
            file_path: str,
            customer: CustomerEntity,
    ) -> NewsEntity:
        news = News.objects.create(
            title=title, text=text, additional_text=additional_text, author=customer, image=file_path,
        )
        return news.to_entity()


class ORMNewsAdminService:
    def get_news(self) -> list[NewsEntity]:
        news = News.objects.all().order_by('is_published', '-created_at')
        return [news.to_entity() for news in news]

    def publish_news(self, news_id: int) -> NewsEntity:
        news = News.objects.get(id=news_id)
        news.is_published = True
        news.save()
        return news.to_entity()

    def unpublish_news(self, news_id: int) -> NewsEntity:
        news = News.objects.get(id=news_id)
        news.is_published = False
        news.save()
        return news.to_entity()
