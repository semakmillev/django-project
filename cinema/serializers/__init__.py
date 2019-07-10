from cinema.models import User, Film, Film_Schedule
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'user_name',
                  'password')
        extra_kwargs = {'password': {'write_only': True}}


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'film_name', 'film_length', 'price')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Film.objects.create(**validated_data)

    def update(self, instance: Film, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.film_name = validated_data.get('film_name', instance.film_name)
        instance.film_length = validated_data.get('film_length', instance.film_length)
        instance.price = validated_data.get('price', instance.price)
        instance.id = validated_data.get('id', instance.id)
        # instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance





class FilmScheduleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Film_Schedule
        fields = ('id', 'film_id', 'hall_id', 'film_start')

        '''
        if Video.objects.filter(field_boolean=True).exists():
            print('Video with field_boolean=True exists')
        else:
            super(Video, self).save(*args, **kwargs)
        '''

    def create(self, validated_data):
        return Film_Schedule.objects.create(**validated_data)

    def update(self, instance: Film_Schedule, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.film_id = validated_data.get('film_id', instance.film_id)
        instance.hall_id = validated_data.get('hall_id', instance.hall_id)
        # instance.price = validated_data.get('price', instance.price)
        instance.film_start = validated_data.get('film_start', instance.film_start)
        # instance.style = validated_data.get('style', instance.style)
        print(instance)
        instance.save()
        print(instance)
        return instance


'''class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
'''
