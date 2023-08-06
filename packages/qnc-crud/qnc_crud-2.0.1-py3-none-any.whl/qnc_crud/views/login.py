from django.template.response import TemplateResponse
from django.views.generic import View

from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

from qnc_crud import js_response

class LoginView(View):
    def get(self, request):
        return TemplateResponse(request, 'qnc_crud/login.html', dict(form=AuthenticationForm()))

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if not form.is_valid() :
            return js_response.set_form_errors(form)

        auth.login(request, form.get_user())
        return js_response.go_back();

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return js_response.reload()
