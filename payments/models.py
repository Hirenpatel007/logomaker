from django.db import models
from django.contrib.auth.models import User
from logo_generator.models import LogoRequest
import uuid

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo_request = models.ForeignKey(LogoRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, blank=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    upi_transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.id} - ₹{self.amount}"

class UPIPayment(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    reference_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"UPI Payment {self.payment.id}"

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic - ₹299/month'),
        ('pro', 'Pro - ₹599/month'),
        ('enterprise', 'Enterprise - ₹1299/month'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan}"

class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    gst_number = models.CharField(max_length=20, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_number}"