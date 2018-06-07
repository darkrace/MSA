
from rest_framework.serializers import (
	CharField,
	EmailField,
	ModelSerializer , 
	HyperlinkedIdentityField,
	SerializerMethodField ,
	ValidationError,
	)
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()	

class UserCreateserializer(ModelSerializer):
	email =EmailField(label='Email Adress')
	email2=EmailField(label='Confirm Email')
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'email',
			'email2',
		]
		extra_kwargs = {'password':
							{"write_only":True}
			}
	def validate(self , data):
		return data

	def validate_email(self , value):
		data = self.get_initial()
		email1 = data.get("email2")
		email2 = value
		if email1 != email2:
			raise ValidationError("Email must match")
		user_qs = User.objects.filter(email= email2)
		if user_qs.exists():
			raise ValidationError("this user already exists.")
		return value
	def validate_email2(self , value):
		data = self.get_initial()
		email1 = data.get("email")
		email2 = value
		if email1 != email2:
			raise ValidationError("Email must match")
		return value

	def create(self , validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj= User(
				username= username,
				email=email,
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data

class UserLoginserializer(ModelSerializer):
	token = CharField(allow_blank=True , read_only=True)
	username = CharField()
	email =EmailField(label='Email Adress')
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'email',
			'token',
		]
		extra_kwargs = {'password':
							{"write_only":True}
			}
	def validate(self , data):
		user_obj = None
		email = data.get("email" , None)
		username = data.get("username" , None)
		password = data["password"]
		if not email and not username:
			raise ValidationError("A user and email is required for Login")
		user = User.objects.filter(
				Q(email=email) |
				Q(username= username)
			).distinct()
		user = user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError(" this user and email is  not valid")

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials please try again.")
		data["token"] = "some random token"
		return dat

class UserDetailserializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'first_name',
			'last_name'
		]