from django.urls import path
from tickets.views import ( TicketListView, TicketDetailView, TicketUpdateView, TicketCreateView, TicketAssignView, add_comment, RoleBasedDashboardView ) 
from django.contrib.auth.views import LoginView, LogoutView
from tickets.admin import admin
from tickets import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', RoleBasedDashboardView.as_view(), name='dashboard'),

    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/new/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/update/', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/assign/', views.TicketAssignView.as_view(), name='ticket-assign'),
    path('tickets/<int:pk>/comment/', views.add_comment, name='ticket-comment'),
]