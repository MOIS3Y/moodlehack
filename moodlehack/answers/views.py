from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Category, Period, Answer
from .serializers import (
    CategorySerializer,
    PeriodSerializer,
    AnswerSerializer
)


# WEB:
class AnswersListView(LoginRequiredMixin, generic.ListView):
    template_name = 'answers/index.html'
    model = Answer
    context_object_name = 'answers'
    ordering = ['-create']
    allow_empty = True
    paginate_by = 25

    def get(self, request, *args, **kwargs):
        # HTMX dynamic search:
        if request.headers.get('HX-Request'):
            search = request.GET.get('q')
            if search:
                queryset = Answer.objects.filter(
                    Q(question__icontains=search) |
                    Q(answer__icontains=search)
                )
                context = {self.context_object_name: queryset}
            else:
                queryset = self.get_queryset()
                self.object_list = self.get_queryset()
                context = self.get_context_data()
            return render(
                request=request,
                template_name='answers/includes/_answers.html',
                context=context
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['page_range'] = page.paginator.get_elided_page_range(
            page.number
        )
        return context


# API:
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
