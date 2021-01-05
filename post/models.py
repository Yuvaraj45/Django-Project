from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
class postmanager(models.Manager):
	def all(self):
		return super(postmanager,self).all().filter(status='published')
class post(models.Model):
	choice = (
		('draft','Draft'),('published','Published')
	)
	title = models.CharField(max_length=100)
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_post')
	slug = models.SlugField(max_length=100,unique=True)
	description = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=100,choices=choice,default='draft')
	likes = models.ManyToManyField(User,related_name='likes',blank=True)
	restrict_comments = models.BooleanField(default=False)
	favourite = models.ManyToManyField(User,related_name='favourite',blank=True)

	def get_absolute_url(self):
		return reverse("blog:post_detail",args=[self.slug])

	def total_likes(self):
		return self.likes.count()
	active = postmanager()
	objects = models.Manager()

class Images(models.Model):
	post = models.ForeignKey(post,on_delete=models.CASCADE)
	image = models.ImageField(upload_to='image/',blank=True,null=True)

	def delete(self,*args,**kwargs):
		self.image.delete()
		super().delete(*args,**kwargs)

class Comments(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(post,on_delete=models.CASCADE)
	content = models.TextField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
	reply = models.ForeignKey('self',null=True,related_name='replies',on_delete=models.CASCADE)

class profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	dob = models.DateField(null=True,blank=True)
	photo = models.ImageField(null=True,blank=True)
		
def create_slug(instance,new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = post.objects.filter(slug=slug).order_by("-id")
	if qs.exists():
		new_slug = "%s-%s"%(slug,qs[0].id)
		return create_slug(instance,new_slug)
	return slug
def receive_slug(instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
pre_save.connect(receive_slug,sender=post)

