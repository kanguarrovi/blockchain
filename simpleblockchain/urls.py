from django.urls import path
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from simpleblockchain import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='chain', permanent=False)),
    path('mine', views.MinningView.as_view(), name='chain'),
    path('transactions/new', views.TransactionView.as_view()),
    path('chain', views.FullChainView.as_view()),
    path('nodes/register', views.RegisterNodesView.as_view()),
    path('nodes/resolve', views.ConsensusView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
