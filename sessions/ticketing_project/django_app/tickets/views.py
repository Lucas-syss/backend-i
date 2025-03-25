from django.views.generic import ListView, DetailView, UpdateView
from .models import Ticket

class TicketListView(ListView):
    model = Ticket

class TicketDetailView(DetailView):
    model = Ticket

class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ['status', 'assigned_to']
    template_name_suffix = '_update_form'