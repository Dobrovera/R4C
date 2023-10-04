from django.contrib import admin
from django.urls import path
from robots.views import RobotView, RobotLastWeekDataView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots/', RobotView.as_view()),
    path('download/', RobotLastWeekDataView.as_view()),
]
