from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from friday.apps.accounts.models import User
from friday.apps.employees.models import Employee


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password')

    def clean(self) -> dict:
        data = super().clean()

        if self.errors:
            return data

        password = self.cleaned_data["password"]
        email = self.cleaned_data["email"]

        user: User = User.objects.filter(email=email).first()

        if not user:
            raise forms.ValidationError("Email or password is not valid",
                                        code="invalid_login")

        if not user.employee:
            raise forms.ValidationError("You're not registered as employee",
                                        code="invalid_user_employee")

        if user.employee.role != Employee.Role.DEVELOPER:
            raise forms.ValidationError("Only Developer can access this app",
                                        code="invalid_employee_role")

        self.user = authenticate(username=user.email, password=password)

        if not self.user:
            error = forms.ValidationError("Email or password is not valid",
                                          code="invalid_login")
            self.add_error("__all__", error)

        return data

    def login(self, request: HttpRequest) -> User:
        login(request, self.user)

        if not request.session.session_key:
            request.session.create()

        return request.user
