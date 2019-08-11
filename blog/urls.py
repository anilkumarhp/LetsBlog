from django.urls import path
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)

from .views import (
    homepage,
    loginpage,
    logout_user,
    register_user,
    post_list,
    post_detail,
    new_post,
    post_search,
)

urlpatterns = [
    path('', homepage, name="home"),
    path('post/new/', new_post, name='post_new'),

    # Login, Logout & Register
    path('login/', loginpage, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),

    # Change password
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # post
    path('list/', post_list, name='list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='details'),
    path('search/', post_search, name='post_search'),
]
