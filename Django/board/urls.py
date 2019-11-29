from django.conf.urls import include, url
from board import views
app_name = 'board'


urlpatterns = [
    url(r'^$', views.recommend_tag, name='api_recommend_tag')
]