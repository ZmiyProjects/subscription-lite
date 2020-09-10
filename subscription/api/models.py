from django.db import models
from datetime import datetime, timedelta


class Editor(models.Model):
    editor_name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.editor_name


class Journal(models.Model):
    editor = models.ForeignKey(Editor, on_delete=models.RESTRICT, related_name='journals')
    journal_name = models.CharField(max_length=100, unique=True, null=False)
    price = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.journal_name


class Customer(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    second_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=255, null=False)
    birth_date = models.DateField(null=False)
    registration_date = models.DateField(null=False, auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class Subscription(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.RESTRICT, related_name='subscriptions')
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name='subscriptions')
    start_date = models.DateField(null=False, auto_now_add=True)
    end_date = models.DateField(null=False, default=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"))

    class Meta:
        unique_together = ('journal', 'customer')
