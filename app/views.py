from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView

from app.models import Person, TypeDocument, Document, Event


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


def person_view(request, person_id):
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
    }
    return render(request, 'app/person.html', context)


class AddDocForm(forms.Form):
    type_doc = forms.CharField(label='Тип документа', required=True)
    date_to = forms.DateTimeField(required=False, label='От')
    date_from = forms.DateTimeField(required=False, label='До')
    file = forms.FileField(required=True, label='Документ')


def person_add_doc(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        person = None

    if request.method == 'POST':
        form = AddDocForm(request.POST, request.FILES)
        if form.is_valid():
            type_doc = form.cleaned_data['type_doc']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            file = None
            if 'file' in request.FILES:
                # get doc
                file = request.FILES['file']

            try:
                type_doc_obj = TypeDocument.objects.get(name=type_doc)
            except TypeDocument.DoesNotExist:
                type_doc_obj = TypeDocument.objects.create(name=type_doc)

            Document.objects.create(person=person,
                                    type_doc=type_doc_obj,
                                    date_from=date_from,
                                    date_to=date_to,
                                    file=file)

            return redirect(person_view, person_id)
    else:
        form = AddDocForm()

    context = {
        'form': form
    }
    return render(request, 'app/add_doc.html', context)


def ask_for_permit(request):
    print(request.POST)
    contractor_name = request.POST.get('contractor', None)
    person_ids = request.POST.get('ids[]', [])

    try:
        contractor = User.objects.get(username=contractor_name)
    except User.DoesNotExist:
        pass

    event = Event.objects.create(event_type=Event.REQUEST_PERMIT,
                                 status=Event.NEW)

    print(event)
    for person_id in person_ids:
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            pass
        else:
            event.persons.add(person)
            person.status = Person.IN_PROCESS
            person.save()

    event.save()

    return redirect(lk)
