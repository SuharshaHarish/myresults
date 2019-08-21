from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class StudentDetails(models.Model):
    register_number = models.CharField(max_length=20,primary_key=True)
    student_name = models.CharField(max_length=100,default='')
    student_branch = models.CharField(max_length=100,default='')

    def __str__(self):
            return self.register_number

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descripton = models.CharField(max_length=100, default='')
    city =  models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)

    def __str__(self):
            return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender= User)



class StudentResults(models.Model):
    GRADE_CHOICES=[
    ('S','S'),
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D'),
    ('F','Fail'),
    ('X','Absent'),
    ]

    subject_id = models.ForeignKey(StudentDetails, on_delete=models.CASCADE,related_name='subject_id')
    subject_name = models.CharField(max_length=100,default='')
    grade =  models.CharField(max_length=100, choices=GRADE_CHOICES,default='')

    def __str__(self):
            return self.subject_name







# Create your models here.
