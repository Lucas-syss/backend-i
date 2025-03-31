import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import Ticket, Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, logout
from .forms import AgentCreationForm, CustomerSignUpForm

# Set up logging
logger = logging.getLogger(__name__)

class RoleBasedDashboardView(LoginRequiredMixin, View):
    """Redirects users to their respective dashboards based on role."""
    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} is attempting to access dashboard.")
        if request.user.is_superuser:
            return redirect(reverse('admin-dashboard'))
        elif request.user.is_staff:
            return redirect(reverse('agent-dashboard'))
        if request.user.role == 'customer':  
            return redirect(reverse('customer-dashboard'))
        return redirect(reverse('login'))  

def logout_view(request):
    logger.info(f"User {request.user.username} logged out.")
    logout(request)
    return redirect(reverse('login'))

class AdminDashboardView(LoginRequiredMixin, ListView):
    """Admin Dashboard View"""
    model = Ticket
    template_name = 'tickets/admin_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} is accessing admin dashboard.")
        if not request.user.is_superuser:
            if request.user.is_staff:
                return redirect('agent-dashboard')
            elif request.user.role == 'customer':
                return redirect('customer-dashboard')
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        logger.debug("Fetching all tickets for admin.")
        return Ticket.objects.all()  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.get_queryset()
        return context
    
class AgentDashboardView(LoginRequiredMixin, View):
    """Agent Dashboard View"""
    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} is accessing agent dashboard.")
        if not request.user.is_staff or request.user.is_superuser: 
            return redirect('dashboard')  
            
        tickets = Ticket.objects.filter(assigned_to=self.request.user)
        return render(request, 'tickets/agent_dashboard.html', {'tickets': tickets})

class TicketListView(LoginRequiredMixin, ListView):
    """Displays tickets based on user role."""
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    
    def get_queryset(self):
        logger.debug(f"User {self.request.user.username} is viewing tickets.")
        if self.request.user.is_superuser:
            return Ticket.objects.all()  
        elif self.request.user.is_staff:
            return Ticket.objects.filter(assigned_to=self.request.user)  
        return Ticket.objects.filter(user=self.request.user) 
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin-dashboard') 
        elif request.user.is_staff:
            return redirect('agent-dashboard')  
        return super().dispatch(request, *args, **kwargs)

class TicketCreateView(LoginRequiredMixin, CreateView):
    """Only customers can create tickets."""
    model = Ticket
    fields = ['subject', 'description'] 
    template_name = 'tickets/ticket_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_staff or request.user.is_superuser:
            logger.warning(f"User {request.user.username} attempted to create a ticket but is not authorized.")
            raise PermissionDenied("Only customers can create tickets.")
        return super().dispatch(request, *args, **kwargs)
        
    def get_success_url(self):
        logger.info(f"Ticket created successfully by user {self.request.user.username}.")
        return reverse('customer-dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        logger.info(f"Ticket form valid for user {self.request.user.username}.")
        return super().form_valid(form)

class TicketDetailView(LoginRequiredMixin, DetailView):
    """All authenticated users can view tickets, but with role-based context."""
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.request.user.is_staff or self.request.user.is_superuser
        return context

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """Only agents can update ticket status."""
    model = Ticket
    fields = ['status']  
    template_name = 'tickets/ticket_update_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logger.warning(f"User {request.user.username} attempted to update a ticket but is not authorized.")
            raise PermissionDenied("Only agents can update tickets.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        logger.info(f"Ticket {self.object.pk} updated successfully.")
        return reverse('ticket-detail', kwargs={'pk': self.object.pk})

class TicketAssignView(LoginRequiredMixin, UpdateView):
    """Only admins can assign agents to tickets."""
    model = Ticket
    fields = ['assigned_to']
    template_name = 'tickets/ticket_assign.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            logger.warning(f"User {request.user.username} attempted to assign tickets but is not authorized.")
            raise PermissionDenied("Only admins can assign tickets.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        form = super().get_form()
        if self.request.user.is_superuser:
            User = get_user_model()
            form.fields['assigned_to'].queryset = User.objects.filter(role='agent', is_staff=True)
        return form
    
    def get_success_url(self):
        logger.info(f"Ticket {self.object.pk} assigned successfully.")
        return reverse('admin-dashboard')

class AddCommentView(LoginRequiredMixin, View):
    """Allow agents to leave comments on tickets."""
    def get(self, request, pk, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=pk)
        logger.info(f"User {request.user.username} is viewing ticket {pk}.")
        return render(request, 'tickets/ticket_detail.html', {'object': ticket})

    def post(self, request, pk, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=pk)
        if not request.user.is_staff:
            logger.warning(f"User {request.user.username} attempted to comment on ticket {pk} but is not authorized.")
            return HttpResponseForbidden("Only agents can comment on tickets.")
        
        comment_text = request.POST.get('comment')
        is_internal = 'internal' in request.POST  
        if comment_text:
            Comment.objects.create(
                ticket=ticket,
                user=request.user,
                text=comment_text,
                is_internal=is_internal
            )
            logger.info(f"User {request.user.username} added a comment to ticket {pk}.")
        return redirect('ticket-detail', pk=ticket.pk)

class CustomerSignUpView(CreateView):
    """Allow customers to sign up."""
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        user.is_staff = False  
        logger.info(f"New customer user {user.username} created successfully.")
        return redirect('login')

class AdminCreateAgentView(LoginRequiredMixin, View):
    """Allow admins to create agent accounts."""
    
    def get(self, request):
        if not request.user.is_superuser:
            logger.warning(f"User {request.user.username} attempted to create an agent but is not authorized.")
            raise PermissionDenied("Only admins can create agents.")
        form = AgentCreationForm()
        return render(request, 'tickets/admin_create_agent.html', {'form': form})

    def post(self, request):
        if not request.user.is_superuser:
            logger.warning(f"User {request.user.username} attempted to create an agent but is not authorized.")
            raise PermissionDenied("Only admins can create agents.")
        form = AgentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"New agent created by user {request.user.username}.")
            return redirect('admin-dashboard')
        return render(request, 'tickets/admin_create_agent.html', {'form': form})
