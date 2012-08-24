# coding: utf-8
import json

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse 
from django.template import RequestContext
from django.db.models import Q

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