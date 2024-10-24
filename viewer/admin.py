from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Position, UserProfile, EmployeeInformation, BankAccount, EmergencyContact, Contract, Customer, \
    SubContract, Comment, Event, SecurityQuestion


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1  # Number of empty forms to display


class BankAccountInline(admin.StackedInline):
    model = BankAccount
    can_delete = False
    verbose_name_plural = 'Bank Account'


class EmployeeInformationInline(admin.StackedInline):
    model = EmployeeInformation
    can_delete = False
    verbose_name_plural = 'Employee Information'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'phone_number']
    inlines = [EmployeeInformationInline, BankAccountInline, EmergencyContactInline]


# registration of models for their management in the administration
admin.site.register(Position)
admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(SubContract)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(SecurityQuestion)
admin.site.register(Permission)
