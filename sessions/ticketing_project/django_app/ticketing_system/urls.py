from django.urls import path
from tickets.views import TicketListView, TicketDetailView, TicketUpdateView
from tickets.admin import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
]