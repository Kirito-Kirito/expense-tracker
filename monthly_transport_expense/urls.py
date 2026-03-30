from django.urls import path
from . import views

urlpatterns = [
    # path("", views.main, name="main"),
    path("", views.expense_list, name="expense_list"),
    path("delete/<int:pk>/", views.delete_expense, name="delete_expense"),
    path("edit/<int:pk>/", views.edit_expense, name="edit_expense"),
    path("export/pdf/", views.export_expenses_pdf, name="export_expenses_pdf"),
]
