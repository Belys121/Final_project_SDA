from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView

from .models import Contract, Customer, Position, SubContract
from .forms import SignUpForm, ContractForm, CustomerForm, SubContractForm

from django.contrib.auth import get_user_model
User = get_user_model()


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        context['users'] = User.objects.all()
        context['contracts'] = Contract.objects.all()
        context['positions'] = Position.objects.all()
        return context


class ContractListView(ListView):
    model = Contract
    template_name = 'contracts_homepage.html'


# from logging import getLogger
# LOGGER = getLogger()
class ContractCreateView(CreateView):
    template_name = 'form.html'
    form_class = ContractForm
    success_url = reverse_lazy('navbar_contracts_all')

    # def form_invalid(self, form):
    #     LOGGER.warning(f'User provided invalid data. {form.errors}')
    #     return super().form_invalid(form)


class ContractUpdateView(UpdateView):
    template_name = "form.html"
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("homepage")


class ContractDeleteView(DeleteView):
    template_name = "form.html"
    model = Contract
    success_url = reverse_lazy('navbar_contracts_all')


class CustomerView(ListView):
    model = Customer
    template_name = 'customers.html'


class CustomerCreateView(CreateView):
    template_name = 'form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('navbar_customers')


class CustomerUpdateView(UpdateView):
    template_name = 'form.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('navbar_customers')


class CustomerDeleteView(DeleteView):
    template_name = 'form.html'
    model = Customer
    success_url = reverse_lazy('navbar_customers')


class UserListView(ListView):
    model = User
    template_name = 'users.html'


class PositionListView(ListView):
    model = Position
    template_name = 'positions.html'


class CustomerListView(ListView):
    model = Customer
    template_name = 'customers.html'


class ContractListView(ListView):
    model = Contract
    template_name = 'navbar_contracts.html'


class ContractAllListView(ListView):
    model = Contract
    template_name = 'navbar_contracts_all.html'



class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('homepage')
    
from django.contrib.auth.views import LoginView, PasswordChangeView

class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class SubmittablePasswordChangeView(PasswordChangeView):
  template_name = 'form.html'
  success_url = reverse_lazy('homepage')


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'detail_contract.html', {'contract': contract})


class SubContractView(ListView):
    model = SubContract
    template_name = 'subcontract.html'


class SubContractCreateView(FormView):
    template_name = 'form.html'
    form_class = SubContractForm
    success_url = reverse_lazy('navbar_contracts_all')

    def form_valid(self, form):
        new_sub_contract = form.save(commit=False)
        new_sub_contract.contract = Contract.objects.get(pk=int(self.kwargs["param"]))
        #TODO - ze SubContractForm "smažte" contract field. (místo __all__ dáte jen ['subcontract_name'])
        #TODO subcontract_number bych smazal z modelu a nahradil ho pomocí .pk, které již má každý model
        #alternativně zde můžete použít toto:
        #new_sub_contract.subcontract_number = 7
        new_sub_contract.save()
        #pomocí self.request.user zkontroluji, že jsou práva OK
        return super().form_valid(form)