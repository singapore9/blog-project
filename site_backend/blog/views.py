from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import View
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Article
from .serializers import ReadOnlyArticleSerializer, WriteOnlyArticleSerializer


def logout_request(request):
    logout(request)
    return redirect('schema-swagger-ui')


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            url = reverse('schema-swagger-ui')
            return HttpResponseRedirect(url)
        else:
            context = {}
            context.update(csrf(request))
            context['login_form'] = AuthenticationForm
            context['next'] = self.request.GET.get('next')
            return render(request, 'login.html', context=context)

    def post(self, request):
        # having received the authorization request
        form = AuthenticationForm(request, data=self.request.POST)

        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())
            next_url = request.POST.get('next')

            if next_url:
                response = HttpResponseRedirect(next_url)
                return response
            else:
                url = reverse('schema-swagger-ui')
                return HttpResponseRedirect(url)
        else:
            # If not true, then the user will appear on the login page
            # and see an error message
            context = {}
            context.update(csrf(request))
            context['next'] = self.request.GET.get('next')
            context['login_form'] = form

            return render(request=request, template_name='login.html', context=context)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', ]:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update',  'destroy']:
            return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', ]:
            return ReadOnlyArticleSerializer
        else:
            return WriteOnlyArticleSerializer

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        request = super().initialize_request(request, *args, **kwargs)
        return request

    def get_parsers(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return [JSONParser(), ]
        elif self.action in ['create', 'update', 'partial_update']:
            return [MultiPartParser(), FormParser()]
