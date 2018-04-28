from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from simpleblockchain import views

urlpatterns = [
    path('mine', views.mine),
    path('transactions/new', views.new_transaction),
    path('chain', views.full_chain),
    path('nodes/register', views.register_nodes),
    path('nodes/resolve', views.consensus),

]

urlpatterns = format_suffix_patterns(urlpatterns)
