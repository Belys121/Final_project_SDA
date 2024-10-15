# Generated by Django 4.1.1 on 2024-10-15 16:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('0', 'V procesu'), ('1', 'Dokončeno'), ('2', 'Zrušeno')], default=('0', 'V procesu'), max_length=64)),
                ('deadline', models.DateTimeField(default=datetime.datetime(2024, 11, 14, 18, 18, 14, 603009))),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.CharField(default='123456789', max_length=16)),
                ('email_address', models.EmailField(default='jan@novak.cz', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups_name', models.CharField(max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, default='123456789', max_length=15, null=True)),
                ('security_answer', models.CharField(blank=True, max_length=255)),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.position')),
                ('security_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.securityquestion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcontract_name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subcontract_number', models.IntegerField(blank=True, default=1, null=True)),
                ('status', models.CharField(choices=[('0', 'V procesu'), ('1', 'Dokončeno'), ('2', 'Zrušeno')], default=('0', 'V procesu'), max_length=64)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subcontracts', to='viewer.contract')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permament_address', models.CharField(max_length=128)),
                ('permament_descriptive_number', models.CharField(max_length=10)),
                ('permament_postal_code', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=15)),
                ('start_employee_contract', models.DateField(blank=True, null=True)),
                ('birth_day', models.DateField(blank=True, null=True)),
                ('contract_type', models.CharField(blank=True, max_length=128, null=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='viewer.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('descriptive_number', models.CharField(max_length=10)),
                ('postal_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=15)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contacts', to='viewer.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.customer'),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subcontract', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='viewer.subcontract')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_prefix', models.CharField(blank=True, default='000000', max_length=6, null=True)),
                ('account_number', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_code', models.CharField(blank=True, max_length=4, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=50, null=True)),
                ('iban', models.CharField(blank=True, max_length=34, null=True)),
                ('swift_bic', models.CharField(blank=True, max_length=11, null=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='viewer.userprofile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='subcontract',
            constraint=models.UniqueConstraint(fields=('contract', 'subcontract_number'), name='unique_subcontract_per_contract'),
        ),
    ]
