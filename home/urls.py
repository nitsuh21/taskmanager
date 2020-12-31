from django.contrib import admin
from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.wellcome,name='wellcome'),
    path('home',views.home,name='home'),
    path('addtask',views.addtask,name='addtask'),
    path('incompletedtasks',views.incompletedtasks,name='incompletedtasks'),
    path('donetasks',views.donetasks,name='donetasks'),
    path('edit/<str:id>',views.edit,name='edit'),
    path('search/',views.search,name='search'),
    path('printing',views.printing,name='printing'),
    path('delete/<str:id>/',views.delete,name='delete'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('createofficer',views.createofficer,name='createofficer'),
    path('profile/<str:id>',views.profile,name='profile'),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]
