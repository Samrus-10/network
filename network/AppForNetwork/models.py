from django.db import models
from .validators import validate_file_extension

# Create your models here.

class Users(models.Model):
    
    login = models.CharField(max_length = 20)
    password = models.CharField(max_length = 10)
    admin = models.IntegerField()

class NETWORKS(models.Model):
    
    id_admin = models.ForeignKey(Users, on_delete = models.CASCADE)

class PARAMS(models.Model):
    
    id_network = models.ForeignKey(NETWORKS, on_delete = models.CASCADE)
    
    name = models.CharField(max_length = 30)
    amount_params = models.IntegerField()
    amount_network = models.IntegerField()
    amount_layers = models.IntegerField()
    name_function = models.CharField(max_length = 30)
    accuracy = models.IntegerField()
    max_time = models.CharField(max_length = 30)
    classs = models.CharField(max_length = 30)

class DESCRIPTIONS(models.Model):

    id_network = models.ForeignKey(NETWORKS, on_delete = models.CASCADE)

    short_text = models.TextField()
    long_text = models.TextField()

class COMMENTS(models.Model):
    
    id_network = models.ForeignKey(NETWORKS, on_delete = models.CASCADE)

    number_param = models.IntegerField()
    comment = models.TextField()

class DATASET(models.Model):
    
    id_network = models.ForeignKey(NETWORKS, on_delete = models.CASCADE)

    file_name = models.TextField()

class RESULT_TEACHING(models.Model):
    
    id_network = models.ForeignKey(NETWORKS, on_delete = models.CASCADE)

    file_name = models.TextField()
    information_teach = models.TextField()
    result_teach = models.TextField()
    
class FILE_EXEL(models.Model):

    id_network = models.ForeignKey(NETWORKS, on_delete = models.CASCADE)
    
    file = models.FileField(upload_to="static/exel", validators=[validate_file_extension])
    
