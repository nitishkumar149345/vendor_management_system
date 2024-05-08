from rest_framework.views import APIView
from rest_framework.response import Response
from .local_serializers import *
from .models import Vendors, PurchaseOrders
from rest_framework import status
from datetime import datetime, timezone 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


def formatresponse( message, data=None):
        return {"message":message,"data":data}


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class Signup(APIView):
    def post(self, request):
        try:
            data= request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                return Response(formatresponse("User created Successfully",serializer.data),
                                status=status.HTTP_201_CREATED)
            else:
                return Response(formatresponse("Missing required fields", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
                
            
        except Exception as e:
            return Response(formatresponse("Something went wrong", str(e)), status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.data.get("username")
                password = serializer.data.get("password")
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response(formatresponse("Invalied login credential"), status=status.HTTP_404_NOT_FOUND)
                
                token = get_tokens_for_user(user)
                return Response(formatresponse("User logged Successfully",token), status=status.HTTP_200_OK)
            else:
                return Response(formatresponse("Invalied login credential", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(formatresponse("Something went wrong", str(e)), status=status.HTTP_400_BAD_REQUEST)


class CreateVendors(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor= Vendors.objects.all()
        serializer= VendorSerializer(vendor, many=True)
        return Response(("Data",serializer.data), status=status.HTTP_200_OK)
    
    def post(self, request):
        data= request.data
        serializer= VendorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(formatresponse("Data",serializer.data),status=status.HTTP_201_CREATED )
        else:
            return Response(("Missing required fields",serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        
class UpdateVendors(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, vendor_id):
        try:
            vendor= Vendors.objects.get(pk= vendor_id)
            serializer= VendorSerializer(vendor)
            return Response(formatresponse("Data",serializer.data), status=status.HTTP_200_OK)
        except Vendors.DoesNotExist as e:
            return Response(formatresponse("vendor not found",str(e)), status= status.HTTP_404_NOT_FOUND)
        
    def put(self, request, vendor_id):
        try:
            vendor= Vendors.objects.get(pk= vendor_id)
        except Vendors.DoesNotExist as e:
            return Response(formatresponse("vendor not found",str(e)), status=status.HTTP_404_NOT_FOUND)
        
        data= request.data
        serializer= VendorSerializer(vendor, data=data)  

        if serializer.is_valid():
            serializer.save()
            return Response(formatresponse("Data",serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, vendor_id):
        try:
            vendor= Vendors.objects.get(pk= vendor_id)
        except Vendors.DoesNotExist as e:
            return Response(formatresponse("vendor not found", str(e)),status=status.HTTP_404_NOT_FOUND)
        
        vendor.delete()
        return Response(formatresponse("vendor successfully deleted"),status=status.HTTP_200_OK)
        
class CreatePurchaseOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset= PurchaseOrders.objects.all()
        
        serializer= PurchaseOrdersSerializer(queryset, many= True)
        return Response(formatresponse("Data",serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        data= request.data
        serializer= PurchaseOrdersSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(formatresponse("purchase order created",serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(formatresponse("Missing required fields",serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class UpdatePurchaseOrders(APIView):
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def get(self, request, po_id):
        try:
            purchase_order= PurchaseOrders.objects.get(po_number= po_id)
        except PurchaseOrders.DoesNotExist as e:
            return Response(formatresponse("purchase order not found",str(e)),status=status.HTTP_404_NOT_FOUND)
        
        serializer = PurchaseOrdersSerializer(purchase_order)
        return Response(formatresponse("Data",serializer.data), status=status.HTTP_200_OK)
    
    def put(self, request, po_id):
        try:
            purchase_order = PurchaseOrders.objects.get(po_number=po_id)
        except PurchaseOrders.DoesNotExist as e:
            return Response(formatresponse("purchase order not found",str(e)), status=status.HTTP_404_NOT_FOUND)

        data= request.data
        serializer = PurchaseOrdersSerializer(purchase_order, data=data) 

        if serializer.is_valid():
            serializer.save()
            return Response(formatresponse("Data",serializer.data), status=status.HTTP_202_ACCEPTED)
        else:
            return Response(formatresponse("Missing required fields",serializer.errors),status=status.HTTP_400_BAD_REQUEST)   
        
    def delete(self, request, po_id):
        try:
            purchase_order= PurchaseOrders.objects.get(po_number= po_id)
        except PurchaseOrders.DoesNotExist as e:
            return Response(formatresponse("Purchase order is not found",str(e)), status=status.HTTP_404_NOT_FOUND)
        
        purchase_order.delete()
        return Response(formatresponse("vendor successfully deleted"), status=status.HTTP_200_OK)


class VendorPerformance(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request,vendor_id):
        try:
            vendor= Vendors.objects.get(pk= vendor_id)
            serializer= PerformaceSerializer(vendor)
            return Response(formatresponse("Data",serializer.data), status=status.HTTP_302_FOUND)
        
        except Exception as e:
            return Response(formatresponse("Missing required fields",str(e)), status=status.HTTP_400_BAD_REQUEST)
        
class AcknowlodgeOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, po_id):
        try:
            purchaseorder = PurchaseOrders.objects.get(po_number= po_id)
            if purchaseorder.acknowledgment_date:
                return Response(formatresponse("order already acknowledged"), status=status.HTTP_208_ALREADY_REPORTED)
            
            else:
                purchaseorder.acknowledgment_date= datetime.now()
                purchaseorder.save()
                return Response(formatresponse("order acknowledged"), status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(formatresponse("something went worng",str(e)), status=status.HTTP_400_BAD_REQUEST)


            
    



