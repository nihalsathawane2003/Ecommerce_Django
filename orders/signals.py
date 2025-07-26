
# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from products.models import Product
from django.core.mail import send_mail

@receiver(post_save, sender=OrderItem)
def reduce_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock -= instance.quantity
        product.save()

@receiver(post_save, sender=OrderItem)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        order = instance.order
        user_email = order.user.email
        send_mail(
            subject='Your order has been placed!',
            message=f'Thank you for your purchase. Your order #{order.id} has been confirmed.',
            from_email='noreply@ecommerce.com',
            recipient_list=[user_email],
            fail_silently=True
        )
