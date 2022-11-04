from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from budget.models import Budget, Income, Expenses
from budget.serializers import BudgetListSerializer, IncomeSerializer, ExpensesSerializer

BUDGET_URL = reverse("budget-list")
INCOME_URL = reverse("income-list")
EXPENSES_URL = reverse("expenses-list")


def sample_budget(**params):
    defaults = {
        "name": "Test name",
    }
    defaults.update(params)

    return Budget.objects.create(**defaults)


def sample_income(**params):
    defaults = {
        "category": "earned",
        "amount": "1000.00",
        "description": "Test income"
    }
    defaults.update(params)

    return Income.objects.create(**defaults)


def sample_expenses(**params):
    defaults = {
        "category": "entertainment",
        "amount": "600.00",
        "description": "Test expenses"
    }
    defaults.update(params)

    return Expenses.objects.create(**defaults)


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BUDGET_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(INCOME_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(EXPENSES_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser1",
            email="test1@test.com",
            password="testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_budget(self):
        sample_budget(owner=self.user)
        sample_budget(owner=self.user)

        res = self.client.get(BUDGET_URL)

        budgets = Budget.objects.all()
        serializer = BudgetListSerializer(budgets, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_income(self):
        testuser1_budget = sample_budget(owner=self.user)
        sample_income(budget=testuser1_budget)
        sample_income(budget=testuser1_budget)

        res = self.client.get(INCOME_URL)

        incomes = Income.objects.all()
        serializer = IncomeSerializer(incomes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_income_filtering_by_user(self):
        """
        Test income doesn't display if budget owner or
        budget shared is not our user
        """
        another_user = get_user_model().objects.create_user(
            username="another_user",
            email="another_user@test.com",
            password="testpass",
        )
        testuser1_budget = sample_budget(owner=self.user)
        another_user_budget = sample_budget(owner=another_user)

        income1 = sample_income(budget=testuser1_budget)
        income2 = sample_income(budget=testuser1_budget)

        income3 = sample_income(budget=another_user_budget)

        res = self.client.get(INCOME_URL)

        serializer1 = IncomeSerializer(income1)
        serializer2 = IncomeSerializer(income2)
        serializer3 = IncomeSerializer(income3)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_list_income_filtering_by_category(self):
        budget = sample_budget(owner=self.user)

        income1 = sample_income(budget=budget)
        income2 = sample_income(budget=budget)

        income3 = sample_income(budget=budget, category="passive")

        res = self.client.get(INCOME_URL, {"category": "passive"})

        serializer1 = IncomeSerializer(income1)
        serializer2 = IncomeSerializer(income2)
        serializer3 = IncomeSerializer(income3)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertIn(serializer3.data, res.data["results"])

    def test_list_expenses(self):
        testuser1_budget = sample_budget(owner=self.user)
        sample_expenses(budget=testuser1_budget)
        sample_expenses(budget=testuser1_budget)

        res = self.client.get(EXPENSES_URL)

        expenses = Expenses.objects.all()
        serializer = ExpensesSerializer(expenses, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_expenses_filtering_by_user(self):
        """
        Test expenses doesn't display if budget owner or
        budget shared is not our user
        """
        another_user = get_user_model().objects.create_user(
            username="another_user",
            email="another_user@test.com",
            password="testpass",
        )
        testuser1_budget = sample_budget(owner=self.user)
        another_user_budget = sample_budget(owner=another_user)

        expenses1 = sample_expenses(budget=testuser1_budget)
        expenses2 = sample_expenses(budget=testuser1_budget)

        expenses3 = sample_expenses(budget=another_user_budget)

        res = self.client.get(EXPENSES_URL)

        serializer1 = ExpensesSerializer(expenses1)
        serializer2 = ExpensesSerializer(expenses2)
        serializer3 = ExpensesSerializer(expenses3)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_list_expenses_filtering_by_category(self):
        budget = sample_budget(owner=self.user)

        expenses1 = sample_expenses(budget=budget)
        expenses2 = sample_expenses(budget=budget)

        expenses3 = sample_expenses(budget=budget, category="rent")

        res = self.client.get(EXPENSES_URL, {"category": "rent"})

        serializer1 = ExpensesSerializer(expenses1)
        serializer2 = ExpensesSerializer(expenses2)
        serializer3 = ExpensesSerializer(expenses3)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertIn(serializer3.data, res.data["results"])
