from django.db.models import Model
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from core.models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ('url',)


def create_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_bound and form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'register.html', {'form': form})


def url_redirect(request, key):
    try:
        url = Url.objects.get(key=key).url
        # redirect_count = Url.objects.get(key=key).redirect_count
        # redirect_count += 1
        Url.objects.get(key=key).redirect_count += 1
    except Model.DoesNotExist:
        url = reverse('index')
    return redirect(to=url)


@login_required
def url_shortener(request):
    ctx = {}
    form = UrlForm(request.POST or None)
    if form.is_bound and form.is_valid():
        obj = form.save()
        ctx['key'] = obj.key
        form = UrlForm()
    ctx['form'] = form
    return render(request, 'index.html', ctx)
