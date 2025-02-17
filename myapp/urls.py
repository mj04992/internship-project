from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.base,name='base'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    # password change
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),

    # reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    #user registration
    path('register/',views.register,name='register'),

    #profile
    path('profile/',views.profile,name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),

    # contact
    path('contact/', views.contact, name='contact'),

    #review
    path('add_review/<int:consumer_id>/', views.add_review, name='add_review'),
    path('view_reviews/<int:consumer_id>/', views.view_reviews, name='view_reviews'),

    #notification
    path('notifications/', views.user_notifications, name='user_notifications'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
