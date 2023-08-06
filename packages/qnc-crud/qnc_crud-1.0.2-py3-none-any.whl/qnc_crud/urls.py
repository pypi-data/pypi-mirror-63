from django.urls import path
# from qnc_crud.views.login import LoginView
from qnc_crud.views.form_test import FormTestView

urlpatterns = [
    # path('login/', LoginView.as_view()),
    path('form_test/', FormTestView.as_view()),
]