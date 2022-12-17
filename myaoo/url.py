# from django.urls import path
# from myaoo import views
# import include
# app_name = 'myaoo'
# urlpatterns = [
#  path(r'', views.index, name='index'),
#  path(r'myaoo/', include('myaoo.urls')),
#  ]

from django.urls import path, reverse_lazy, include
from myaoo import views, admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'myaoo'

urlpatterns = [
                  path('register_user', views.register_user, name='register_user'),
                  path(r'', views.index, name='index'),
                  path(r'about/', views.about, name='about'),
                  path(r'<int:cat_no>/', views.detail, name='Category'),
                  path(r'products/', views.products, name='products'),
                  path(r'placeorder/', views.place_order, name='placeorder'),
                  path(r'products/<int:prod_id>/', views.productdetail, name='productdetail'),
                  path(r'login/', views.user_login, name='user_login'),
                  path(r'logout/', views.user_logout, name='user_logout'),
                  #path(r'myorders/<int:user_id>', views.myorders, name='myorders'),

                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                  path(r'myorders', views.myorders, name='myorders'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
