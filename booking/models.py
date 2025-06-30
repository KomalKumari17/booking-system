from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('user', 'day_of_week', 'start_time', 'end_time')
        ordering = ['user', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.user.username} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()

    class Meta:
        unique_together = ('user', 'date', 'start_time', 'end_time')
        ordering = ['user', 'date', 'start_time']

    def __str__(self):
        return f"{self.guest_name} booked {self.user.username} on {self.date} {self.start_time}-{self.end_time}"
