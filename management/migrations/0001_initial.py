# Generated by Django 4.2.1 on 2023-06-10 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "PENDING"), ("SUCCESS", "SUCCESS")],
                        default="PENDING",
                        max_length=250,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=management.models.user_contract_file_upload_path,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contracts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "organisation_name",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("profile_image", models.ImageField(upload_to="profile_image")),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ManagementRule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gross_area_then_net_area", models.BooleanField(default=False)),
                ("is_vacant_then_vacancy_reason", models.BooleanField(default=False)),
                ("option_then_date_provided", models.BooleanField(default=False)),
                ("index_then_date", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Management",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("lease_id", models.CharField(blank=True, max_length=250, null=True)),
                ("date_of_lease_date", models.DateField(blank=True, null=True)),
                ("first_day_of_term_date", models.DateField(blank=True, null=True)),
                ("last_day_of_term_date", models.DateField(blank=True, null=True)),
                ("lease_expiration_date", models.DateField(blank=True, null=True)),
                (
                    "rent_security",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "rent_security_type",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("tenant_id", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "tenant_name",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("is_company", models.BooleanField(blank=True, null=True)),
                ("from_date", models.DateField(blank=True, null=True)),
                ("to_date", models.DateField(blank=True, max_length=240, null=True)),
                (
                    "type_code",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "option_by_code",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "term",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "notice_term",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "notice_term_date",
                    models.DateField(blank=True, max_length=250, null=True),
                ),
                (
                    "term_frequency",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("fund_id", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "property_id",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("unit_id", models.CharField(blank=True, max_length=250, null=True)),
                ("unit_type", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "gross_area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "net_area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("vacant", models.BooleanField(blank=True, null=True)),
                (
                    "vacancy_note",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "amount_rent",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "amount_service_charge",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "amount_others",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "amount_discount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "charge_frequency",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("vat_code", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "vat_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "vat_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("start_payment_schedule", models.DateField(blank=True, null=True)),
                ("end_payment_schedule", models.DateField(blank=True, null=True)),
                (
                    "currency_code",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "index_series",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("index_type", models.CharField(blank=True, max_length=250, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                (
                    "index_frequency",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("index_date", models.DateField(blank=True, null=True)),
                (
                    "value",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("value_sr2", models.DateField(blank=True, null=True)),
                (
                    "index_date_sr2",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "contract",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="management.contract",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="managements",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
