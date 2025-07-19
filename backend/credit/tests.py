from django.test import TestCase, Client
from .models import Customer, Loan
from django.urls import reverse

class CustomerAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            age=30,
            monthly_income=50000,
            approved_limit=200000,
            phone_number="9999999999"
        )

    def test_register_customer(self):
        response = self.client.post('/register', {
            "first_name": "Amit",
            "last_name": "Sharma",
            "age": 28,
            "monthly_income": 60000,
            "approved_limit": 300000,
            "phone_number": "9999988888"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_check_eligibility(self):
        response = self.client.post('/check-eligibility', {
            "customer_id": self.customer.id,
            "loan_amount": 50000,
            "interest_rate": 10,
            "tenure": 12
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_loan(self):
        response = self.client.post('/create-loan', {
            "customer_id": self.customer.id,
            "loan_amount": 50000,
            "interest_rate": 10,
            "tenure": 12
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)
