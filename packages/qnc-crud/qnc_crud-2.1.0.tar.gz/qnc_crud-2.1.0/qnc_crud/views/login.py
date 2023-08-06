from django.template.response import TemplateResponse
from django.views.generic import View

from django.conf import settings
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

        '''
            This works well when logging in from a public page which looks different when logged in.
            On such pages, you should include a login link with ?return=True as the query string.
        '''
        if request.GET.get('return') :
            return js_response.go_back()

        '''
            Otherwise, behave like django's login view.
        '''
        redirect = request.GET.get('next') or getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return js_response.go_to(redirect)

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return js_response.reload()
