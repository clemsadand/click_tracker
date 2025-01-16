from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('increment_click/', views.increment_click, name='increment_click'),
    path('undo_last_click/', views.undo_last_click, name='undo_last_click'),
    path('clear_all/', views.clear_all, name='clear_all'),
    path('get_chart_data/', views.get_chart_data, name='get_chart_data'),
]
