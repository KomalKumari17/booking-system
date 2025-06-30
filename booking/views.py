from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Availability, Booking
from .serializers import AvailabilitySerializer, BookingSerializer
from datetime import datetime, timedelta, time
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db import IntegrityError

# Create your views here.

class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            if isinstance(e, IntegrityError):
                return Response({'error': 'This availability slot already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)
            raise e


@extend_schema(
        parameters=[
            OpenApiParameter(name='user_id', type=int, required=True, location=OpenApiParameter.QUERY, description='User ID'),
        ]
    )
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Booking.objects.filter(user_id=user_id)
        return Booking.objects.none()

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get('user')
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        overlap = Booking.objects.filter(
            user_id=user_id,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()
        if overlap:
            return Response({'error': 'Booking overlaps with an existing booking.'}, status=status.HTTP_400_BAD_REQUEST)
        avail = Availability.objects.filter(
            user_id=user_id,
            day_of_week=datetime.strptime(date, '%Y-%m-%d').weekday(),
            start_time__lte=start_time,
            end_time__gte=end_time
        ).exists()
        if not avail:
            return Response({'error': 'Booking does not fit in user availability.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='user_id', type=int, required=True, location=OpenApiParameter.QUERY, description='User ID'),
            OpenApiParameter(name='date', type=str, required=True, location=OpenApiParameter.QUERY, description='Date in YYYY-MM-DD'),
        ]
    )
    @action(detail=False, methods=['get'], url_path='available_slots')
    def available_slots(self, request):
        user_id = request.query_params.get('user_id')
        date_str = request.query_params.get('date')
        if not user_id or not date_str:
            return Response({'error': 'user_id and date are required.'}, status=400)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = date.weekday()
        availabilities = Availability.objects.filter(user_id=user_id, day_of_week=day_of_week)
        bookings = Booking.objects.filter(user_id=user_id, date=date)
        slot_lengths = [15, 30, 45, 60]  
        slots = []
        for avail in availabilities:
            start = datetime.combine(date, avail.start_time)
            end = datetime.combine(date, avail.end_time)
            current = start
            while current + timedelta(minutes=15) <= end:
                for length in slot_lengths:
                    slot_end = current + timedelta(minutes=length)
                    if slot_end > end:
                        continue
                    overlap = bookings.filter(
                        start_time__lt=slot_end.time(),
                        end_time__gt=current.time()
                    ).exists()
                    if not overlap:
                        slots.append({
                            'start_time': current.time(),
                            'end_time': slot_end.time(),
                            'duration': length
                        })
                current += timedelta(minutes=15)
        return Response(slots)
