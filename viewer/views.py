import json

from django.contrib.admin.templatetags.admin_list import search_form
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.base import kwarg_re
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView, DetailView
from sympy.polys.polyconfig import query

from .models import Contract, Customer, Position, SubContract, Event, Comment
from .forms import SignUpForm, ContractForm, CustomerForm, SubContractForm, SubContractFormUpdate, CommentForm, \
    SearchForm

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'detail_contract.html', {'contract': contract})

@login_required
def show_subcontracts(request):
    query = request.GET.get("query", "")
    subcontracts = SubContract.objects.filter(user=request.user)
    if query:
        subcontracts = subcontracts.filter(
            Q(subcontract_name__icontains=query)
        )
    search_form = SearchForm(initial={'query': query})
    search_url = 'navbar_show_subcontracts'
    show_search = True

    return render(request, 'subcontract.html', {
        'subcontracts': subcontracts,
        'search_form': search_form,
        'search_url': search_url,
        'show_search': show_search,
    })

@login_required
def subcontract_detail(request, subcontract_id):
    subcontract = get_object_or_404(SubContract, pk=subcontract_id)
    contract = subcontract.contract
    return render(request, 'detail_subcontract.html', {'subcontract': subcontract, 'contract': contract})


class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['users'] = User.objects.all()
        context['subcontracts'] = SubContract.objects.filter(user=self.request.user)
        contracts = Contract.objects.filter(user=self.request.user)
        sorted_contracts = sorted(contracts, key=lambda contract: contract.delta())
        context['contracts'] = sorted_contracts
        today = date.today()
        context['events'] = Event.objects.filter(
            Q(start_time__date=today) |
            Q(end_time__date=today) |
            Q(start_time__date__lt=today, end_time__date__gt=today)
        ).order_by('start_time')
        return context


class ContractCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ContractForm
    success_url = reverse_lazy('navbar_contracts_all')


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("navbar_contracts_all")


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "form.html"
    model = Contract
    success_url = reverse_lazy('navbar_contracts_all')


class CustomerView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'


class CustomerCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('navbar_customers')


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('navbar_customers')


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'form.html'
    model = Customer
    success_url = reverse_lazy('navbar_customers')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'employees.html'
    context_object_name = "employees"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["search_url"] = "employees"
        context["show_search"] = True
        return context


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'navbar_customers.html'
    context_object_name = "customers"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["search_url"] = "navbar_customers"
        context["show_search"] = True
        return context


class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'navbar_contracts.html'
    context_object_name = "contracts"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Contract.objects.filter(user=self.request.user)
            query = self.request.GET.get("query")
            if query:
                queryset = queryset.filter(contract_name__icontains=query)
            return sorted(queryset, key=lambda contract: contract.delta())
        return Contract.objects.none()  #TODO nebo all?

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["search_url"] = "navbar_contracts"
        context["show_search"] = True
        return context

class ContractAllListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'navbar_contracts_all.html'
    context_object_name = "contracts"

    def get_queryset(self):
        queryset = Contract.objects.all()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(contract_name__icontains=query)
        return sorted(queryset, key=lambda contract: contract.delta())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET or None)
        context["search_url"] = "navbar_contracts_all"
        context["show_search"] = True
        return context


class SignUpView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('homepage')
    
from django.contrib.auth.views import LoginView, PasswordChangeView


class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class SubmittablePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
  template_name = 'form.html'
  success_url = reverse_lazy('homepage')


class SubContractView(LoginRequiredMixin, ListView):
    model = SubContract
    template_name = 'subcontracts_homepage.html'


class SubContractCreateView(LoginRequiredMixin, FormView):
    template_name = 'form.html'
    form_class = SubContractForm

    def form_valid(self, form):
        new_sub_contract = form.save(commit=False)
        new_sub_contract.contract = Contract.objects.get(pk=int(self.kwargs["param"]))
        max_subcontract_number = SubContract.objects.filter(contract=new_sub_contract.contract).aggregate(Max('subcontract_number'))['subcontract_number__max']
        new_sub_contract.subcontract_number = (max_subcontract_number or 0) + 1
        new_sub_contract.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contract_detail', kwargs={'pk': self.kwargs['param']})


class SubContractUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    model = SubContract
    form_class = SubContractForm

    def get_object(self):
        contract_pk = self.kwargs.get("contract_pk")
        subcontract_number = self.kwargs.get("subcontract_number")
        return SubContract.objects.get(contract__pk=contract_pk, subcontract_number=subcontract_number)

    def get_success_url(self):
        return reverse_lazy('contract_detail', kwargs={'pk': self.kwargs['contract_pk']})


class SubContractDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "form.html"
    model = SubContract

    def get_success_url(self):
        contract_id = self.object.contract.id
        return reverse_lazy('contract_detail', kwargs={'pk': contract_id})


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = CommentForm

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.subcontract = SubContract.objects.get(pk=int(self.kwargs["pk"]))
        new_comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        subcontract = SubContract.objects.get(pk=int(self.kwargs["pk"]))
        contract_id = subcontract.contract.pk
        return reverse_lazy('subcontract_detail', kwargs={'contract_pk': contract_id, "subcontract_number": subcontract.subcontract_number })


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "comments_homepage.html"



from django.http import JsonResponse
from .models import Event # Předpokládejme, že máš model pro události
import json
from datetime import datetime, date
from django.contrib.auth.models import Group


@login_required
def calendar_view(request):
    return render(request, 'calendar.html')


@login_required
def events_feed(request):
    events = Event.objects.all()
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'extendedProps': {
                'group': event.group.name if event.group else 'No Group'
            }
        } for event in events
    ]
    return JsonResponse(events_data, safe=False)


@login_required
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        group_name = data.get('group')

        group = Group.objects.filter(name=group_name).first()
        if group:
            event = Event.objects.create(
                title=title,
                start_time=datetime.strptime(start_time, '%Y-%m-%dT%H:%M'),
                end_time=datetime.strptime(end_time, '%Y-%m-%dT%H:%M'),
                group=group
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Group not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def get_groups(request):
    groups = Group.objects.all()
    groups_data = [{'name': group.name} for group in groups]
    return JsonResponse(groups_data, safe=False)


@login_required
def delete_event(request, event_id):
    if request.method == 'DELETE':
        try:
            event = Event.objects.get(pk=event_id)
            event.delete()
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@csrf_exempt
def update_event(request, event_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            event = Event.objects.get(pk=event_id)
            event.title = data.get('title', event.title)
            event.start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
            event.end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
            group_name = data.get('group')
            if group_name:
                group = Group.objects.filter(name=group_name).first()
                if group:
                    event.group = group
            event.save()
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class ContractView(LoginRequiredMixin, DetailView):
    model = Contract
    template_name = "detail_contract.html"


class SubContractDetailView(LoginRequiredMixin, DetailView):
    template_name = "detail_subcontract.html"
    model = SubContract

    def get_object(self):
        contract_pk = self.kwargs.get("contract_pk")
        subcontract_number = self.kwargs.get("subcontract_number")
        return SubContract.objects.get(contract__pk=contract_pk, subcontract_number=subcontract_number)
