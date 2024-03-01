from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    # path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('Aboutus/',views.Aboutus,name='Aboutus'),
    path('schemes',views.schemes,name='schemes'),
    path('loan',views.loan,name='loan'),
    path('cropmanage',views.crop,name='cropmanage'),
    path('crop2',views.crop2,name='crop'),
    path('weather',views.weather,name='weather'),
    path('market/',views.market,name='market'),
    path('estimate',views.chatbot,name='estimate'),
    path('profile',views.profile,name='profile'),
    path('news',views.news,name='news'),
    path('detail/<int:pk>',views.detail,name='detail'),
    path('services',views.services,name='services'),
    path('edit',views.edit,name='edit'),
    path('logout',views.logout,name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    # path('forgotemail',views.forgotemail,name='forgotemail'),
    # path('send_mail',views.mail,name='send_mail'),
    # path('verify/<uid>',views.verify,name='verify')
]
