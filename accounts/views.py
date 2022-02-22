import django
from django.shortcuts import redirect, render
from django.views.generic import View
from accounts.forms import SignUpForm
from django.contrib import messages

# Create your views here.
class SignUpView(View):
    template_name = 'accounts/sign_up.html'
    signup_form = SignUpForm

    def get(self, request):
        form = self.signup_form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.signup_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('core:home')
        return render(request, self.template_name, {'form': form})
