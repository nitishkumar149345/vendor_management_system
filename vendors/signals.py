from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import *


@receiver(post_save, sender=PurchaseOrders)
def update_vendor_avg_response_time(sender, instance, **kwargs):
    print ("signla triggred")
    vendor = instance.vendor
    print (vendor)
    if vendor.on_time_delivery_rate or vendor.quality_rating_avg or vendor.average_response_time or vendor.fulfillment_rate:
        HistorialPerformance.objects.create(vendor=vendor, on_time_delivery_rate=vendor.on_time_delivery_rate,
                                        quality_rating_avg=vendor.quality_rating_avg, average_response_time=vendor.average_response_time,
                                        fulfillment_rate=vendor.fulfillment_rate)
    
    avg_response_time = PurchaseOrders.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(avg_response_time=Avg('response_time'))
    vendor.average_response_time = avg_response_time['avg_response_time']
    completed = PurchaseOrders.objects.filter(vendor=vendor, status="Completed").count()
    total_orders = PurchaseOrders.objects.filter(vendor=vendor).count()
    vendor.fulfillment_rate = completed / total_orders * 100
    quality_rating = PurchaseOrders.objects.filter(vendor=vendor, status="Completed").aggregate(rating_avg=Avg('quality_rating'))
    vendor.quality_rating_avg = quality_rating['rating_avg']
    if completed:
        on_time_delivery = PurchaseOrders.objects.filter(vendor=vendor, on_time_delivery=True).count()
        vendor.on_time_delivery_rate = on_time_delivery / completed * 100

    vendor.save()