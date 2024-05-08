from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Avg
from datetime import datetime,timezone,timedelta

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True



class Vendors(models.Model):
    name=models.CharField(max_length=100)
    contact_details= models.TextField()
    address= models.TextField()
    vendor_code= models.CharField(max_length=100, unique=True)
    on_time_delivery_rate= models.FloatField(blank=True, null=True)
    quality_rating_avg= models.FloatField(blank=True, null=True)
    average_response_time= models.FloatField(blank=True, null=True) 
    fulfillment_rate= models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class PurchaseOrders(models.Model):
    po_number = models.CharField(max_length=100, unique=True, primary_key=True,
                                 help_text="system generated Po number")
    vendor = models.ForeignKey(Vendors, on_delete= models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, blank=True, null=True)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    response_time = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    on_time_delivery = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        
        format_string = "%Y-%m-%d %H:%M:%S"
        if self.issue_date and self.acknowledgment_date:
            acknowledgement_date= datetime.strptime(str(self.acknowledgment_date)[:19], format_string)
            issue_date = datetime.strptime(str(self.issue_date)[:19], format_string)
            response_time = (acknowledgement_date - issue_date).total_seconds()
            self.response_time = response_time / 3600
  
        if self.status == "completed":
            if self.delivery_date == None:
                self.delivery_date = datetime.now()
                self.on_time_delivery = True
            elif datetime.strptime(str(self.delivery_date)[:19], format_string) <= datetime.now():
                self.on_time_delivery = True
        else:
            self.quality_rating = 0

        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.po_number

class HistorialPerformance(BaseModel):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    on_time_delivery_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quality_rating_avg = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    average_response_time = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fulfillment_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.vendor.name
    

@receiver(post_save, sender= PurchaseOrders)
def update(sender, instance, **kwargs):
        
    vendor = instance.vendor

    if vendor.on_time_delivery_rate or vendor.quality_rating_avg or vendor.average_response_time or vendor.fulfillment_rate:

        HistorialPerformance.objects.create(vendor=vendor, on_time_delivery_rate=vendor.on_time_delivery_rate,
                                        quality_rating_avg=vendor.quality_rating_avg, average_response_time=vendor.average_response_time,
                                        fulfillment_rate=vendor.fulfillment_rate)
    
    avg_response_time = PurchaseOrders.objects.filter(vendor=vendor.id, acknowledgment_date__isnull=False).aggregate(avg_response_time=Avg('response_time'))
    vendor.average_response_time = avg_response_time['avg_response_time']
    completed = PurchaseOrders.objects.filter(vendor=vendor.id, status="completed").count()

    total_orders = PurchaseOrders.objects.filter(vendor=vendor.id).count()

    vendor.fulfillment_rate = completed / total_orders * 100
    quality_rating = PurchaseOrders.objects.filter(vendor=vendor.id, status="completed").aggregate(rating_avg=Avg('quality_rating'))
    vendor.quality_rating_avg = round(quality_rating['rating_avg'],4)
    if completed:
        on_time_delivery = PurchaseOrders.objects.filter(vendor=vendor.id, on_time_delivery=True).count()
        print ("on_time_delivery",on_time_delivery)
        print (completed)
        vendor.on_time_delivery_rate = round(on_time_delivery / completed,4) * 100

    vendor.save()