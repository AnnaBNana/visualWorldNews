from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    # url(r'getData$', views.getData),
    url(r'getGeoCode$', views.geoCodePlace),
]
