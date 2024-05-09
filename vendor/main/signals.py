from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder
from .views import calculate_vendor_performance_metrics

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics_on_save(sender, instance, **kwargs):
    # Call the calculate_vendor_performance_metrics function whenever a PurchaseOrder is saved
    calculate_vendor_performance_metrics(instance.vendor)

@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_performance_metrics_on_delete(sender, instance, **kwargs):
    # Call the calculate_vendor_performance_metrics function whenever a PurchaseOrder is deleted
    calculate_vendor_performance_metrics(instance.vendor)
