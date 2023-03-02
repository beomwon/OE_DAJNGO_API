from django.db import models
# from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    email = models.CharField(max_length=255, db_column='email', unique=True, default='')
    password = models.CharField(max_length=255, db_column='password')
    name = models.CharField(max_length=255, db_column='name')
    department = models.CharField(max_length=255, db_column='department', default='')
    phone = models.CharField(max_length=255, db_column='phone', default='')

    class Meta:
        db_table = 'user'

class Preference(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255, db_column='category')
    preference = models.IntegerField(db_column='preference')
    user_id = models.IntegerField(db_column='user_id')

    class Meta:
        managed = False
        db_table = 'food_preference'

class MustFood(models.Model):
    user_id = models.IntegerField(db_column='user_id')
    category = models.CharField(max_length=255, db_column='category')
    preference = models.IntegerField(db_column='preference')
    date = models.IntegerField(db_column='date')

    class Meta:
        managed = False
        db_table = 'must_food'