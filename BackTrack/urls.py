from django.urls import path
from BackTrack import views

urlpatterns = [
    path('', views.LoginPage.as_view(), name='LoginPage'),
    path('signin',views.Signin.as_view(), name='signin'),
    path('Productbacklog/',views.Productbacklog.as_view(),name='Productbacklog'),
    path('logout',views.Logout.as_view(), name='logout'),
    path('CreateProject',views.CreateProject.as_view(),name='CreateProject'),
    path('Productbacklog/AddPBI',views.AddPBI.as_view(),name='AddPBI'),
    path('Productbacklog/DeletePBI/',views.DeletePBI.as_view(),name='DeletePBI'),
    path('Productbacklog/filter',views.Filter.as_view(),name='filter'),
    path('Overview',views.Overview.as_view(),name='Overview'),
]
