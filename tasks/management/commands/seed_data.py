from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from tasks.models import Task, Note, SubTask, Priority, Category


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker()

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        statuses = ["Pending", "In Progress", "Completed"]

        for i in range(20):
            task = Task.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                status=random.choice(statuses),
                deadline=timezone.make_aware(
                    fake.date_time_this_month()
                ),
                priority=random.choice(priorities),
                category=random.choice(categories)
            )

            Note.objects.create(
                task=task,
                content=fake.paragraph()
            )

            SubTask.objects.create(
                title=fake.sentence(),
                status=random.choice(statuses),
                task=task
            )

        self.stdout.write(
            self.style.SUCCESS("Sample data created successfully.")
        )