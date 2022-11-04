from django.contrib import admin

from budget.models import Budget, Income, Expenses

admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(Expenses)
