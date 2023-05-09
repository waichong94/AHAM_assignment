from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Customer
from .serializers import CustomerSerializer

class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_detail = exc.detail.get('phone', [])[0]
            error_message = error_detail if error_detail else 'Unknown validation error'
            return Response({'status': False, 'error': error_message}, status=400)
        return super().handle_exception(exc)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'status': True,
            'message': 'Customer created successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_detail = exc.detail.get('phone', [])[0]
            error_message = error_detail if error_detail else 'Unknown validation error'
            return Response({'status': False, 'error': error_message}, status=400)
        return super().handle_exception(exc)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'status': True,
            'message': 'Customer updated successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'status': True, 
            'message': 'Customer deleted successfully'
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
