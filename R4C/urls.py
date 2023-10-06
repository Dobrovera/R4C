from django.contrib import admin
from django.urls import path
from robots.views import RobotView, RobotLastWeekDataView
from orders.views import OrderView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots/', RobotView.as_view()),
    path('download/', RobotLastWeekDataView.as_view()),
    path('order/', OrderView.as_view()),
]
