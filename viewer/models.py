from datetime import datetime, timedelta, date
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import CharField, Model, ForeignKey, DateTimeField, DO_NOTHING, IntegerField, \
    EmailField, UniqueConstraint, CASCADE, PROTECT, Max
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from django.utils import timezone

User = get_user_model()


class Customer(Model):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    created = DateTimeField(auto_now_add=True)
    phone_number = CharField(max_length=16, default="123456789")
    email_address = EmailField(max_length=128, default="jan@novak.cz")


    def __str__(self):
        return f"Zákazník: {self.first_name} {self.last_name}"


class Contract(Model):
    contract_name = CharField(max_length=100)
    created = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=DO_NOTHING, default=1)
    customer = ForeignKey(Customer, on_delete=DO_NOTHING, default=1)
    status_choices = [("0", "V procesu"), ("1", "Dokončeno"), ("2", "Zrušeno")]
    status = CharField(max_length=64, choices=status_choices, default=status_choices[0])
    deadline = DateTimeField(default=timezone.now() + timedelta(days=30))


    def delta(self):
        current_date = timezone.now()
        return (self.deadline - current_date).days


    def __str__(self):
        return f"Zakázka: {self.contract_name}"


class SubContract(Model):
    subcontract_name = CharField(max_length=128)
    created = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=DO_NOTHING, default=1)
    contract = ForeignKey(Contract, related_name='subcontracts', on_delete=PROTECT)
    subcontract_number = IntegerField(null=True, blank=True, default=1)
    status_choices = [("0", "V procesu"), ("1", "Dokončeno"), ("2", "Zrušeno")]
    status = CharField(max_length=64, choices=status_choices, default=status_choices[0])

    class Meta:
        constraints = [
            UniqueConstraint(fields=["contract", "subcontract_number"], name="unique_subcontract_per_contract")
        ]

    @property
    def delta(self):
        if self.contract:
            delta_days = (self.contract.deadline - self.created).days
            return max(delta_days, 0)
        return None

    @classmethod
    def get_next_subcontract_number(cls, contract):
        max_number = cls.objects.filter(contract=contract).aggregate(Max('subcontract_number'))['subcontract_number__max']
        return (max_number or 0) + 1

    def __str__(self):
        return f"Podprojekt: {self.subcontract_name} {self.contract.pk}-{self.subcontract_number}"


class Position(Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SecurityQuestion(Model):
    question_text = CharField(max_length=255)

    def __str__(self):
        return f"{self.question_text}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, default="123456789")
    security_question = models.ForeignKey(SecurityQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)  # Allow blank answers

    def set_security_answer(self, raw_answer):
        self.security_answer = make_password(raw_answer)

    def check_security_answer(self, raw_answer):
        return check_password(raw_answer, self.security_answer)

    def __str__(self):
        return f"{self.user.username} - {self.position.name if self.position else 'No position'} - {self.phone_number}"



class Comment(Model):
    text = CharField(max_length=200)
    subcontract = ForeignKey(SubContract, on_delete=CASCADE, default=1)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentář: {self.text}"


# for calendar
class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.title


class BankAccount(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    account_prefix = models.CharField(max_length=6, default="000000", null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_code = models.CharField(max_length=4, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    iban = models.CharField(max_length=34, null=True, blank=True)
    swift_bic = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return f"{self.bank_name}, {self.account_prefix} - {self.account_number}/{self.bank_code}"


class EmergencyContact(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    descriptive_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class EmployeeInformation(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    permament_address = models.CharField(max_length=128)
    permament_descriptive_number = models.CharField(max_length=10)
    permament_postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    start_employee_contract = models.DateField(null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    contract_type = models.CharField(max_length=128, null=True, blank=True)

    def duration_of_employment(self):
        if self.start_employee_contract:
            today = date.today()
            delta_days = (today - self.start_employee_contract).days
            return max(delta_days, 0)
        return None


    # or years and days
    # def duration_of_employment(self):
    #     if self.start_employee_contract:
    #         today = date.today()
    #         delta = today - self.start_employee_contract
    #         years = delta.days // 365
    #         days = delta.days % 365
    #         return f"{years} let, {days} dní" if years else f"{days} dní"
    #     return None
