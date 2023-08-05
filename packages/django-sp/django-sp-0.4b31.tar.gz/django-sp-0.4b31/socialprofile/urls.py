"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

# pylint: disable=W0401, W0614, E1120

from django.conf.urls import url, include
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from . import views

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    # Profile Self View
    url(r'^$', never_cache(login_required(views.SocialProfileView.as_view())), name="sp_profile_view_page"),
    url(r'^login/$', never_cache(login_required(views.home))),
    url(r'^logout/$', never_cache(views.logout), name="sp_logout_page"),
    url(r'^done/$', views.done, name='done'),
    # url(r'^ajax-auth/(?P<backend>[^/]+)/$', views.ajax_auth, name='ajax-auth'),

    # New Profile
    url(r'^new-profile/$', login_required(views.SocialProfileWelcome.as_view()), name="new_profile"),
    # New Profile's Association
    url(r'^new-association/$', login_required(views.SocialProfileView.as_view()), name="new_profile_association"),
    # Login Error
    url(r'^login-error/$', login_required(views.SocialProfileView.as_view()), name="login_error"),
    # Login Error
    url(r'^inactive/$', login_required(views.SocialProfileView.as_view()), name="inactive"),
    # Profile Disconnected
    url(r'^profile-disconnected/$', login_required(views.SocialProfileView.as_view()), name="profile_disconnected"),

    # Profile Other View
    url(r'^view/(?P<username>\w.+)/$', login_required(views.SocialProfileView.as_view()),
        name="sp_profile_other_view_page"),

    # Profile Edit
    url(r'^edit/(?P<user_id>\d+)/$', never_cache(login_required(views.SocialProfileEditView.as_view())), name="sp_profile_edit_page"),

    # Select Sign Up Method
    url(r'^select/$', never_cache(views.SelectAuthView.as_view()), name="sp_select_page"),

    # Delete
    url(r'^delete/$', login_required(views.DeleteSocialProfileView.as_view()), name="sp_delete_page"),

    # Logout Page
    # url(r'^logout/$', logout, name="sp_logout_page"),

    # Social Auth
    url(r'', include('social_django.urls', namespace='social')),

    # User Sessions
    url(r'', include('user_sessions.urls', 'user_sessions')),

    # OAuth2 Token
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Rest Framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    # One-Time-Password
    # url(r'', include('two_factor.urls', 'two_factor')),

]
