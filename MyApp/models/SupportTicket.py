from django.db import models

class SupportTicket(models.Model):
    TICKET_TYPES = [
        ('Email', 'Email Support'),
        ('Call', 'Call Request'),
        ('Dashboard', 'Dashboard Ticket'),
    ]

    ticket_type = models.CharField(max_length=50, choices=TICKET_TYPES, default='Dashboard')
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()
    
    # Contact Info
    user_name = models.CharField(max_length=100, null=True, blank=True)
    user_contact = models.CharField(max_length=100, null=True, blank=True) # phone or email
    
    status = models.CharField(max_length=50, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.ticket_type}] {self.subject or 'No Subject'} - {self.status}"

    class Meta:
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"
