from rest_framework import serializers

from cinema.exceptions import LogicException
from cinema.models.booking import Booking


class BookingSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ('user_id', 'schedule_id', 'place_id', 'status')

    def create(self, validated_data):
        has_bookings = Booking.objects.filter(schedule_id=validated_data.get('schedule_id'),
                                              place_id=validated_data.get('place_id'),
                                              status__in=("CREATED", "PAID")
                                              ).exists()
        if has_bookings:
            raise LogicException('Place is busy!')

        return Booking.objects.create(**validated_data)

    def pay(self, instance: Booking):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.status = 'PAID'
        instance.save()
        return instance
