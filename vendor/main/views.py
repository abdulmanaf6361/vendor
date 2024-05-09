# Import necessary modules
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

class TokenBasedPermission(IsAuthenticated):
    """
    Custom permission class to require token authentication.
    """
    authentication_classes = [TokenAuthentication]

# Vendor API endpoints
class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Purchase Order API endpoints
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



from django.db.models import Avg, Count,F
from django.utils import timezone
from .models import Vendor, PurchaseOrder

from datetime import timedelta

def calculate_vendor_performance_metrics(vendor):
    try:
        completed_orders = vendor.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        print(total_completed_orders)
        
        # Calculate on-time delivery rate
        # Count the number of completed POs delivered on or before delivery_date
        on_time_deliveries = completed_orders.filter(issue_date__lte=F('delivery_date')).count()
        total_completed_orders = completed_orders.count()
        # Calculate the on-time delivery rate
        if total_completed_orders > 0:
            on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100
        else:
            on_time_delivery_rate = 0.0
        # Assign the calculated on-time delivery rate to the vendor's on_time_delivery_rate field
        vendor.on_time_delivery_rate = on_time_delivery_rate

        
        # Calculate quality rating average
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).aggregate(quality_rating_avg=Avg('quality_rating'))
        vendor.quality_rating_avg = quality_ratings['quality_rating_avg'] if quality_ratings['quality_rating_avg'] else 0.0
    
        # Calculate average response time (in days)
        acknowledged_orders = completed_orders.exclude(acknowledgment_date__isnull=True)
        if acknowledged_orders.exists():
            total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in acknowledged_orders)
            average_response_time_seconds = total_response_time / acknowledged_orders.count()
            vendor.average_response_time = average_response_time_seconds / (60 * 60 * 24)  # Convert seconds to days
        else:
            vendor.average_response_time = 0.0
    
        # Calculate fulfillment rate
        total_orders_by_vendor = vendor.purchaseorder_set.count()
        if total_orders_by_vendor > 0 and total_completed_orders>0:
            vendor.fulfillment_rate = (total_completed_orders / total_orders_by_vendor) * 100
        else:
            vendor.fulfillment_rate = 0.0
        
        # Save changes to the vendor
        vendor.save()
    except Exception as e:
        print(f"An error occurred while calculating vendor performance metrics: {e}")


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer

class VendorPerformanceAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Return calculated performance metrics for the vendor
        performance_data = {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate
        }
        return Response(performance_data)



class AcknowledgePurchaseOrderAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update acknowledgment date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Recalculate average response time
        calculate_vendor_performance_metrics(purchase_order.vendor)

        return Response({"message": "Purchase order acknowledged successfully"})
