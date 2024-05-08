from django.urls import path, include
from .views import *
urlpatterns = [
    path('signup',Signup.as_view(), name= "Signup"),
    path('login',Login.as_view(), name='login'),
    path('vendors',CreateVendors.as_view(), name= 'Vendors'),
    path('vendors/<int:vendor_id>',UpdateVendors.as_view(), name="Update_vendor"),
    path('vendors/<int:vendor_id>/performance',VendorPerformance.as_view(), name="vendor_performance"),
    path('purchase_orders',CreatePurchaseOrders.as_view(), name= 'Purchase_order'),
    path('purchase_orders/<str:po_id>',UpdatePurchaseOrders.as_view(), name= 'Update_purchase_order'),
    path('purchase_orders/<str:po_id>/acknowledge',AcknowlodgeOrder.as_view())
]