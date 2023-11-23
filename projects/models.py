#from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model





class Project(models.Model):
    STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('Incompleted', 'Incompleted'),
        ('Completed', 'Completed'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Not Started')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week = models.IntegerField(choices=[(i, f"Week {i}") for i in range(1, 11)], null=True)




    def __str__(self):
        return self.name

    def update_status(self):
        steps = self.steps.all()
        if not steps:
            self.status = "Not Started"
            self.save()
            return
        if all(step.status == "Completed" for step in steps):
            self.status = "Completed"
        elif any(step.status in ["In Progress", "Not Started"] for step in steps):
            self.status = "Incompleted"
        else:
            self.status = "Completed"
        self.save()

class Step(models.Model):
    STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Not Started')

    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    study_id = models.CharField(max_length=50)
    condition = models.TextField()
    notes = models.TextField()



