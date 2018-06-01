from django.urls import path
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from simpleblockchain import views

schema_view = get_schema_view(title='Simple blockchain API')

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='chain', permanent=False)),
    path('mine', views.MinningView.as_view()),
    path('transactions/new', views.TransactionView.as_view()),
    path('chain', views.FullChainView.as_view(), name='chain'),
    path('nodes/register', views.RegisterNodesView.as_view()),
    path('nodes/resolve', views.ConsensusView.as_view()),
    path('schema', schema_view, name="schema"),
    path('info', RedirectView.as_view(pattern_name='schema', permanent=False)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
