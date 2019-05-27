from django.conf.urls import url
from . import views


urlpatterns = [
	url(r"^new/$", views.PostNew.as_view(), name="post_new"),
	url(r"^(?P<pk>\d+)/detail/$", views.PostDetail.as_view(), name="post_detail"),
	url(r"^(?P<pk>\d+)/edit/$", views.PostEdit.as_view(), name="post_edit"),
	url(r"^(?P<pk>\d+)/delete/$", views.PostDelete.as_view(), name="post_delete"),
	url(r"^list/$", views.PostList.as_view(), name="post_list"),
	url(r"^draft_list/$", views.PostDraftList.as_view(), name="post_draft_list"),
	# url(r"^publish/(?P<pk>\d+)/$", views.PostPublish.as_view(), name="post_publish"),
	url(r"^(?P<pk>\d+)/publish/$", views.PostPublish.as_view(), name="post_publish"),
	url(r"^(?P<pk>\d+)/comment/new/$", views.CommentNew.as_view(), name="comment_new"),
]