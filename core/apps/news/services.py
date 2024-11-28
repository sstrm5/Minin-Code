from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer
from core.apps.news.models import News
from core.apps.news.entities import News as NewsEntity


class ORMNewsService:
    def get_all_published_news(self) -> list[NewsEntity]:
        news = News.objects.filter(is_published=True)
        return [news.to_entity() for news in news]

    def add_picture_to_news(self, image):
        file_path = f"media/news/{image.name}"
        with open(file_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)
        return file_path

    def create_news(
            self,
            title: str,
            text: str,
            additional_text: str,
            # image_path: str,
            customer: CustomerEntity,
    ) -> NewsEntity:
        # , image=image_path
        news = News.objects.create(
            title=title, text=text, additional_text=additional_text, author=customer
        )
        return news.to_entity()
