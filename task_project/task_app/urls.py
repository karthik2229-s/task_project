from django.urls import path
from .views import TaskView, UserListView

urlpatterns = [
    path('', TaskView.as_view(), name='task_list'),
    path('<int:pk>/', TaskView.as_view(), name='task_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
]