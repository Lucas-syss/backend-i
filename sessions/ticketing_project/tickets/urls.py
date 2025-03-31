from django.contrib.auth.views import LoginView, LogoutView
from tickets import views
from django.urls import path
from tickets.views import (
    TicketListView, TicketDetailView, TicketUpdateView,
    TicketCreateView, TicketAssignView,
    RoleBasedDashboardView, AddCommentView, CustomerSignUpView, AdminCreateAgentView, logout_view
)

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # Dashboards (role-based)
    path('dashboard/', RoleBasedDashboardView.as_view(), name='dashboard'),
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='admin-dashboard'),  
    path('dashboard/agent/', views.AgentDashboardView.as_view(), name='agent-dashboard'),
    path('dashboard/customer/', TicketListView.as_view(), name='customer-dashboard'),
    # Tickets
    
    path('customer/dashboard/create', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('tickets/<int:pk>/comment/', AddCommentView.as_view(), name='ticket-comment'),
    
    # Customer Sign-Up and Admin-Only Views
    path('signup/', CustomerSignUpView.as_view(), name='customer-signup'),
    path('create-agent/admin/', AdminCreateAgentView.as_view(), name='admin-create-agent'),
]