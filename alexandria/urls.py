from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from acervo.views import LivroViewSet


router = routers.DefaultRouter()
router.register(r'livros', LivroViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Minhas API's
    url(r'^', include(router.urls)),

    # rest framework browserable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]