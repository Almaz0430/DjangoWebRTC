from django.urls import path
from . import views

app_name = 'video_calls'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('create/', views.create_room, name='create_room'),
    path('join/<uuid:room_id>/', views.join_room, name='join_room'),
    path('leave/<uuid:room_id>/', views.leave_room, name='leave_room'),
] 