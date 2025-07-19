from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def load_customer_data(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    for _, row in df.iterrows():
        Customer.objects.create(
            first_name=row['first_name'],
            last_name=row['last_name'],
            age=row['age'],
            phone_number=row['phone_number'],
            monthly_income=row['monthly_income'],
            approved_limit=row['approved_limit'],
        )

@shared_task
def load_loan_data(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()

    for _, row in df.iterrows():
        if Customer.objects.filter(id=row['customer_id']).exists():
            Loan.objects.create(
                customer_id=row['customer_id'],
                loan_amount=row['loan_amount'],
                tenure=row['tenure'],
                interest_rate=row['interest_rate'],
                monthly_installment=row['monthly_payment'],  
                emi_paid_on_time=row['emi_pai_on_time'],
                start_date=row['date_of_approval'],  
                end_date=row['end_date'] if not pd.isna(row['end_date']) else datetime.today().date()
            )

