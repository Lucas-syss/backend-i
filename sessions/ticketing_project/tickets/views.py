from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Ticket, Comment

# --- Utility Functions for Role Checks ---
def is_customer(user):
    return user.is_authenticated and user.role == 'customer'

def is_agent(user):
    return user.is_authenticated and user.role == 'agent'

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# --- Views ---
class RoleBasedDashboardView(LoginRequiredMixin, View):
    """Redirects users to their respective dashboards based on role."""
    def get(self, request, *args, **kwargs):
        if is_admin(request.user):
            return redirect('admin-dashboard')
        elif is_agent(request.user):
            return redirect('agent-dashboard')
        return redirect('ticket-list') 

class TicketListView(LoginRequiredMixin, ListView):
    """Displays tickets based on user role."""
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    
    def get_queryset(self):
        if is_admin(self.request.user):
            return Ticket.objects.all()
        elif is_agent(self.request.user):
            return Ticket.objects.filter(assigned_to=self.request.user)
        return Ticket.objects.filter(user=self.request.user)  

class TicketCreateView(LoginRequiredMixin, CreateView):
    """Only customers can create tickets."""
    model = Ticket
    fields = ['subject', 'description', 'priority']
    template_name = 'tickets/ticket_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not is_customer(request.user):
            raise PermissionDenied("Only customers can create tickets.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TicketDetailView(LoginRequiredMixin, DetailView):
    """All authenticated users can view tickets, but with role-based context."""
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = is_admin(self.request.user) or is_agent(self.request.user)
        return context

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """Only agents/admins can update ticket status."""
    model = Ticket
    fields = ['status', 'assigned_to']
    template_name = 'tickets/ticket_update_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (is_agent(request.user) or is_admin(request.user)):
            raise PermissionDenied("Only agents/admins can update tickets.")
        return super().dispatch(request, *args, **kwargs)

class TicketAssignView(LoginRequiredMixin, UpdateView):
    """Only admins can assign agents to tickets."""
    model = Ticket
    fields = ['assigned_to']
    template_name = 'tickets/ticket_assign.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied("Only admins can assign tickets.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('admin-dashboard')

@login_required
def add_comment(request, pk):
    """Agents/admins can post internal comments; customers post public ones."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        Comment.objects.create(
            ticket=ticket,
            user=request.user,
            text=request.POST.get('comment'),
            is_internal=not is_customer(request.user)  
        )
    return redirect('ticket-detail', pk=pk)