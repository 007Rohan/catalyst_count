from tempfile import NamedTemporaryFile

from allauth.account import forms, views
from celery.result import AsyncResult
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView

from .forms import CompanyFilterForm, FileUploadForm
from .models import Company
from .process_file import process_csv


class HomeView(TemplateView):
    template_name = 'base.html'


class UserListView(LoginRequiredMixin, ListView):    
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    login_url = '/company/login/'
    queryset = model.objects.order_by('id')


class RegisterView(views.SignupView):
    form_class = forms.SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class LoginView(views.LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    

class LogoutView(views.LogoutView):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('home')


class CompanyFilterView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies_filter.html'
    context_object_name = 'companies'
    login_url = '/company/login/'

    def get_queryset(self):
        form = CompanyFilterForm(self.request.GET)
        q_filters = Q()
        queryset = super().get_queryset()
        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            industry = form.cleaned_data.get('industry')
            year_founded = form.cleaned_data.get('year_founded')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            size_range = form.cleaned_data.get('size_range')

            industry_placeholder= 'Select Industry'
            year_founded_placeholder= 'Select Year Founded'
            city_placeholder= 'Select City'
            state_placeholder= 'Select State'
            country_placeholder= 'Select Country'
            size_range_placeholder= 'Select Size Range'

            if keyword:
                q_filters &= Q(name__icontains=keyword)
            if industry and industry != industry_placeholder:
                q_filters &= Q(industry=industry)
            if year_founded and year_founded != year_founded_placeholder:
                q_filters &= Q(year_founded=year_founded)
            if city and city != city_placeholder:
                q_filters &= Q(city_name=city)
            if state and state != state_placeholder:
                q_filters &= Q(state_name=state)
            if country and country != country_placeholder:
                q_filters &= Q(country_name=country)
            if size_range and size_range != size_range_placeholder:
                q_filters &= Q(size_range=size_range)

        queryset = queryset.filter(q_filters) if q_filters else queryset.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompanyFilterForm(self.request.GET)
        return context


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies_list.html'
    context_object_name = 'companies'
    login_url = '/company/login/'

class FileUploadView(LoginRequiredMixin, View):
    form_class = FileUploadForm
    template_name = 'file_upload.html'
    login_url = '/company/login/'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                with NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                    for chunk in file.chunks():
                        temp_file.write(chunk)
                    temp_file_path = temp_file.name
                task = process_csv.delay(temp_file_path)
                return JsonResponse({'task_id': task.id})
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid file type. Please upload a CSV file.'})
        return render(request, self.template_name, {'form': form})


class TaskProgressView(View):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == 'PROGRESS':
            return JsonResponse({'status': 'PROGRESS', 'current': result.info.get('current'), 'total': result.info.get('total')})
        elif result.state == 'SUCCESS':
            return JsonResponse({'status': 'SUCCESS'})
        else:
            return JsonResponse({'status': result.state})