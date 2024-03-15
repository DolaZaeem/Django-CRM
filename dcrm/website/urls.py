from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    #path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('record/<str:quote_no_ref>',views.quote_record,name='record'),
    path('delete_record/<str:quote_no_ref>',views.delete_record,name='delete_record'),
    path('add_record/',views.add_record,name='add_record'),
    path('update_record/<str:quote_no_ref>',views.update_record,name='update_record'),
    path('add_items/<str:quote_no_ref>',views.add_items,name='add_items'),
    path('item_details/<int:pk>',views.update_item,name='update_item'),
    path('delete_items/<int:pk>',views.delete_items,name='delete_items'),
    path('Incomplete',views.Incomplete,name='Incomplete'), #quotes without items
    path('search/', views.search, name='search'),
    path('importdata/', views.importdata, name='importdata'),
]