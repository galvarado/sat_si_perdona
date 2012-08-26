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
from django.db.models import Avg, Max, Min, Count

from main.models import DataBaseFile, Credit
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
    Retrive deputies table when user search in map
    '''
    aaData = []
    start = request.POST.get('iDisplayStart')
    display_length = request.POST.get('iDisplayLength')
    end = start + display_length
    credits = Credit.objects.all()
    count = credits.count()

    for credit in credits[start:end]:
        aaData.append([
            '$%s' % str(credit.amount),
            credit.cancel_reason,
            credit.supposed_by,
            credit.entity,
            credit.sector,
            
        ])
    data = {
        'iTotalRecords': count,
        'iDisplayStart': start,
        'iDisplayLength': display_length,
        'iTotalDisplayRecords': count,
        'aaData':aaData
    }
    return HttpResponse(json.dumps(data))

def get_graph_by_state(request):
    response = 0
    if request.method == 'POST' and request.is_ajax():
        state = request.POST.get('state')

        _query = "SELECT id, taxpayer_type, ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM main_credit WHERE entity LIKE '%%" + state + "%%')) AS pct FROM main_credit WHERE entity LIKE '%%" + state + "%%' GROUP BY taxpayer_type;"
        credits = Credit.objects.raw(_query)
        total_amount = Credit.objects.filter(entity=state).aggregate(Count('amount'))
        persons_type = []
        persons_type_values = []
        for credit in credits:
            persons_type.append(credit.taxpayer_type)
            persons_type_values.append(int(credit.pct))

        _query = "SELECT id, sector, ROUND(SUM(amount)) AS amount FROM main_credit WHERE entity LIKE '%%"+state+"%%' GROUP BY sector;"
        credits = Credit.objects.raw(_query)
        sectors_name = []
        sectors_values = []
        for credit in credits:
            sectors_name.append(credit.sector)
            sectors_values.append(int(credit.amount))

        _query = "SELECT id, cancel_reason, ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM main_credit WHERE entity LIKE '%%"+state+"%%')) AS pct FROM main_credit WHERE entity LIKE '%%"+state+"%%' GROUP BY cancel_reason;"
        credits = Credit.objects.raw(_query)
        reasons_name = []
        reasons_values = []
        for credit in credits:
            reasons_name.append(credit.cancel_reason)
            reasons_values.append(int(credit.pct))


        data = {
            'response': 1,
            'persons_type': persons_type,
            'persons_type_values': persons_type_values,
            'sectors_name': sectors_name,
            'sectors_values': sectors_values,
            'reasons_name': reasons_name,
            'reasons_values': reasons_values,
            'total_amount': total_amount,
            'state': state,
        }
        return HttpResponse(json.dumps(data))

def get_credits_search(request):
    '''
    Retrive deputies specific search
    '''
    aaData = []
    start = request.POST.get('iDisplayStart')
    display_length = request.POST.get('iDisplayLength')
    end = display_length
    search = request.POST.get('sSearch', None)
    if search:

        search = search.split(' ')

        #fields = ('sex', 'name', 'lastname', 'party', 'election_type', 'entity', 'district', 'circunscription', 'phone', 'extension', 'email', 'twitter', 'commissions', 'bio', 'patrimony', 'answer', 'answer_why', 'suplent', 'status')
        fields = ('amount', 'cancel_reason', 'supposed_by', 'taxpayer_type', 'entity', 'sector')

        # Query to filter records
        _query = """SELECT * FROM main_credit WHERE 1"""

        args_to_append = []

        for arg in search:
            _query += """ AND ("""

            i = 0

            for field in fields:
                if i > 0:
                    _query += " OR "

                _query += field + " LIKE '%%" + arg + "%%'"
                #args_to_append.append(arg)
                i = i + 1

            _query += """)"""

        _query += " LIMIT " + start + "," + end

        #args_to_append.append(start)
        #args_to_append.append(end)

        credits = Credit.objects.raw(_query, args_to_append)

        # Query to obtain total count
        _query = """SELECT * FROM main_credit WHERE 1"""

        for arg in search:
            _query += """ AND ("""

            i = 0

            for field in fields:
                if i > 0:
                    _query += " OR "

                _query += field + " LIKE '%%" + arg + "%%'"
                #args_to_append.append(arg)
                i = i + 1

            _query += """)"""

        count = len(list(Credit.objects.raw(_query, args_to_append)))
        for credit in credits:
            aaData.append([
                '$%s' % str(credit.amount),
                credit.cancel_reason,
                credit.supposed_by,
                credit.entity,
                credit.sector,
            ])

    else:
        credits = Credit.objects.all()
        count = credits.count()

        for credit in credits[start:end]:
            aaData.append([
                '$%s' % str(credit.amount),
                credit.cancel_reason,
                credit.supposed_by,
                credit.entity,
                credit.sector,
            ])

    data = {
        'iTotalRecords': count,
        'iDisplayStart': start,
        'iDisplayLength': display_length,
        'iTotalDisplayRecords': count,
        'aaData':aaData
    }
    return HttpResponse(json.dumps(data))

def graph(request):
    '''
    Show graph page
    '''
    return render_to_response('graph.html', RequestContext(request))

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