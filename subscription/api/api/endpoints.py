from api.api.serializers import (EditorSerializer, JournalSerializer,
                                 EditorWithJournalsSerializer, JournalPartialSerializer,
                                 CustomerSerializer, SubscriptionSerializer, SubscriptionOnlySerializer)
from api.models import Editor, Journal, Customer, Subscription
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin, CreateModelMixin)
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class CustomerViewSet(GenericViewSet, CreateModelMixin, RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(methods=['post'], detail=True, url_path='subscriptions')
    def add_subscription(self, request, pk=None):
        request.data["customer"] = pk
        serializer = SubscriptionOnlySerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            subscription = Subscription(journal_id=serializer.data['journal'], customer_id=pk)
            subscription.save()
            return Response(SubscriptionSerializer(subscription).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JournalViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class EditorViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer


class EditorWithJournalsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    queryset = Editor.objects.all()
    serializer_class = EditorWithJournalsSerializer

    @action(methods=['post'], detail=True, url_path='journals')
    def add_journal(self, request, pk=None):
        serializer = JournalPartialSerializer(data=request.data)
        if serializer.is_valid():
            journal = Journal(journal_name=serializer.data['journal_name'], price=serializer.data['price'], editor_id=pk)
            journal.save()
            return Response(JournalSerializer(journal).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditorListView(ListAPIView):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer


class EditorDetailView(RetrieveAPIView):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer
