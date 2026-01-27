from django.urls import path
from .views import DashboardView, GadgetCreateView, GadgetDetailView, GadgetVoteView
app_name = 'challenges'

urlpatterns = [
    # A főoldal (HTML)
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Az API végpont a létrehozáshoz (JSON)
    path('api/create/', GadgetCreateView.as_view(), name='gadget-create'),
    path('gadget/<slug:slug>/', GadgetDetailView.as_view(), name='detail'),
    path('gadget/<int:pk>/vote/', GadgetVoteView.as_view(), name='gadget-vote'),
]