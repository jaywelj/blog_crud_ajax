# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView

from braces.views import JSONResponseMixin, LoginRequiredMixin

from .forms import PostForm, CommentForm
from .models import Post, Comment
from .mixin import GetContextMixin

class PostList(ListView):
	queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-pk')
	context_object_name = "posts"
	paginate_by = 100

	def get_context_data(self, **kwargs):
		context = super(PostList, self).get_context_data(**kwargs)
		context['range'] = range(context["paginator"].num_pages)
		context['page_title'] = "Post List"

		return context

class PostDraftList(LoginRequiredMixin, ListView):
	queryset = Post.objects.filter(published_date__isnull=True).order_by('-pk')
	template_name="blog/post_draft_list.html"
	context_object_name = "posts"
	paginate_by = 100

	def get_context_data(self, **kwargs):
		context = super(PostDraftList, self).get_context_data(**kwargs)
		context['range'] = range(context["paginator"].num_pages)
		context['page_title'] = "Draft List"


		return context

# class PostDetail(DetailView):
# 	model = Post
# 	context_object_name = "post"

class PostNew(LoginRequiredMixin, GetContextMixin, View):
	model = Post
	form_class = PostForm
	template = "blog/post_new.html"
	data = dict()

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()
			context = self.get_object(request, new_post.pk)
			self.data["form_is_valid"] = True
			self.data["post_content"] = render_to_string("blog/post_list_content.html", context)

		else:
			self.data["form_is_valid"] = False

		context = {
		"form": form,
		}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

	def get(self, request):
		form = self.form_class()
		context = {"form": form}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)


class PostEdit(LoginRequiredMixin, GetContextMixin, View):
	model = Post
	form_class = PostForm
	template = "blog/post_edit.html"
	template_name = "blog/post_edit.html"
	data = dict()

	def post(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		form = self.form_class(request.POST, instance = post)
		if form.is_valid():
			form.save()
			context = self.get_object(request, pk)
			self.data["form_is_valid"] = True
			self.data["post_content"] = render_to_string("blog/post_list_content.html", context)

		else:
			self.data["form_is_valid"] = False

		context = {"form": form}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

	def get(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		form = self.form_class(instance = post)
		context = {"form": form}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

class PostDelete(LoginRequiredMixin, GetContextMixin, View):
	model = Post
	form_class = PostForm
	template = "blog/post_delete.html"
	data = dict()

	def post(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		context = self.get_object(request, pk)
		post.delete()
		self.data["form_is_valid"] = True
		self.data["post_content"] = render_to_string("blog/post_list_content.html", context)
		
		return JsonResponse(self.data)

	def get(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		context = {"post": post}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

class PostPublish(LoginRequiredMixin, GetContextMixin, DetailView):
	model = Post
	form_class = PostForm
	template = "blog/post_publish.html"
	data = dict()

	def post(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		post.published_date = timezone.now()
		post.save()
		context = self.get_object(request, pk)
		self.data["form_is_valid"] = True
		self.data["post_content"] = render_to_string("blog/post_list_content.html", context)
		
		return JsonResponse(self.data)

	def get(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		context = {"post": post}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

class PostDetail(JSONResponseMixin, DetailView):
	model = Post
	json_dumps_kwargs = {'indent': 2}
	template = "blog/post_detail.html"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		context = {"post": self.object}
		context["comments"] = Comment.objects.filter(post=self.object)
		data = {
			"html_form": render_to_string(self.template, context, request=request)
		}

		return self.render_json_response(data)

class AccountLogin(LoginView, JSONResponseMixin):
	template = "registration/login.html"
	template_name = "registration/login-error.html"

	def get(self, request, *args, **kwargs):
		context = {"form": self.form_class}
		data = {
			"html_form": render_to_string(self.template, context, request=request)
		}

		return self.render_json_response(data)

class CommentNew(LoginRequiredMixin, ListView):
	model = Comment 
	form_class = CommentForm
	template = "blog/comment_new.html"
	data = dict()

	def post(self, request, pk):
		form = self.form_class(request.POST)
		if form.is_valid():
			post = get_object_or_404(Post, pk=pk)
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.save()
			comments = Comment.objects.filter(post=post).filter(flag=False)
			context = {
				"post": post,
				"comments": comments,
			}
			self.data["form_is_valid"] = True
			self.data["post_content"] = render_to_string("blog/post_detail.html", context)

		else:
			self.data["form_is_valid"] = False

		context = {
		"form": form,
		}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

	def get(self, request, pk):
		form = self.form_class()
		context = {"form": form}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)














