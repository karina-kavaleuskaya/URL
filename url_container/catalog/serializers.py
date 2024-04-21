from rest_framework import serializers, generics
from catalog.models import Collection, Container


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Container
        fields = ('id', 'title', 'description', 'url', 'image', 'url_type', 'collection',
                  'created_at', 'changed_at')


class CollectionSerializer(serializers.ModelSerializer):
    containers = UrlSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ('id', 'name', 'description', 'user', 'containers')


class CollectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'user']

    def create(self, validated_data):
        collection = Collection.objects.create(**validated_data)

        return collection


class CollectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name', 'description']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UrlUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['url']

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance







