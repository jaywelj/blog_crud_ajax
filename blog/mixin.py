from django.shortcuts import get_object_or_404

from .models import Post


class GetPostContextMixin(object):
	def get_object(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		if post.published_date:
			posts = self.model.objects.filter(published_date__isnull=False).order_by('-pk')
			page_title = "Post List"
		else:
			posts = self.model.objects.filter(published_date__isnull=True).order_by('-pk')
			page_title = "Draft List"
		context = {
			"request": request,
			"posts": posts,
			"user": request.user,
			"page_title": page_title,
		}
		return context

class GetCommentContextMixin(object):
	def get_object(self, request, pk):
		post = get_object_or_404(Post, pk=pk)
		comments = self.model.objects.filter(post=post).order_by("created_date")
		csrf_token_value = request.COOKIES['csrftoken']
		context = {
			"post": post,
			"comments": comments,
			"user": request.user,
			"request": request,
			"csrf_token_value": csrf_token_value,
			"form": self.form_class()
		}
		return context