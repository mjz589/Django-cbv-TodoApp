from django.urls import path
from . import views

app_name  = 'api-v1'

urlpatterns = [
    path("task/", views.taskList, name="task-list"),

]