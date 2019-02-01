from rest_framework import serializers
from .models import Event, Artist

class ArtistSerializer(serializers.ModelSerializer):
  """
  Artist serializer
  """
  class Meta:
    model = Artist
    fields = ('id', 'name',)

class EventSerializer(serializers.ModelSerializer):
  """
  Event serializer
  """
  artist = ArtistSerializer(many=False, read_only=True)

  class Meta:
    model = Event
    fields = ('id', 'start_time', 'end_time', 'artist',)