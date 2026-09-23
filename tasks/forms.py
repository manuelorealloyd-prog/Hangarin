from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, Note, Category, Priority


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password"
        })
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "priority",
            "category"
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter task title"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Enter task description"}
            ),
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            )
        }
        input_formats = {
            "deadline": ["%Y-%m-%dT%H:%M"]
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["task", "content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Enter your note"})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter category name"})
        }


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter priority name"})
        }