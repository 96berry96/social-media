from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes, permission_classes

from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def notifications(request):
    received_notifications = Notification.objects.filter(is_read=False, created_for=request.user)
    serializer = NotificationSerializer(received_notifications, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def read_notifications(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'message':'notification read'})