from rest_framework import serializers

from .models import Category, Period, Answer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    create = serializers.DateTimeField(read_only=True)
    update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
