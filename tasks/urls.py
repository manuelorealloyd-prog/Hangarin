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
    login_view,
    logout_view,
    add_category,
    add_priority,
    activity_list,
    delete_note,
    delete_category,
    delete_priority,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("activity/", activity_list, name="activity_list"),

    path("tasks/", task_list, name="task_list"),
    path("categories/", category_list, name="category_list"),
    path("priorities/", priority_list, name="priority_list"),
    path("notes/", note_list, name="note_list"),

    path("tasks/add/", add_task, name="add_task"),
    path("notes/add/", add_note, name="add_note"),
    path("categories/add/", add_category, name="add_category"),
    path("priorities/add/", add_priority, name="add_priority"),

    path("tasks/edit/<int:task_id>/", edit_task, name="edit_task"),
    path("tasks/delete/<int:task_id>/", delete_task, name="delete_task"),

    path("notes/delete/<int:note_id>/", delete_note, name="delete_note"),
    path("categories/delete/<int:category_id>/", delete_category, name="delete_category"),
    path("priorities/delete/<int:priority_id>/", delete_priority, name="delete_priority"),
]