from django.views import generic

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Category, Period, Answer
from .serializers import (
    CategorySerializer,
    PeriodSerializer,
    AnswerSerializer
)


class IndexTemplateView(generic.TemplateView):
    template_name = 'answers/index.html'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = (IsAuthenticated, )


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer']
