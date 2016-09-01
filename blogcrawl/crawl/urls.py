from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'/blog', views.BlogViewSet)
router.register(r'/link', views.LinkViewSet)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^/in_degrees/(?P<page>[0-9]+)$', views.in_degrees),
    url(r'^/out_degrees/(?P<page>[0-9]+)$', views.out_degrees),
    url(r'^/api', include(router.urls)),
    url(r'/count$', views.link_count),
]