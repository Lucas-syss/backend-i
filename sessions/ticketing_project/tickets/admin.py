from django.contrib import admin
from .models import User, Ticket, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'assigned_to', 'status', 'priority')
    list_filter = ('status', 'priority')
    search_fields = ('subject', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at', 'is_internal')
    list_filter = ('is_internal',)