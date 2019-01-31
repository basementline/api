from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class Artist(models.Model):
  """
  Model for artist
  """
  name = models.CharField(max_length=250, 
    null=False, 
    help_text=u'Artistname, max 250 chars length')

  def __str__(self):
    return self.name

class Event(models.Model):
  """
  Model for events
  """
  start_time = models.DateTimeField('Starting time', 
    help_text=u'Starting time')
  end_time = models.DateTimeField('Ending time', 
    help_text=u'Ending time')
  notes = models.TextField('Show notes', 
    help_text=u'Setlist, etc.', 
    blank=True, 
    null=True)
  artist = models.ForeignKey(Artist, 
    on_delete=models.CASCADE, 
    null=False, 
    related_name='events')

  def __str__(self):
    return self.artist.name

  class Meta:
    verbose_name = 'Calendar'
    verbose_name_plural = 'Calendar'

  def get_cal_url(self):
    """
    Returns HTML link to calendar event
    """
    url = reverse('admin:%s_%s_change' % (self._meta.app_label, 
      self._meta.model_name), args=[self.id])

    start_time = self.start_time.strftime('%H:%M')
    end_time = self.end_time.strftime('%H:%M')

    return '<a href="%s">%s (%s-%s)</a>' % (url, self.artist.name, start_time, end_time)

  def clean(self):
    """
    Validate event time
    """
    if self.end_time <= self.start_time:
      raise ValidationError('Ending hour must be after the starting hour')

    # TODO: does not work.
    events = Event.objects.filter(
      end_time__gte=self.start_time, 
      end_time__lte=self.end_time)

    if events.exists():
      event = events.first()
      raise ValidationError('There is an overlap with another event: %s-%s' % (str(event.start_time), str(event.end_time)))
