from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, reverse

from django.views import View


class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html', {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))

        return render(request, 'registration/register.html', { 'form': form })
