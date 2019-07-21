from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import FormView

from app.models import Person


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "app/index.html"

    success_url = "lk/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('login')


def lk(request):
    persons = Person.objects.filter(contractor=request.user)

    context = {
        'persons': persons
    }
    return render(request, 'app/index.html', context)


def person(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        person = None

    context = {
        'person': person
    }
    return render(request, 'app/person.html', context)


def add_person(request):
    context = {
        'person': person
    }
    return render(request, 'app/person.html', context)
