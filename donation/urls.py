from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^challenge/(?P<pk>[0-9]+)$', views.ChallengeView.as_view(), name='challenge_view'),
    url(r'^challenge/(?P<pk>[0-9]+)/delete/$', views.ChallengeDelete.as_view(), name='challenge_delete'),
    url(r'^challenge/create/$', views.ChallengeCreate.as_view(), name='challenge_create'),
    url(r'^challenge/(?P<pk>[0-9]+)/up_vote/$', views.UserChallengeUpVoteToggle.as_view(), name='challenge_up_vote'),
    url(r'^challenge/(?P<pk>[0-9]+)/down_vote/$', views.UserChallengeDownVoteToggle.as_view(), name='challenge_down_vote'),
    url(r'^challenge/(?P<pk>[0-9]+)/donate/', views.UserChallengeDonate.as_view(), name='challenge_donate'),
    url(r'^challenge/(?P<pk>[0-9]+)/comment/', views.ChallengeComment.as_view(), name='challenge_comment'),
    url(r'^comment_delete/(?P<pk>[0-9]+)/', views.ChallengeCommentDelete.as_view(), name='challenge_comment_delete'),
    url(r'^challenge/search/', views.TagChallengeSearch.as_view(), name='challenge_tag_search'),
    url(r'^account/register/$', views.Register.as_view(), name='register'),
    url(r'^account/login/$', views.LogIn.as_view(), name='log_in'),
    url(r'^account/logout/$', views.LogOut.as_view(), name='log_out'),
    url(r'^search/$', views.UserSearch.as_view(), name='user_search'),
    url(r'^edit-profile/(?P<pk>[0-9]+)$', views.EditProfile.as_view(), name='edit_user_profile'),
    url(r'^user-profile/(?P<pk>[0-9]+)$', views.UserProfile.as_view(), name='user_profile'),
    url(r'^user-profile/(?P<pk>[0-9]+)/follow/$', views.UserFollowToggle.as_view(), name='user_follow'),
    url(r'^user-profile/(?P<pk>[0-9]+)/follows/$', views.UserFollows.as_view(), name='user_follows'),
    url(r'^user-profile/(?P<pk>[0-9]+)/followers/$', views.UserFollowers.as_view(), name='user_followers'),
    url(r'^feed/$', views.FeedView.as_view(), name='feed'),
    url(r'^$',  views.IndexView.as_view(), name='main'),
]
