from django.urls import path
from . import views
from django.conf.urls.static import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('welcome',views.welcome,name='welcome'),
    path('signup', views.signup,name='signup'),
    path('home', views.home , name='home'),
    path('patient',views.Parser,name='Launch the parser'),
    path('graph/<int:lead_id>', views.graph, name='graph'),
    path('graph/analyze', views.analyze, name='analyze_graph'),
    path('graph/addGraph', views.add_graph, name='add_graph'),
    path('goto/<file>',views.GoToMainPage,name='GoToMain'),
    path('signout',views.signOut,name='signout')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)