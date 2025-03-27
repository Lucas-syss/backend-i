from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment

class RoleBasedDashboardView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin-dashboard')
        elif request.user.groups.filter(name='Agents').exists():
            return redirect('agent-dashboard')
        return redirect('ticket-list')

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/customer_dashboard.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Ticket.objects.all()
        elif self.request.user.groups.filter(name='Agents').exists():
            return Ticket.objects.filter(assigned_to=self.request.user)
        return Ticket.objects.filter(user=self.request.user)

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['subject', 'description', 'priority']
    template_name = 'tickets/ticket_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['status', 'assigned_to']
    template_name = 'tickets/ticket_update_form.html'

class TicketAssignView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['assigned_to']
    template_name = 'tickets/ticket_assign.html'
    
    def get_success_url(self):
        return reverse('admin-dashboard')

@login_required
def add_comment(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        Comment.objects.create(
            ticket=ticket,
            user=request.user,
            text=request.POST.get('comment'),
            is_internal=not request.user.is_superuser
        )
    return redirect('ticket-detail', pk=pk)