from django_filters.rest_framework import FilterSet, Filter

from budget.models import Budget, Income, Expenses


class BudgetFilter(FilterSet):
    class Meta:
        model = Budget
        fields = [
            "name",
        ]


class IncomeFilter(FilterSet):
    amount_gte = Filter(field_name="amount", lookup_expr="gte")
    amount_lte = Filter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Income
        fields = [
            "budget",
            "category",
        ]


class ExpensesFilter(FilterSet):
    amount_gte = Filter(field_name="amount", lookup_expr="gte")
    amount_lte = Filter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Expenses
        fields = [
            "budget",
            "category",
        ]
