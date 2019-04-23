from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register("tags", views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewset)

app_name = 'recipe'

urlpatterns = [
    # by doing this, if we register another viewset in our router,
    # we don't need to do any modification down here
    path('', include(router.urls))
]
