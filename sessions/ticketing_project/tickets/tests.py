from django.test import TestCase, Client
from django.urls import reverse
from tickets.models import User, Ticket, Comment

class TicketingSystemTests(TestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.agent_user = User.objects.create_user(
            username="agent", email="agent@example.com", password="agent123", role="agent", is_staff=True
        )
        self.customer_user = User.objects.create_user(
            username="customer", email="customer@example.com", password="customer123", role="customer"
        )

        # Create a ticket
        self.ticket = Ticket.objects.create(
            subject="Test Ticket",
            description="This is a test ticket.",
            user=self.customer_user,
            status="Open",
            priority="Medium",
        )

        # Create a client for testing
        self.client = Client()

    def test_login_page_accessible(self):
        """Test that the login page is accessible."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_admin_dashboard_access(self):
        """Test that only admin can access the admin dashboard."""
        # Login as admin
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("admin-dashboard"))
        self.assertEqual(response.status_code, 200)

        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.get(reverse("admin-dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to agent dashboard

        # Login as customer
        self.client.login(username="customer", password="customer123")
        response = self.client.get(reverse("admin-dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to customer dashboard

    def test_agent_dashboard_access(self):
        """Test that only agents can access the agent dashboard."""
        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.get(reverse("agent-dashboard"))
        self.assertEqual(response.status_code, 200)

        # Login as admin
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("agent-dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to admin dashboard

        # Login as customer
        self.client.login(username="customer", password="customer123")
        response = self.client.get(reverse("agent-dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to customer dashboard

    def test_customer_dashboard_access(self):
        """Test that only customers can access the customer dashboard."""
        # Login as customer
        self.client.login(username="customer", password="customer123")
        response = self.client.get(reverse("customer-dashboard"))
        self.assertEqual(response.status_code, 200)

        # Login as admin
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("customer-dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to admin dashboard

        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.get(reverse("customer-dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to agent dashboard

    def test_ticket_creation_by_customer(self):
        """Test that only customers can create tickets."""
        # Login as customer
        self.client.login(username="customer", password="customer123")
        response = self.client.post(reverse("ticket-create"), {
            "subject": "New Ticket",
            "description": "This is a new ticket.",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Ticket.objects.count(), 2)

        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.post(reverse("ticket-create"), {
            "subject": "Invalid Ticket",
            "description": "Agents cannot create tickets.",
        })
        self.assertEqual(response.status_code, 403)  # Permission denied

    def test_ticket_update_by_agent(self):
        """Test that only agents can update ticket status."""
        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.post(reverse("ticket-update", args=[self.ticket.pk]), {
            "status": "In Progress",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "In Progress")

        # Login as customer
        self.client.login(username="customer", password="customer123")
        response = self.client.post(reverse("ticket-update", args=[self.ticket.pk]), {
            "status": "Closed",
        })
        self.assertEqual(response.status_code, 403)  # Permission denied

    def test_ticket_assignment_by_admin(self):
        """Test that only admins can assign tickets to agents."""
        # Login as admin
        self.client.login(username="admin", password="admin123")
        response = self.client.post(reverse("ticket-assign", args=[self.ticket.pk]), {
            "assigned_to": self.agent_user.pk,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after assignment
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.agent_user)

        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.post(reverse("ticket-assign", args=[self.ticket.pk]), {
            "assigned_to": self.agent_user.pk,
        })
        self.assertEqual(response.status_code, 403)  # Permission denied

    def test_comment_creation_by_agent(self):
        """Test that only agents can comment on tickets."""
        # Login as agent
        self.client.login(username="agent", password="agent123")
        response = self.client.post(reverse("ticket-comment", args=[self.ticket.pk]), {
            "comment": "This is a test comment.",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after comment
        self.assertEqual(Comment.objects.count(), 1)

        # Login as customer
        self.client.login(username="customer", password="customer123")
        response = self.client.post(reverse("ticket-comment", args=[self.ticket.pk]), {
            "comment": "Customers cannot comment.",
        })
        self.assertEqual(response.status_code, 403)  # Permission denied
