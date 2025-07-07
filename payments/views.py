from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import uuid
import qrcode
import io
import base64
from .models import Payment, PaymentMethod, UPIPayment, Invoice
from logo_generator.models import LogoRequest

def payment_methods(request):
    methods = PaymentMethod.objects.filter(is_active=True)
    return render(request, 'payments/methods.html', {'methods': methods})

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        logo_request = get_object_or_404(LogoRequest, id=data['logo_request_id'])
        
        payment = Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            logo_request=logo_request,
            amount=settings.PAYMENT_SETTINGS['logo_price'],
            currency=settings.PAYMENT_SETTINGS['currency'],
            payment_method_id=data['payment_method_id']
        )
        
        return JsonResponse({
            'success': True,
            'payment_id': str(payment.id),
            'amount': float(payment.amount),
            'upi_id': settings.PAYMENT_SETTINGS['upi_id']
        })
    
    return JsonResponse({'success': False})

def generate_upi_qr(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    upi_string = f"upi://pay?pa={settings.PAYMENT_SETTINGS['upi_id']}&pn=Hiren Patel&am={payment.amount}&cu=INR&tn=Logo for {payment.logo_request.company_name}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_string)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return JsonResponse({
        'qr_code': f"data:image/png;base64,{img_str}",
        'upi_string': upi_string
    })

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        payment = get_object_or_404(Payment, id=data['payment_id'])
        
        # In a real implementation, you would verify with payment gateway
        payment.transaction_id = data.get('transaction_id', '')
        payment.upi_transaction_id = data.get('upi_transaction_id', '')
        payment.status = 'completed'
        payment.save()
        
        # Mark logo request as paid
        payment.logo_request.is_paid = True
        payment.logo_request.save()
        
        # Generate invoice
        create_invoice(payment)
        
        return JsonResponse({
            'success': True,
            'message': 'Payment verified successfully'
        })
    
    return JsonResponse({'success': False})

def create_invoice(payment):
    invoice_number = f"INV-{payment.id.hex[:8].upper()}"
    
    Invoice.objects.create(
        payment=payment,
        invoice_number=invoice_number,
        customer_name=payment.user.get_full_name() if payment.user else 'Guest',
        customer_email=payment.user.email if payment.user else '',
        customer_phone=settings.BUSINESS_INFO['phone'],
        customer_address=f"From: {settings.BUSINESS_INFO['address']}",
        subtotal=payment.amount,
        tax_amount=0,
        total_amount=payment.amount
    )

@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/history.html', {'payments': payments})

def pricing(request):
    return render(request, 'payments/pricing.html', {
        'logo_price': settings.PAYMENT_SETTINGS['logo_price'],
        'business_info': settings.BUSINESS_INFO
    })

def invoice_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    invoice = get_object_or_404(Invoice, payment=payment)
    
    return render(request, 'payments/invoice.html', {
        'invoice': invoice,
        'business_info': settings.BUSINESS_INFO
    })