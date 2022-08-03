from django.urls import path
from .views import IndexView, LoginView, LogoutView, DailyReports, WeeklyRreports, MonthlyReports

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('daily/report', DailyReports.as_view(), name='daily_report'),
    path('weekly/report', WeeklyRreports.as_view(), name='weekly_report'),
    path('monthly/report', MonthlyReports.as_view(), name='monthly_report'),
]
