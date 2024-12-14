from django.urls import path
from . import views
from .views import VoteView

app_name = 'board'

urlpatterns = [
    # path('', views.advertisement_list, name='advertisement_list'),
    path('', views.advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('edit/<int:pk>/', views.edit_advertisement, name='edit_advertisement'),
    path('delete/<int:pk>/', views.del_advertisement, name='del_advertisement'),
    # path('delete/<int:pk>/', views.vote_advertisement, name='vote_advertisement'),
    path('vote/<int:advertisement_id>/<str:action>/', VoteView.as_view(), name='vote'),

]
