from django.urls import path
from catalog.views import (CollectionListView, CollectionCreateView, CollectionUpdateView,
                           CollectionDeleteView, UrlCreateView, UrlListView, UrlDeleteView,
                           UrlUpdateView, ContainerAddToCollectionView)


urlpatterns = [
    path('collection/', CollectionListView.as_view(), name='collection'),
    path('create-collection/', CollectionCreateView.as_view(), name='create-collection'),
    path('update-collection/<int:id>/', CollectionUpdateView.as_view(), name='update-collection'),
    path('delete-collection/<int:id>/', CollectionDeleteView.as_view(), name='delete-collection'),
    path('containers/', UrlListView.as_view(), name='container-create'),
    path('containers-create/', UrlCreateView.as_view(), name='container-create'),
    path('delete-container/<int:id>/', UrlDeleteView.as_view(), name='delete-container'),
    path('update-container/<int:id>/', UrlUpdateView.as_view(), name='update-container'),
    path('collections/<int:collection_id>/add-container/', ContainerAddToCollectionView.as_view(),
         name='add-container-to-collection'),

]