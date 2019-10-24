from django.urls import path
from BackTrack import views

urlpatterns = [
    path('', views.LoginPage.as_view(), name='LoginPage'),
    path('signin',views.Signin.as_view(), name='signin'),
    path('ProductBacklog',views.ProductBacklog.as_view(),name='ProductBacklog'),
    path('logout',views.Logout.as_view(), name='logout'),
    path('CreateProject',views.CreateProject.as_view(),name='CreateProject'),
]
