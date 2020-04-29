from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	score = models.IntegerField(default = 0)
	def __str__(self):
  		return self.user.username
