import requests
from bs4 import BeautifulSoup
from catalog.models import Collection, Container
from catalog.serializers import (CollectionSerializer, CollectionCreateSerializer, CollectionUpdateSerializer,
                                 UrlSerializer, UrlUpdateSerializer)
from datetime import datetime
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class CollectionListView(ListAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        queryset = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)


class CollectionCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CollectionCreateSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionUpdateView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, id):
        try:
            collection = Collection.objects.get(id=id)
        except Collection.DoesNotExist:
            return Response({'detail': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionUpdateSerializer(collection, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        try:
            collection = Collection.objects.get(pk=id)
        except Collection.DoesNotExist:
            return Response({'detail': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UrlCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UrlSerializer

    def post(self, request):
        url = request.data.get('url')
        user = request.user

        if not url:
            return Response({'detail': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        if Container.objects.filter(url=url).exists():
            return Response({'detail': 'URL already exists'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(url)
        if response.status_code != 200:
            return Response({'detail': 'Failed to fetch data from the URL'}, status=status.HTTP_400_BAD_REQUEST)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else ' '
        description = soup.find('meta', {'name': 'description'})['content'] \
            if soup.find('meta', {'name': 'description'}) else ' '
        image = soup.find('meta', {'property': 'og:image'})['content'] \
            if soup.find('meta',{'property': 'og:image'}) else ' '
        url_type = soup.find('meta', {'property': 'og:type'})['content'] \
            if soup.find('meta', {'property': 'og:type'}) else 'Website'

        container = Container(
            title=title,
            description=description,
            url=url,
            image=image,
            url_type=url_type,
            user=user,
            created_at=datetime.now(),
            changed_at=datetime.now()
        )
        print(container.title, container.description)
        container.save()


        serializer = self.serializer_class(container)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UrlListView(ListAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Container.objects.filter(user=request.user)
        serializer = UrlSerializer(queryset, many=True)
        return Response(serializer.data)


class UrlDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        try:
            collection = Container.objects.get(pk=id)
        except Container.DoesNotExist:
            return Response({'detail': 'Url not found'}, status=status.HTTP_404_NOT_FOUND)

        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UrlUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        try:
            container = Container.objects.get(id=id)
        except Container.DoesNotExist:
            return Response({'detail': 'Url not found'}, status=status.HTTP_404_NOT_FOUND)

        url = request.data.get('url', container.url)
        response = requests.get(url)

        if response.status_code != 200:
            return Response({'detail': 'Failed to fetch data from the URL'}, status=status.HTTP_400_BAD_REQUEST)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else ''
        description = soup.find('meta', {'name': 'description'})['content']\
            if soup.find('meta', {'name': 'description'}) else ''
        image = soup.find('meta', {'property': 'og:image'})['content'] \
            if soup.find('meta', {'property': 'og:image'}) else ''
        url_type = soup.find('meta', {'property': 'og:type'})['content'] \
            if soup.find('meta', {'property': 'og:type'}) else 'Website'

        container.url = url
        container.title = title
        container.description = description
        container.image = image
        container.url_type = url_type
        container.changed_at = datetime.now()
        container.save()

        serializer = UrlSerializer(container)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UrlAndCollectionView(generics.UpdateAPIView):
    serializer_class = UrlSerializer

    def put(self, request, *args, **kwargs):
        container_id = kwargs.get('container_id')
        try:
            container = Container.objects.get(id=container_id)
        except Container.DoesNotExist:
            return Response({'error': 'Container not found.'}, status=status.HTTP_404_NOT_FOUND)

        collection_id = request.data.get('collection_id')
        try:
            collection = Collection.objects.get(id=collection_id)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found.'}, status=status.HTTP_404_NOT_FOUND)

        container.collections.add(collection)

        serializer = self.get_serializer(container)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContainerAddToCollectionView(APIView):
    def post(self, request, collection_id):
        try:
            collection = Collection.objects.get(id=collection_id)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection does not exist'}, status=400)
        container_id = request.data.get('container_id')

        try:
            container = Container.objects.get(id=container_id)
        except Container.DoesNotExist:
            return Response({'error': 'Container does not exist'}, status=400)
        container.collection.add(collection)
        serializer = UrlSerializer(container)
        return Response(serializer.data, status=201)
