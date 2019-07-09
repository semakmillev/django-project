from cinema.models import User, Film
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


'''class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
'''
