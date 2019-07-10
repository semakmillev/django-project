from rest_framework import serializers

from cinema.models.booking import Booking


class BookingSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ('user_id', 'schedule_id', 'place_id', 'status')

        '''
        if Video.objects.filter(field_boolean=True).exists():
            print('Video with field_boolean=True exists')
        else:
            super(Video, self).save(*args, **kwargs)
        '''

    def create(self, validated_data):
        has_bookings = Booking.objects.filter(schedule_id=validated_data.get('schedule_id'),
                                              place_id=validated_data.get('place_id'),
                                              status__in=("CREATED", "PAID")
                                              # status_ =("CREATED", "PAYED")
                                              ).exists()
        if has_bookings:
            raise Exception('crap!')

        return Booking.objects.create(**validated_data)

    def pay(self, instance: Booking):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.status = 'PAID'
        # instance.film_name = validated_data.get('film_name', instance.film_name)
        # instance.film_length = validated_data.get('film_length', instance.film_length)
        # instance.price = validated_data.get('price', instance.price)
        # instance.id = validated_data.get('id', instance.id)
        # instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
