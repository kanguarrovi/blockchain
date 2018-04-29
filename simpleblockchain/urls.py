from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from simpleblockchain import views

urlpatterns = [
    path('mine', views.MinningView.as_view()),
    path('transactions/new', views.Transaction.as_view()),
    path('chain', views.FullChainView.as_view()),
    path('nodes/register', views.RegisterNodesView.as_view()),
    path('nodes/resolve', views.ConsensusView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
