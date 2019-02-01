from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import EventSerializer
from .models import Event

class EventsAPIView(APIView):
  
  def get(self, request):
    """
    Return upcoming events
    """
    
    now = datetime.today()
    queryset = Event.objects.filter(start_time__gte=now)
    queryset = queryset.order_by('start_time')
    
    serializer = EventSerializer(queryset, many=True)
    return Response(serializer.data)