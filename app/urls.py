from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),
    path('add-task/', views.add_task, name='add_task'),
    path('add-members/', views.create_user, name='create_user'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),


]