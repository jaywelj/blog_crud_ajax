# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from .forms import PostForm
from .models import Post


class PostList(View):
	form_class = PostForm
	template = "blog/post_list.html"
	model = Post

	def get(self, request):
		posts = self.model.objects.filter(published_date__lte=timezone.now()).order_by('-pk')
		form = self.form_class()
		context = {
			"posts": posts,
			"form": form,
		}
		
		return render(request, self.template, context) 

class PostDraftList(View):
	template = "blog/post_list.html"
	model = Post

	def get(self, request):
		posts = self.model.objects.filter(published_date__isnull=True).order_by('-pk')
		context = {"posts": posts}
		
		return render(request, self.template, context) 


class PostNew(View):
	model = Post
	form_class = PostForm
	template = "blog/post_new.html"
	data = dict()

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			if new_post.published_date:
				posts = self.model.objects.filter(published_date__isnull=False).order_by('-pk')
			else:
				posts = self.model.objects.filter(published_date__isnull=True).order_by('-pk')

			new_post.author = request.user
			new_post.save()
			self.data["form_is_valid"] = True
			self.data["post_content"] = render_to_string("blog/post_list_content.html", {"posts": posts})

		else:
			self.data["form_is_valid"] = False

		context = {"form": form}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

	def get(self, request):
		form = self.form_class()
		context = {"form": form}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)


class PostEdit(View):
	model = Post
	form_class = PostForm
	template = "blog/post_edit.html"
	data = dict()

	def post(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		form = self.form_class(request.POST, instance = post)
		if form.is_valid():
			new_post = form.save()
			if new_post.published_date:
				posts = self.model.objects.filter(published_date__isnull=False).order_by('-pk')
			else:
				posts = self.model.objects.filter(published_date__isnull=True).order_by('-pk')
			self.data["form_is_valid"] = True
			self.data["post_content"] = render_to_string("blog/post_list_content.html", {"posts": posts})

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

class PostDelete(View):
	model = Post
	form_class = PostForm
	template = "blog/post_delete.html"
	data = dict()

	def post(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		post.delete()
		if post.published_date:
			posts = self.model.objects.filter(published_date__isnull=False).order_by('-pk')
		else:
			posts = self.model.objects.filter(published_date__isnull=True).order_by('-pk')
		self.data["form_is_valid"] = True
		self.data["post_content"] = render_to_string("blog/post_list_content.html", {"posts": posts})
		
		return JsonResponse(self.data)

	def get(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		context = {"post": post}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)

class PostPublish(View):
	model = Post
	form_class = PostForm
	template = "blog/post_publish.html"
	data = dict()

	def post(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		if post.published_date:
			posts = self.model.objects.filter(published_date__isnull=False).order_by('-pk')
		else:
			posts = self.model.objects.filter(published_date__isnull=True).order_by('-pk')
		post.published_date = timezone.now()
		post.save()
		self.data["form_is_valid"] = True
		self.data["post_content"] = render_to_string("blog/post_list_content.html", {"posts": posts})
		
		return JsonResponse(self.data)

	def get(self, request, pk):
		post = get_object_or_404(self.model, pk=pk)
		context = {"post": post}
		self.data["html_form"] = render_to_string(self.template, context, request=request)

		return JsonResponse(self.data)











