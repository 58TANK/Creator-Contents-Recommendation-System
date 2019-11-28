from django.conf.urls import include, url
from board import views
from django.urls import path
app_name = 'board'


urlpatterns = [
    path('', views.recommend_tag, name='api_recommend_tag')
]