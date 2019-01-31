from django.contrib import admin
from events.models import Event, Artist
import datetime
import calendar
from django.urls import reverse
from django.utils.safestring import mark_safe
from events.utils import EventCalendar

class EventAdmin(admin.ModelAdmin):
  
  list_display = [
    'start_time', 
    'end_time', 
    'artist', 
    'notes'
  ]

  change_list_template = 'admin/events/change_list.html'

  def get_first_day(self, d, day=1, next_month=True):
    
    month = datetime.date(
      year=d.year,
      month=d.month,
      day=day)  # find first day of month
    
    if not next_month:
      month = month - datetime.timedelta(days=1)
    else:
      month = month + datetime.timedelta(days=1)
    
    month = datetime.date(
      year=month.year, 
      month=month.month,
      day=1)  # find first day of month
    
    return month

  def changelist_view(self, request, extra_context=None):
    
    after_day = request.GET.get('start_time__gte', None)
    extra_context = extra_context or {}

    # If date not passed or invalid date, use today
    if not after_day:
      d = datetime.date.today()
    else:
      try:
        split_after_day = after_day.split('-')
        d = datetime.date(
          year=int(split_after_day[0]), 
          month=int(split_after_day[1]), 
          day=1)
      except:
        d = datetime.date.today()

    # Get previous and next month
    last_day = calendar.monthrange(d.year, d.month)
    previous_month = self.get_first_day(d, 1, False)   
    next_month = self.get_first_day(d, last_day[1], True)
    
    # Get links to buttons (next/previous month)
    reverse_url = 'admin:events_event_changelist'
    extra_context['previous_month'] = reverse(reverse_url) + '?start_time__gte=' + str(previous_month)
    extra_context['next_month'] = reverse(reverse_url) + '?start_time__gte=' + str(next_month)
    
    cal = EventCalendar()
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    extra_context['calendar'] = mark_safe(html_calendar)

    return super(EventAdmin, self).changelist_view(request, extra_context)

admin.site.register(Event, EventAdmin)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Artist, ArtistAdmin)