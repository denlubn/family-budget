from rest_framework.serializers import ModelSerializer

from budget.models import Income, Expenses, Budget
from user.serializers import SharedUserSerializer


class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "category", "description", "amount", "budget"]


class ExpensesSerializer(ModelSerializer):
    class Meta:
        model = Expenses
        fields = ["id", "category", "description", "amount", "budget"]


class BudgetSerializer(ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "owner", "name", "income", "expenses", "shared"]


class BudgetListSerializer(BudgetSerializer):
    income = IncomeSerializer(many=True, read_only=True)
    expenses = ExpensesSerializer(many=True, read_only=True)
    shared = SharedUserSerializer(many=True, read_only=True)
