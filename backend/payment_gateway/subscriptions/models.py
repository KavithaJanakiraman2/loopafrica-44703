from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

# Create your models here.
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=255, null=True, blank=True)  # Active, Inactive, Expired, Cancelled, Pending
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_created_by', null=True, blank=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscription_last_updated_by')
    last_updated_at = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)

    def __str__(self):
        return f"Subscription for {self.user.username}'s {self.plan} plan" 

class Customer(models.Model):
    email = models.EmailField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.email
    
# class PaymentTransaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     # subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
#     transaction_id = models.CharField(max_length=255, null=True, blank=True)
#     amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
#     # currency = models.CharField(max_length=255, null=True, blank=True)
#     status = models.CharField(max_length=255, null=True, blank=True)
#     reference = models.CharField(max_length=255, null=True, blank=True)
#     # gateway_response = models.TextField(null=True, blank=True)
#     paid_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)
#     last_updated_at = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)
#     last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_last_updated_by')
#     def __str__(self):
#         return f"Payment {self.transaction_id} for {self.user.username}'s subscription"

    