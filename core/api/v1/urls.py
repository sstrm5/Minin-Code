from core.project import settings
from ninja import Router

# from core.api.v1.products.handlers import router as product_router
# from core.api.v1.questions.handlers import router as question_router
from core.api.v1.customers.handlers import router as customer_router
from core.api.v1.news.handlers import router as news_router
from core.api.v1.events.handlers import router as event_router
from core.api.v1.events.handlers_for_admin import router as event_admin_router
from core.api.v1.news.handlers_for_admin import router as news_admin_router

router = Router(tags=['v1'])
# router.add_router('products/', product_router)
# router.add_router('tests/', question_router)
router.add_router('customers/', customer_router)
router.add_router('news/', news_router)
router.add_router('events/', event_router)
router.add_router('events/admin/', event_admin_router)
router.add_router('news/admin/', news_admin_router)
