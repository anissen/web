from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^OmTK.php$',
        RedirectView.as_view(url='/om/', permanent=True), ),

    url(r'^BESTFU.php',
        RedirectView.as_view(url='/bestfu/', permanent=True), ),

    url(r'^Kalender.php',
        RedirectView.as_view(url='/kalender/', permanent=True), ),

    url(r'^Arrangementer.php',
        RedirectView.as_view(url='/arrangementer/', permanent=True), ),

    url(r'^Kontakt.php',
        RedirectView.as_view(url='/kontakt/', permanent=True), ),

    url(r'^Login.php',
        RedirectView.as_view(url='/admin/', permanent=True), ),

    url(r'^Billeder/index.php',
        RedirectView.as_view(url='/galleri/', permanent=True), ),
]
