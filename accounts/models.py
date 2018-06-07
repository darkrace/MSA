from django.db import models
from django.conf import settings
from .utils import code_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import (
	AbstractBaseUser , BaseUserManager
	)

class UserManager(BaseUserManager):
	def create_user(self , email , full_name=None , password=None , is_active=True , is_staff=False , is_admin=False ):
		if not email:
			raise ValueError("User must have an email")
		if not password:
			raise ValueError("User must have password")
		user_obj = self.model(
			email = self.normalize_email(email),
			full_name = full_name
			)
		user_obj.set_password(password)
		user_obj.staff  = is_staff
		user_obj.admin  = is_admin
		user_obj.active = is_active
		user_obj.save(using= self._db)
		return user_obj

	def create_stuffuser(self , email ,full_name=None, password=None):
		user = self.create_user(
			email,
			full_name=full_name,
			password=password,
			is_staff=True,
			)
		return user

	def create_superuser(self , email ,full_name=None, password=None):
		user = self.create_user(
			email,
			full_name=full_name,
			password=password,
			is_admin=True,
			is_staff=True,
			)
		return user

class User(AbstractBaseUser):
	email 			 = models.EmailField(max_length=255 , unique=True)
	full_name 	 	 = models.CharField(max_length=255 , blank=True , null=True)
	active 		 	 = models.BooleanField(default=True)
	activation_key	 = models.CharField(max_length=120 , blank=True , null=True)
	staff 		 	 = models.BooleanField(default=False)
	admin 		  	 = models.BooleanField(default=False)
	timestamp		 = models.DateTimeField(auto_now_add=True)

	
	USERNAME_FIELD  = 'email'

	REQUIRED_FIELDS = [email]

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		if self.full_name:
			return self.full_name
		return self.email

	def get_short_name(self):
		return self.email

	def has_perm(self , perm , obj=None):
		return True
	def has_module_perms(self , app_lable):
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

	def send_activation_email(self):
		if not self.is_active:
			self.activation_key = code_generator()
			self.save()
			path_ 			= reverse('activate' , kwargs={"code": self.activation_key})
			subject 		= 'Activate Account'
			from_email  	= settings.DEFAULT_FROM_EMAIL
			message 		= f'activate your acount here: {path_}'
			recipient_list  = [self.email]
			html_message 	= f'<p>activate your acount here:{path_}</p>'
			print(html_message)
			sent_mail 	 	= send_mail(
									subject,
									message, 
									from_email, 
									recipient_list, 
									fail_silently=False, 
									html_message=html_message)

			return sent_mail

class SubUser(models.Model):
	owner 	  	 = models.ForeignKey(User , on_delete=None)
	name 	  	 = models.CharField(max_length=120)
	email	  	 = models.CharField(max_length=120 , null=True , blank=True)
	icon      	 = models.ImageField( null=True , blank=True )
	timestamp 	 = models.DateTimeField(auto_now_add=True)
	slug  	  	 = models.SlugField(unique=True , null=True , blank=True)
	active 	  	 = models.BooleanField(default=False)
	admin_active = models.BooleanField(default=False)



