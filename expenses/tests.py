from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Expense


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(
        username=username,
        password=password
    )


def create_expense(user, title='Lunch', amount=12.50, category='Food'):
    return Expense.objects.create(
        title=title,
        description='Test expense',
        amount=amount,
        category=category,
        user=user,
    )


# Model tests
class ExpenseModelTest(TestCase):

    def setUp(self):
        self.user = create_user()

    def test_expense_is_created_with_correct_fields(self):
        expense = create_expense(self.user)
        self.assertEqual(expense.title, 'Lunch')
        self.assertEqual(expense.amount, 12.50)
        self.assertEqual(expense.user, self.user)

    def test_expense_is_linked_to_one_user(self):
        create_expense(self.user)
        self.assertEqual(self.user.expenses.count(), 1)


# Authentication tests
class AuthTest(TestCase):

    def test_signup_creates_user_and_redirects(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertRedirects(response, reverse('expenses:list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_unauthenticated_user_is_redirected_to_login_page(self):
        response = self.client.get(reverse('expenses:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])


# Expense list view tests
class ExpenseListViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )

    def test_list_shows_only_current_user_expenses(self):
        other_user = create_user(username='otheruser')
        create_expense(self.user, title='My Expense')
        create_expense(other_user, title='Their Expense')

        response = self.client.get(reverse('expenses:list'))
        expenses = response.context['expenses']

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].title, 'My Expense')

    def test_list_returns_200_for_logged_in_user(self):
        response = self.client.get(reverse('expenses:list'))
        self.assertEqual(response.status_code, 200)


# Expense create view tests
class ExpenseCreateViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )

    def test_create_expense_saves_to_database(self):
        self.client.post(reverse('expenses:create'), {
            'title': 'Coffee',
            'description': 'Morning coffee',
            'amount': 5.00,
            'category': 'Food',
        })
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().title, 'Coffee')

    def test_create_expense_assigns_logged_in_user(self):
        self.client.post(reverse('expenses:create'), {
            'title': 'Bus ticket',
            'description': 'Commute',
            'amount': 2.50,
            'category': 'Transport',
        })
        expense = Expense.objects.first()
        self.assertEqual(expense.user, self.user)


# Expense update view tests
class ExpenseUpdateViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        self.expense = create_expense(self.user)

    def test_update_expense_changes_fields(self):
        self.client.post(
            reverse('expenses:update', kwargs={
                'pk': self.expense.pk
            }),
            {
                'title': 'New Title',
                'description': 'Updated',
                'amount': 99.99,
                'category': 'Other',
            }
        )
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.title, 'New Title')
        self.assertEqual(self.expense.description, 'Updated')
        self.assertEqual(self.expense.amount, 99.99)
        self.assertEqual(self.expense.category, 'Other')
    
    def test_update_expense_only_one_field(self):
        new_amount = 45.2

        self.client.post(
            reverse('expenses:update', kwargs={
                'pk': self.expense.pk
            }),
            {
                'title': self.expense.title,
                'description': self.expense.description,
                'amount': new_amount,
                'category': self.expense.category,
            }
        )
        original_expense = self.expense
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.title, original_expense.title)
        self.assertEqual(self.expense.description, original_expense.description)
        self.assertEqual(self.expense.amount, new_amount)
        self.assertEqual(self.expense.category, original_expense.category)


    def test_user_cannot_update_another_users_expense(self):
        other_user = create_user(username='otheruser')
        other_expense = create_expense(other_user, title='Not yours')

        response = self.client.post(
            reverse('expenses:update', kwargs={
                'pk': other_expense.pk
            }),
            {
                'title': 'Hijacked',
                'description': '',
                'amount': 1,
                'category': ''
            }
        )
        self.assertEqual(response.status_code, 404)


# Expense delete view tests
class ExpenseDeleteViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client.login(username='testuser', password='testpass123')
        self.expense = create_expense(self.user)

    def test_delete_removes_expense_from_database(self):
        self.client.post(reverse('expenses:delete', args=[self.expense.pk]))
        self.assertEqual(Expense.objects.count(), 0)

    def test_user_cannot_delete_another_users_expense(self):
        other_user = create_user(username='otheruser')
        other_expense = create_expense(other_user)

        response = self.client.post(reverse('expenses:delete', args=[other_expense.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Expense.objects.filter(pk=other_expense.pk).exists())
