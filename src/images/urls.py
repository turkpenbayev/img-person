from rest_framework import routers

from images.views import ImagesViewSet, PersonNamesViewSet

router = routers.SimpleRouter()
router.register('images', ImagesViewSet, basename='images')
router.register('person', PersonNamesViewSet, basename='person')


urlpatterns = [
    *router.urls
]