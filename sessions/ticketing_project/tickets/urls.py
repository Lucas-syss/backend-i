from django.urls import path
from tickets.views import (
    TicketListView, TicketDetailView, TicketUpdateView,
    TicketCreateView, TicketAssignView, add_comment,
    RoleBasedDashboardView,
    AdminDashboardView, AgentDashboardView  # Add these new views if needed
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.admin.views.decorators import staff_member_required
from tickets import views

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dashboards (role-based)
    path('dashboard/', RoleBasedDashboardView.as_view(), name='dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),  # Add this view
    path('agent-dashboard/', views.AgentDashboardView.as_view(), name='agent-dashboard'),  # Add this view

    # Tickets
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('tickets/<int:pk>/comment/', add_comment, name='ticket-comment'),
]