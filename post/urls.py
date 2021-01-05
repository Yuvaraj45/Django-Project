from django.urls import path,include
from post.views import *
urlpatterns = [
	path('postlist/',post_list,name='post_list'),
    path('view/<slug:slug_text>/',post_detail,name='post_detail'),
    path('postform',post_form,name='post_form'),
    path('post_edit/<slug:slug_text>/',post_edit,name='post_editform'),
    path('post_delete/<slug:slug_text>/',post_delete,name='post_delete'),
    path('loginform',user_login,name='user_login'),
    path('logout',user_logout,name='user_logout'),
    path('register',user_registrationform,name="user_registrationform"),
    path('profile',user_profile,name='user_profile'),
    path('',post_likes,name='post_likes'),
    path('<slug:slug_text>',post_favourite,name='post_favourite'),
    path('favourites/',fav_list,name='fav_list'),
   ]
