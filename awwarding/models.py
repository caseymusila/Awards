from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
  user=models.OneToOneField(User, on_delete = models.CASCADE)
  image=CloudinaryField('Profile Picture')
  bio =  models.TextField()
  location = models.CharField(max_length = 40)
  email = models.EmailField()
  link = models.URLField()

  def __str__(self):
    return self.user.username

  def save_profile(self):
    self.save()

  def delete_profile(self):
    self.delete() 

  def edit_bio(self, new_bio):
    self.bio = new_bio
    self.save()