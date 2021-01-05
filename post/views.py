from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import post,Images,Comments
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.template.loader import render_to_string
from django.forms import modelformset_factory

@login_required(login_url='blog:user_login')
def post_list(request):
	obj_list = post.active.all().order_by('-id')
	if request.user.is_staff or request.user.is_superuser:
		obj_list = post.objects.all().order_by('-id')
	query = request.GET.get("q")
	if query:
		obj_list = obj_list.filter(
			Q(title__icontains=query)|
			Q(author__username=query)|
			Q(description__icontains=query)
			)
	paginator = Paginator(obj_list,6)
	page = request.GET.get('page')
	obj = paginator.get_page(page)
	context = {
	'posts':obj
	}
	return render(request,'post_list.html',context)

def post_detail(request,slug_text):
	obj = post.objects.get(slug=slug_text)
	comments = Comments.objects.filter(post=obj,reply=None).order_by('-id')
	# print(obj.images_set.all())
	is_liked = False
	is_fav = False
	if obj.likes.filter(id=request.user.id).exists():
		is_liked = True
	if obj.favourite.filter(id=request.user.id).exists():
		is_fav = True
	if request.method == 'POST':
		form = commentsform(request.POST or None)
		if form.is_valid():
			content = request.POST.get('content')
			reply_id = request.POST.get('comment_id')
			main_comment = None 
			if reply_id:
				main_comment = Comments.objects.get(id=reply_id)
			Comments.objects.create(post=obj,user=request.user,content=content,reply=main_comment)
		# return redirect(obj.get_absolute_url())
	else:
		form = commentsform()
	context = {
	'form':form,
	'comments':comments,
	'instance':obj,
	'is_liked':is_liked,
	'is_fav':is_fav,
	'total_likes':obj.total_likes(),
	}
	if request.is_ajax():
		html = render_to_string('comments.html',context,request=request)
		return JsonResponse({'form':html})
	return render(request,'post_detail.html',context)

def post_likes(request):
	post_obj = post.objects.get(id=request.POST.get('id'))
	is_liked = False
	if post_obj.likes.filter(id=request.user.id).exists():
		post_obj.likes.remove(request.user)
		is_liked = False
	else:
		post_obj.likes.add(request.user)
		is_liked = True
	context = {
	'instance':post_obj,
	'is_liked':is_liked,
	'total_likes':post_obj.total_likes(),
	}
	if request.is_ajax():
		html = render_to_string('like_section.html',context,request=request)
		return JsonResponse({'form':html})

	# return HttpResponseRedirect(post_obj.get_absolute_url())
def post_favourite(request,slug_text):
	post_obj = post.objects.get(slug=slug_text)
	if post_obj.favourite.filter(id=request.user.id).exists():
		post_obj.favourite.remove(request.user)
	else:
		post_obj.favourite.add(request.user)
	return redirect(post_obj.get_absolute_url())

def fav_list(request):
	user = request.user
	user_fav = user.favourite.all()
	print(user_fav)
	context = {
	'user_fav':user_fav,
	}
	return render(request,'fav_list.html',context)

def post_form(request):
	imageform = modelformset_factory(Images,fields=('image',),extra=4)
	if request.method == 'POST':
		form = postform(request.POST or None)
		imageform = imageform(request.POST or None,request.FILES or None)
		if form.is_valid() and imageform.is_valid():
			# post.objects.create(**form.cleaned_data)
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			for p in imageform:
				try:
					photo = Images(post=post,image=p.cleaned_data['image'])
					photo.save()
					print(post,p.cleaned_data['image'])
				except:
					break
			messages.success(request,'Post has successfully created..')
			return redirect('blog:post_list')
	else:
		form = postform(request.POST or None)
		imageform = imageform(queryset=Images.objects.none())
	context = {
	'form':form,
	'imageform':imageform,
	}
	return render(request,'postform.html',context)

def delete_img(post_obj):
	image_list = Images.objects.filter(post=post_obj)
	for i in image_list:
		i.delete()
	return None

def post_edit(request,slug_text):
	post_obj = post.objects.get(slug=slug_text)
	imageform = modelformset_factory(Images,fields=('image',),extra=4,max_num=4)
	if request.user != post_obj.author:
		raise Http404
	if request.method == 'POST':
		form = post_editform(request.POST or None,instance=post_obj)
		imageform = imageform(request.POST or None,request.FILES or None)
		# print(imageform)
		if form.is_valid() and imageform.is_valid():
			delete_img(post_obj)
			form.save()
			for p in imageform:
				try:
					photo = Images(post=post_obj,image=p.cleaned_data['image'])
					photo.save()
				except:
					break
			messages.success(request,"The post updated successfully.")
			return redirect(post_obj.get_absolute_url())
	else:
		form = post_editform(instance=post_obj)
		imageform = imageform(queryset=Images.objects.filter(post=post_obj))	
	context = {
	'post':post_obj,
	'form':form,
	'imageform':imageform,
	}
	return render(request,'post_editform.html',context)

def post_delete(request,slug_text):
	post_obj = post.objects.get(slug=slug_text)
	if request.user != post_obj.author:
		raise Http404
	delete_img(post_obj)
	post_obj.delete()
	messages.warning(request,f'{post_obj.title} has been successfully deleted.')
	return redirect('blog:post_list')

def user_login(request):
	form = loginform(request.POST or None)
	if request.method=='POST':
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse("blog:post_list"))
			else:
				return HttpResponse("invalid account ")
	return render(request,'loginform.html',{'form':form})

def user_logout(request):
	logout(request)
	return redirect("blog:post_list")

def user_registrationform(request):
	form = userregistrationform(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			# User.objects.create(**cleaned_data)
			password = form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']
			if password != confirm_password:
				raise forms.ValidationError("Password Mismatch ")
			newuser = form.save(commit=False)
			newuser.set_password(password)
			newuser.save()
			return redirect("blog:user_login")
	return render(request,'userregistrationform.html',{'form':form})

def user_profile(request):
	if request.method == 'POST':
		user_form = userform(data=request.POST or None,instance=request.user)
		profile_form = profileform(data=request.POST or None,instance=request.user.profile,files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('blog:user_profile')
	else:
		user_form = userform(instance=request.user)
		profile_form = profileform(instance=request.user.profile)
	context={
	'user_form':user_form,
	'profile_form':profile_form,
	}
	return render(request,'user_profile.html',context)



