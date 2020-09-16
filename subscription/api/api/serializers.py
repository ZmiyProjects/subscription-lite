from rest_framework import serializers
from ..models import Editor, Journal, Customer, Subscription

from datetime import date


def age(birth_date: date) -> int:
    """Получает дату рожденрия, возвращает количество полных лет на текущую дату"""
    current_date = date.today()
    if (current_date.month, current_date.day) > (birth_date.month, birth_date.day):
        return current_date.year - birth_date.year
    return (current_date.year - birth_date.year) - 1


class EditorSerializer(serializers.ModelSerializer):
    # count = serializers.SerializerMethodField('journals_count')

    # def journals_count(self, obj):
    #    return Journal.objects.all().filter(editor_id=obj.pk).count()

    class Meta:
        model = Editor
        # fields = '__all__'
        fields = ['id', 'editor_name', 'journals_count']


class EditorPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = ['id', 'editor_name']


class JournalPartialSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if (price := attrs.get("price")) is not None:
            if price <= 0:
                raise serializers.ValidationError("incorrect price!")
        return attrs

    class Meta:
        model = Journal
        fields = ['id', 'journal_name', 'price']


class EditorWithJournalsSerializer(serializers.ModelSerializer):
    journals = JournalPartialSerializer(many=True, read_only=True)

    class Meta:
        model = Editor
        fields = '__all__'


class JournalSerializer(serializers.ModelSerializer):
    editor = EditorSerializer(many=False, read_only=True)

    class Meta:
        model = Journal
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
    def validate(self, attrs):
        if (birth_date := attrs.get("birth_date")) is not None:
            if age(birth_date) < 18:
                raise serializers.ValidationError("Customer mast be 18+!")
        return attrs

    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
