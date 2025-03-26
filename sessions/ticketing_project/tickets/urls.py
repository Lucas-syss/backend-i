from django.urls import path
from tickets.views import TicketListView, TicketDetailView, TicketUpdateView
from django.contrib.auth.views import LoginView
from tickets.admin import admin
from tickets import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/update/', views.TicketUpdateView.as_view(), name='ticket-update'),
]