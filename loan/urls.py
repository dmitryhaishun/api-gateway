from django.urls import path

from loan.views.loan_products import GetLoanProductsView, GetLoanProductByIdView
from loan.views.loan import GetAllLoansWithFilterView, GetLoansByIdView, CreateNewLoanView

urlpatterns = [
    path('', GetAllLoansWithFilterView.as_view(), name='get_loans_or_loan_applications'),
    path('<int:loan_id>/', GetLoansByIdView.as_view(), name='get_loan_by_id'),
    path('create', CreateNewLoanView.as_view(), name='create_new_loan'),
    path('products/', GetLoanProductsView.as_view(), name="get_loan_products"),
    path('products/<int:loan_product_id>/', GetLoanProductByIdView.as_view(), name="get_loan_product_by_id"),
]
