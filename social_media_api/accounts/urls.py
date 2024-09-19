from django.urls import path
from accounts.views import RegisterView
#from accounts.views import LoginView

from accounts.views import FollowUserView, UnfollowUserView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    #path('login/', LoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('users/', UserListView.as_view(), name='user-list'),
]
