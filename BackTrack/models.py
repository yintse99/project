from django.db import models

# Create your models here.

class Manager(models.Model):
    name = models.CharField(max_length=60)
    icon = models.ImageField(max_length=100,blank=True,null=True)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['username'],name='unique manager username'),
        ]

class Developer(models.Model):
    name = models.CharField(max_length=60)
    icon = models.ImageField(max_length=100,blank=True,null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE,blank=True,null=True, related_name='Project')
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['username'],name='unqiue developer username'),
        ]

class Project(models.Model):
    name = models.CharField(max_length=200)
    scrum_master = models.ForeignKey(Manager, on_delete=models.CASCADE)
    product_owner = models.ForeignKey('Developer', on_delete=models.CASCADE, related_name='ProductOwner')
    current_sprint_number = models.CharField(max_length=4)


class ProductBacklog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,blank=True,null=True)
    size = models.DecimalField(max_digits=3, decimal_places=1)
    sprintbacklog = models.ForeignKey('SprintBacklog', on_delete=models.CASCADE, blank=True,null=True, related_name='sprintbacklog')
    status = models.CharField(max_length=1)
    order = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['name'],name='unqiue pbi'),
            models.UniqueConstraint(fields= ['order'],name='unique order'),
        ]

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='project2')
    sprint_number = models.CharField(max_length=4)
    capacity = models.IntegerField()

class SprintBacklog(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE,related_name='sprint')
    pbi= models.ForeignKey(ProductBacklog, on_delete=models.CASCADE,related_name='pbi')
    estimated_time = models.DecimalField(max_digits=3, decimal_places=2)
    time_spent = models.DecimalField(max_digits=3, decimal_places=2)

class Task(models.Model):
    sprint = models.ForeignKey(SprintBacklog, on_delete=models.CASCADE)
    task_to_do = models.CharField(max_length=200)
    time = models.DecimalField(max_digits=3,decimal_places=2)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE,blank=True,null=True)
