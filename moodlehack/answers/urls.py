from django.urls import include, path

from rest_framework import routers

from . import views


app_name = 'answers'


router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'periods', views.PeriodViewSet)
router.register(r'answers', views.AnswerViewSet)


urlpatterns = [
    path('', views.AnswersListView.as_view(), name='index'),
    path('api/v1/', include(router.urls))
]
