# encoding: utf8
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.flatpages import views


urlpatterns = [
    # J40
    url(r'^40/resume$',
        views.flatpage, {'url': '/J40/resume/'},
        name='J40resume'),
    url(r'^40/historie$',
        views.flatpage, {'url': '/J40/historie/'},
        name='J40historie'),

    # J50
    url(r'^50/resume',
        views.flatpage, {'url': '/J50/resume/'},
        name='J50resume'),
    url(r'^50/arrangementer$',
        views.flatpage, {'url': '/J50/arrangementer/'},
        name='J50arrangementer'),
    url(r'^50/deltagere$',
        views.flatpage, {'url': '/J50/deltagere/'},
        name='J50deltagere'),

    # J60
    url(r'^60',
        views.flatpage, {'url': '/J60/'},
        name='J60'),
]
