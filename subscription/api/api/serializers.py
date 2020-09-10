from rest_framework import serializers
from ..models import Editor, Journal, Customer, Subscription


class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = '__all__'


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'


class JournalPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'journal_name', 'price']


class EditorWithJournalsSerializer(serializers.ModelSerializer):
    journals = JournalPartialSerializer(many=True, read_only=True)

    class Meta:
        model = Editor
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    journal = JournalSerializer(many=False, read_only=True)

    class Meta:
        model = Subscription
        fields = ['start_date', 'end_date', 'journal']


class SubscriptionOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
