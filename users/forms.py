from django import forms
from django.contrib.auth.models import User

from users.models import UserProfile
from django.core.exceptions import ValidationError


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    organisation_name = forms.SlugField(max_length=255)
    profile_image = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "organisation_name",
            "profile_image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["username"].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.user.email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.instance.user.username != username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self.instance.user.email != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("This email is already taken.")
        return email

    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        self.instance.organisation_name = self.cleaned_data["organisation_name"]
        if commit:
            self.instance.save()
        return self.instance


class AdminUpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    organisation_name = forms.CharField(max_length=255)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "organisation_name",
            "is_staff",
            "is_superuser",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["username"].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.user.email
            self.fields["is_staff"].initial = self.instance.user.is_staff
            self.fields["is_superuser"].initial = self.instance.user.is_superuser
            self.fields["password"].initial = self.instance.user.password

    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.instance.user.username != username:
            if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
                raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self.instance.user.email != email:
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise ValidationError("This email is already taken.")
        return email

    def clean_organisation_name(self):
        organisation_name = self.cleaned_data["organisation_name"]
        if self.instance.organisation_name != organisation_name:
            if UserProfile.objects.filter(organisation_name=organisation_name).exclude(id=self.instance.id).exists():
                raise ValidationError("This organisation_name is already taken.")
        return organisation_name

    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.save()
        self.instance.organisation_name = self.cleaned_data["organisation_name"]
        if commit:
            self.instance.save()
        return self.instance


class UserCreationCustomForm(forms.Form):
    """this form is used to create new user"""
    first_name = forms.SlugField(required=True)
    last_name = forms.SlugField(required=True)
    username = forms.SlugField(required=True)
    organisation_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    password = forms.CharField(required=True)


class ChangePasswordForm(forms.Form):
    password = forms.SlugField()
    confirm_password = forms.SlugField()
