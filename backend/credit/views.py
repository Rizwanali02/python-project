from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from datetime import date


@api_view(['POST'])
def register_customer(request):
    data = request.data
    approved_limit = round(data["monthly_income"] * 36, -5)
    customer = Customer.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        monthly_income=data["monthly_income"],
        approved_limit=approved_limit,
        phone_number=data["phone_number"]
    )
    serializer = CustomerSerializer(customer)
    return Response({
        "customer_id": customer.id,
        "name": f"{customer.first_name} {customer.last_name}",
        "age": customer.age,
        "monthly_income": customer.monthly_income,
        "approved_limit": customer.approved_limit,
        "phone_number": customer.phone_number,
    })


@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    customer = Customer.objects.get(id=data["customer_id"])
    loan_amount = data["loan_amount"]
    tenure = data["tenure"]
    interest_rate = data["interest_rate"]

    past_loans = Loan.objects.filter(customer=customer)
    current_year = date.today().year
    current_year_loans = past_loans.filter(start_date__year=current_year)

    credit_score = 100
    on_time_emi = sum(loan.emi_paid_on_time for loan in past_loans)
    loan_count = past_loans.count()
    total_volume = sum(loan.loan_amount for loan in past_loans)
    current_total_debt = sum(loan.loan_amount for loan in past_loans)

    if current_total_debt > customer.approved_limit:
        credit_score = 0
    else:
        credit_score -= (loan_count * 5)
        credit_score -= (len(current_year_loans) * 10)
        credit_score -= (total_volume / customer.approved_limit) * 20
        credit_score += on_time_emi * 2
        credit_score = max(0, min(100, credit_score))

    approval = False
    corrected_interest = interest_rate

    if credit_score > 50:
        approval = True
    elif 30 < credit_score <= 50:
        if interest_rate < 12:
            corrected_interest = 12
        approval = True
    elif 10 < credit_score <= 30:
        if interest_rate < 16:
            corrected_interest = 16
        approval = True
    else:
        approval = False

    monthly_installment = loan_amount * (1 + (corrected_interest / 100)) / tenure
    if monthly_installment * tenure > customer.monthly_income * 0.5 * tenure:
        approval = False

    response_data = {
        "customer_id": customer.id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest,
        "tenure": tenure,
        "monthly_installment": monthly_installment
    }
    return Response(response_data)


@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer = Customer.objects.get(id=data["customer_id"])
    loan_amount = data["loan_amount"]
    tenure = data["tenure"]
    interest_rate = data["interest_rate"]
    monthly_installment = loan_amount * (1 + (interest_rate / 100)) / tenure
    end_date = date.today().replace(year=date.today().year + tenure // 12)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        tenure=tenure,
        interest_rate=interest_rate,
        monthly_installment=monthly_installment,
        end_date=end_date
    )
    return Response({
        "loan_id": loan.id,
        "customer_id": customer.id,
        "loan_approved": True,
        "message": "Loan Created Successfully",
        "monthly_installment": monthly_installment
    })


@api_view(['GET'])
def view_loan(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    customer = loan.customer
    data = {
        "loan_id": loan.id,
        "customer": {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
        },
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_installment,
        "tenure": loan.tenure,
    }
    return Response(data)


@api_view(['GET'])
def view_loans(request, customer_id):
    loans = Loan.objects.filter(customer_id=customer_id)
    data = []
    for loan in loans:
        data.append({
            "loan_id": loan.id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "repayments_left": loan.tenure - loan.emi_paid_on_time
        })
    return Response(data)
