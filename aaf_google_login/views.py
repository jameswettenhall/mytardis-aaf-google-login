import logging

from six.moves import urllib

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import auth as djauth
from django.contrib.auth.models import User
from django.contrib import messages

from tardis.tardis_portal.forms import LoginForm
from tardis.tardis_portal.shortcuts import render_response_index

logger = logging.getLogger('tardis.apps.' + __name__)


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, request, **kwargs):
        url = request.META.get('HTTP_REFERER', '/')
        u = urllib.parse.urlparse(url)
        if u.netloc == request.META.get('HTTP_HOST', ""):
            next_page = u.path
        else:
            next_page = '/'
        c = super(LoginView, self).get_context_data(**kwargs)
        login_form = LoginForm()
        login_form.fields['username'].widget.attrs['style'] = \
            "width: 70%; max-width: 200px;"
        login_form.fields['password'].widget.attrs['style'] = \
            "width: 70%; max-width: 200px;"
        c['loginForm'] = login_form
        c['next_page'] = next_page
        return c

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect the user to the home page if he is trying to go to the
            # login page
            return HttpResponseRedirect(request.GET.get('next_page', '/'))

        c = self.get_context_data(request, **kwargs)
        return render_response_index(request, self.template_name, c)

    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request, *args, **kwargs):
        from tardis.tardis_portal.auth import auth_service
        c = self.get_context_data(request, **kwargs)
        if request.user.is_authenticated:
            # redirect the user to the home page if he is trying to go to the
            # login page
            return HttpResponseRedirect(request.POST.get('next_page', '/'))

        # TODO: put me in SETTINGS
        if 'username' in request.POST and \
                'password' in request.POST:
            authMethod = request.POST.get('authMethod', None)

            user = auth_service.authenticate(
                authMethod=authMethod, request=request)

            if user and user.is_active:
                next_page = request.POST.get(
                    'next_page', '/')
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                djauth.login(request, user)
                return HttpResponseRedirect(next_page)

            if user and not user.is_active:
                c['status'] = "Sorry, this account is inactive."
            else:
                c['status'] = "Sorry, username and password don't match."

            c['error'] = True
            c['loginForm'] = LoginForm()

            return HttpResponseForbidden(
                render_response_index(request, self.template_name, c))

        return render_response_index(request, self.template_name, c)
