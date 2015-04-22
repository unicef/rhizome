from django.contrib.auth.models import User,Group
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views import generic
from django.contrib.auth.models import User,Group
from django.template import RequestContext

import re
import itertools
import json

DEFAULT_LIMIT = 50
MAX_LIMIT = 500

USER_METADATA = 'static/users_metadata_mockup.json'

class MyUser:
    def __init__(self, pk):
        __auth_user = User.objects.get(pk=pk)
        self.pk = pk
        self.first_name = __auth_user.first_name
        self.last_name = __auth_user.last_name
        __groups_raw = Group.objects.raw('''
            SELECT ag.id, ag.name
                FROM auth_user au 
                    JOIN auth_user_groups aug
                        ON au.id = aug.user_id 
                    JOIN auth_group ag 
                        ON ag.id = aug.group_id
                WHERE au.id = %s;
            ''', (pk,))
        self.groups = [ Group.objects.get(pk=g.id) for g in __groups_raw ]

    def get_dict(self):
        s = {}
        s['groups'] = [ {'value': g.pk, 'label': g.name } for g in self.groups ]
        s['id'] = self.pk
        s['first_name'] = self.first_name
        s['last_name'] = self.last_name
        return s

    def serialize(self):
        return json.dumps(self.get_dict())

def api_user_mock(request):
    ''' send mock meta data out '''
    with open(USER_METADATA, 'r') as f:
        mockup = f.read()
        mockup = mockup.replace('\n', '')\
            .replace('\t', '')\

    return HttpResponse(mockup\
        , content_type="application/json")

def _user_search(users, keywords):
    ''' search is AND-wise but can easily be changed to OR-wise '''
    for k in keywords:
        found = []
        for obj in users:
            data = MyUser(pk=obj.pk).serialize().lower()
            if data.find(k) > -1:
                found.append(obj.pk)
        users = users.filter(pk__in=found)
    return users

def find_group(g, user):
    ''' return True if MyUser user is in group g (soft)'''
    for groups in user.groups:
        if group['label'].find(g) > -1:
            return True
    return False

def is_group(g, user):
    ''' return True if MyUser is in group g (hard)'''
    for group in user.groups:
        if group.name == g:
            return True
    return False

def _user_filter(users, terms, val):
    relation_map = {'eq': 'exact', 'lt': 'lt', 'lte': 'lte', 'gt': 'gt', 'gte': 'gte', 'in': 'in'}
    var = terms[1]
    res = []
    rel = relation_map[terms[2]]
    if rel == 'in':
        vals = val.split(',')
    if var in ['first_name', 'last_name', 'id']:
        kwargs = {
            "{0}__{1}".format(var, rel) : val
        }
        res = users.filter(**kwargs)
    if var == 'group':
        my_users = [ MyUser(pk=u.pk) for u in users ]
        if rel == 'contains':
            my_users = itertools.ifilter(lambda mu: find_group(val, mu), my_users)
            res = users.filter(pk__in=[ mu.pk for mu in my_users ])
        if rel == 'exact':
            my_users = itertools.ifilter(lambda mu: is_group(val, mu), my_users)
            res = users.filter(pk__in=[ mu.pk for mu in my_users ])
        elif rel == 'in':
            found = []
            for v in vals:
                filt = itertools.ifilter(lambda mu: is_group(v, mu), my_users)
                for mu in filt:
                    if mu.pk not in found:
                        found.append(mu.pk)
            res = users.filter(pk__in=found)
    return res

def _user_sort(users, sort_on, sort_direction='asc'):
    sortables = ['first_name', 'last_name']
    if sort_on not in sortables:
        raise Exception("Cannot sort on unordered field")
    if sort_direction.lower() == 'desc':
        sort_on = '-'+sort_on
    res = users.order_by(sort_on)
    return res


def api_user(request):

    users = User.objects.all()
    for (k,v) in request.GET.iteritems():
        verb = k.split('.')[0]
        if verb == 'search':
            keywords = re.split('(?<!\\\)\ ', v.lower())
            users = _user_search(users, keywords)
        elif verb == 'filter':
            terms = k.split('.')
            users = _user_filter(users, terms, v)
        elif verb == 'sort':
            if 'sort_direction' in request.GET:
                sd = request.GET['sort_direction']
                try:
                    users = _user_sort(users, v, sd)
                except:
                    return HttpResponse({'error': 'Cannot Sort on Field'})
            else:
                users = _user_sort(users, v)
    if 'sort' not in request.GET:
        users = _user_sort(users, 'last_name', 'asc')
    offset = 0
    if 'offset' in request.GET:
        offset = int(request.GET['offset'])
    limit = DEFAULT_LIMIT
    if 'limit' in request.GET:
        limit = int(request.GET['limit'])
    my_users = [ MyUser(pk=u.id).get_dict() for u in users ]
    my_users = my_users[offset:offset+limit]
    total_count = len(my_users)
    resp = {}
    resp['error'] = None
    resp['meta'] = {
        'limit': limit,
        'offset': offset,
        'total_count': total_count
    }
    resp['objects'] = my_users
    resp['requested_params'] = [ {k: v} for (k,v) in request.GET.iteritems()]
    return HttpResponse(json.dumps(resp),
            content_type='application/json')