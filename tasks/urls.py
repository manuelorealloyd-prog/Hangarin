from django.urls import path
from .views import (
    dashboard,
    task_list,
    category_list,
    priority_list,
    note_list,
    add_task,
    add_note,
    edit_task,
    delete_task,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("tasks/", task_list, name="task_list"),
    path("categories/", category_list, name="category_list"),
    path("priorities/", priority_list, name="priority_list"),
    path("notes/", note_list, name="note_list"),
    path("tasks/add/", add_task, name="add_task"),
    path("notes/add/", add_note, name="add_note"),
    path("tasks/edit/<int:task_id>/", edit_task, name="edit_task"),
    path("tasks/delete/<int:task_id>/", delete_task, name="delete_task"),
]