from django.urls import path
from . import views
from django.conf.urls.static import settings, static

urlpatterns = [
    path('', views.greeting, name='greeting'),
    path('graph/<int:lead_id>/', views.graph, name='graph'),
    path('graph/analyze/', views.analyze, name='analyze_graph'),
    path('graph/addGraph/', views.add_graph, name='add_graph'),
    path('goto/<file>/', views.GoToMainPage, name='GoToMain'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
