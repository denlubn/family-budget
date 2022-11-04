from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from budget.filtersets import BudgetFilter, IncomeFilter, ExpensesFilter
from budget.models import Budget, Income, Expenses
from budget.serializers import BudgetSerializer, IncomeSerializer, ExpensesSerializer, BudgetListSerializer


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all().prefetch_related("income", "expenses")
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BudgetFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BudgetListSerializer

        return BudgetSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(owner=self.request.user) | Q(shared=self.request.user)).distinct()


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = IncomeFilter

    def get_queryset(self):
        return self.queryset.filter(
            Q(budget__owner=self.request.user) | Q(budget__shared=self.request.user)
        ).distinct()


class ExpensesViewSet(ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpensesFilter

    def get_queryset(self):
        return self.queryset.filter(
            Q(budget__owner=self.request.user) | Q(budget__shared=self.request.user)
        ).distinct()
