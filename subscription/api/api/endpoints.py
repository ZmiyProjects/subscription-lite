from ..api.serializers import (EditorSerializer, JournalSerializer,
                               EditorWithJournalsSerializer, JournalPartialSerializer,
                               CustomerSerializer, SubscriptionSerializer, SubscriptionOnlySerializer,
                               EditorPartialSerializer)
from ..models import Editor, Journal, Customer, Subscription
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   CreateModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.transaction import atomic


class CustomerViewSet(GenericViewSet, CreateModelMixin, RetrieveAPIView, UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'id': serializer.data["id"]}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='subscriptions')
    def add_subscription(self, request, pk=None):
        request.data["customer"] = pk
        serializer = SubscriptionOnlySerializer(data=request.data)
        if serializer.is_valid():
            subscription = Subscription(journal_id=serializer.data['journal'], customer_id=pk)
            subscription.save()
            return Response(SubscriptionSerializer(subscription).data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JournalViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class EditorWithJournalsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin):
    queryset = Editor.objects.all()
    # serializer_class = EditorWithJournalsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return EditorSerializer
        elif self.action == 'retrieve':
            return EditorSerializer
        elif self.action == 'create':
            return EditorPartialSerializer
        return EditorPartialSerializer

    def create(self, request, *args, **kwargs):
        """Добавляет издателю новый журнал и увеличивает количество изданных (journals_count) на 1"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'id': serializer.data["id"]}, status=status.HTTP_201_CREATED)

    @atomic
    @action(methods=['post'], detail=True, url_path='journals')
    def add_journal(self, request, pk=None):
        serializer = JournalPartialSerializer(data=request.data)
        if serializer.is_valid():
            journal = Journal(
                journal_name=serializer.data['journal_name'], price=serializer.data['price'], editor_id=pk)

            o = Editor.objects.get(id=pk)
            o.journals_count += 1
            journal.save()
            o.save()
            return Response({'id': JournalSerializer(journal).data["id"]})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_journal.mapping.get
    def get_journals(self, request, pk=None):
        return Response(EditorWithJournalsSerializer(Editor.objects.get(id=pk)).data, status.HTTP_200_OK)


class EditorListView(ListAPIView):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer


class EditorDetailView(RetrieveAPIView):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer
