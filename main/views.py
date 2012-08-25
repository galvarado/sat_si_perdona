# coding: utf-8
import json
import os

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse 
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from main.models import DataBaseFile
from main.forms import DataBaseFileForm
import import_excel

def index(request):
    '''
    Show index page
    '''
    return render_to_response('index.html', RequestContext(request))

def map(request):
    '''
    Show map page
    '''
    return render_to_response('map.html', RequestContext(request))

def search(request):
    '''
    Show search page
    '''
    return render_to_response('search.html', RequestContext(request))

def get_credits(request):
    '''
    Retrive deputies table
    '''
    aaData = []
    start = 0
    display_length = 0
    end = 0
    search = request.POST.get('sSearch')
    users = []
    count = 0

    for user in users[start:end]:
        group = 'Sin asignar' if user.profile.group is None else user.profile.group.name
        aaData.append([
            user.username,
            user.email,
            group,
            '<input type="checkbox" data-id="%s">' % user.pk,
        ])
    data = {
        "iTotalRecords": count,
        "iDisplayStart": start,
        "iDisplayLength": display_length,
        "iTotalDisplayRecords": count,
        "aaData":aaData
    }
    return HttpResponse(json.dumps(data))

def login(request):
    """
    Function to login an user
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('manage'))

    auth_form = AuthenticationForm()
    if request.method == 'POST':
        auth_form = AuthenticationForm(None, request.POST)
        if auth_form.is_valid():
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            auth_login(request, auth_form.get_user())
            return HttpResponseRedirect(reverse('manage'))

    return render_to_response('registration/login.html', RequestContext(request, {
        'form': auth_form,
    }))

@login_required
def logout(request):
    """
    Function to logout an user
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def manage(request):
    '''
    Show manage page
    '''
    db_file = DataBaseFile.objects.all()
    return render_to_response('manage.html', RequestContext(request, {
        'db_file': db_file
    }))

@login_required
def change_db(request):
    '''
    Display form to add a db file
    '''
    form = DataBaseFileForm()
    if request.method == 'POST':
        form = DataBaseFileForm(request.POST, request.FILES)
        if form.is_valid():
            DataBaseFile.objects.all().delete()
            filelist = [ f for f in os.listdir(".") if f.endswith(".xls") ]
            for f in filelist:
                os.remove(f)
            content = form.save()
            import_excel.import_file(content.file_name()) 
            return HttpResponseRedirect(reverse('manage'))
    return render_to_response('change_db.html', RequestContext(request, {
        'form': form,
    }))