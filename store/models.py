from django.db import models

# Create your models here.
class Info(models.Model):
    # id = models.AutoField(db_column='id', primary_key=True)
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(max_length=255, db_column='name')
    category = models.CharField(max_length=255, db_column='category')
    aver_price = models.IntegerField(db_column='aver_price')
    arrival_time = models.IntegerField(db_column='arrival_time')
    call_number = models.CharField(max_length=255, db_column='call_number')
    location = models.CharField(max_length=255, db_column='location')
    aver_rating = models.FloatField(db_column='aver_rating')
    
    class Meta:
        managed = False
        db_table = 'store_info'

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_column='user_id')
    store_id = models.IntegerField(db_column='store_id')
    store_rating = models.IntegerField(db_column='store_rating')
    comment = models.CharField(max_length=255, db_column='comment')
    date = models.IntegerField(db_column='date')

    class Meta:
        managed = False
        db_table = 'store_rating'