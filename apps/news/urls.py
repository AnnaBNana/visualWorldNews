from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'getTwitter$',views.getTwitterData),
    # url(r'getData$', views.getData),
    url(r'getGeoCode$', views.geoCodePlace),
    url(r'frontEndData$', views.frontEndData),
]
