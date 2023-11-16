from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.ChaletHome.as_view(), name='home'),
    path('menu/', views.MenuHome.as_view(), name='menu'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
]
