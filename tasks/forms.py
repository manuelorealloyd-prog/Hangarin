from django import forms
from .models import Task, Note


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "priority", "category"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter task title"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter task description"}),
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
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
                attrs={"placeholder": "Enter your note"}
            ),
        }