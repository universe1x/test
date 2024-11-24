from django.db import models
from groups.models import Group
from resume.models import Resume

class Application(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)