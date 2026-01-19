from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, UpdateView
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import AnswerForm
from .models import Answer, Category, Period
from .serializers import AnswerSerializer, CategorySerializer, PeriodSerializer


# HTMX views
@login_required
@require_POST
def check_question_exists(request):
    question_text = request.POST.get("question", "").strip()
    instance_id = request.POST.get("instance_id")

    if not question_text:
        return HttpResponse("")

    qs = Answer.objects.filter(question__iexact=question_text)
    if instance_id:
        qs = qs.exclude(id=instance_id)

    if qs.exists():
        response = HttpResponse(
            '<span id="error_1_id_question" class="invalid-feedback d-block">'
            '<strong>{}</strong>'
            '</span>'.format(_("Answer with this question already exists."))
        )
        response["HX-Trigger"] = '{"fieldInvalid": "question"}'
        return response

    response = HttpResponse(
        '<span class="valid-feedback d-block">'
        '<strong>{}</strong>'
        '</span>'.format(_("Question is unique."))
    )
    response["HX-Trigger"] = '{"fieldValid": "question"}'
    return response


# WEB Views
class AnswersListView(LoginRequiredMixin, generic.ListView):
    """
    View to display a filtered list of answers.
    Supports standard GET requests and HTMX partial updates for live search.
    """

    model = Answer
    template_name = "answers/index.html"
    context_object_name = "answers"
    paginate_by = 24  # 3x8 grid

    def get_queryset(self):
        # Start with all answers and optimize DB query
        # by pre-selecting categories
        queryset = Answer.objects.all().select_related("category")

        # Extract filter parameters from the GET request
        query = self.request.GET.get("q")
        category_id = self.request.GET.get("category")
        status = self.request.GET.get("status")
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")
        quarter = self.request.GET.get("quarter")

        # Apply text search filter (Question or Answer content)
        if query:
            queryset = queryset.filter(
                Q(question__icontains=query) | Q(answer__icontains=query)
            )

        # Apply exact match filters
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if status:
            queryset = queryset.filter(status=status)
        if year:
            queryset = queryset.filter(year=year)
        if month:
            queryset = queryset.filter(month=month)

        # Calculate month range for Quarter filter (e.g., Q1 = Months 1 to 3)
        if quarter:
            try:
                q_int = int(quarter)
                start_month = (q_int - 1) * 3 + 1
                end_month = q_int * 3
                queryset = queryset.filter(
                    month__range=(start_month, end_month)
                )
            except ValueError:
                pass  # Ignore invalid quarter values

        # Return ordered results: newest years/months first,
        # then by last update
        return queryset.order_by("-year", "-month", "-update")

    def get(self, request, *args, **kwargs):
        """
        Handle HTMX requests. If the request comes from HTMX (live search),
        render only the partial answers list template.
        """
        if request.headers.get("HX-Request"):
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            return render(request, "answers/includes/_answers.html", context)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Inject additional choices into the template context
        for filter dropdowns.
        """
        context = super().get_context_data(**kwargs)

        # Provide choice lists directly from the Model
        context["categories"] = Category.objects.all()
        context["status_choices"] = Answer.STATUS_CHOICES
        context["month_choices"] = Answer.MONTH_CHOICES
        context["year_choices"] = Answer.YEAR_CHOICES

        context["page_title"] = _("Answers")

        # Handle pagination for elided page range (e.g., 1 2 ... 10)
        page_obj = context.get("page_obj")
        if page_obj:
            context["page_range"] = page_obj.paginator.get_elided_page_range(
                page_obj.number, on_each_side=2, on_ends=1
            )

        return context


class AnswerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Answer
    template_name = "answers/answer_detail.html"
    context_object_name = "answer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = format_lazy(
            _("View answer #{id}"),
            id=self.object.id
        )
        return context


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = "answers/answer_form.html"

    def form_valid(self, form):
        # Save the form and assign the object to self.object
        self.object = form.save()

        # Add a success message using Django messages framework
        messages.success(
            self.request,
            format_lazy(
                _("Answer #{id} successfully created!"),
                id=self.object.pk
            )
        )

        # Check which button was pressed in the POST data
        if "save_and_add" in self.request.POST:
            return redirect("answers:create")

        if "save_and_continue" in self.request.POST:
            return redirect("answers:update", pk=self.object.pk)

        # Redirect to the detail view of the newly created object by default
        return redirect("answers:detail", pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Add new answer")
        return context


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = "answers/answer_form.html"

    def get_success_url(self):
        # Default success URL if no special button is pressed
        return reverse_lazy("answers:detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _("Answer successfully updated!"))

        # Check if "Save and continue" was pressed
        if "save_and_continue" in self.request.POST:
            return redirect("answers:update", pk=self.object.pk)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = format_lazy(
            _("Edit answer #{id}"),
            id=self.object.id
        )
        context["instance_id"] = self.object.id
        return context


class AnswerDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy("answers:index")
    success_message = _("Answer successfully deleted!")


# API Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = (IsAuthenticated,)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["question", "answer"]
