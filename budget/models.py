from django.conf import settings
from django.db import models


class Budget(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budget")
    shared = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="shared_budget")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Income(models.Model):

    class IncomeCategories(models.TextChoices):
        EARNED = "earned",
        PORTFOLIO = "portfolio",
        PASSIVE = "passive",

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="income")
    category = models.CharField(choices=IncomeCategories.choices, max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.category}: {self.description}"


class Expenses(models.Model):

    class ExpensesCategories(models.TextChoices):
        UTILITIES = "utilities",
        TRANSPORTATION = "transportation",
        ENTERTAINMENT = "entertainment",
        RENT = "rent",
        HEALTH_INSURANCE = "health_insurance",
        CLOTHING = "clothing",
        OTHER = "other",

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="expenses")
    category = models.CharField(choices=ExpensesCategories.choices, max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.category}: {self.description}"
