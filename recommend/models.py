from django.db import models

# Create your models here.
class Team(models.Model):
    team = models.CharField(max_length=255, db_column='team')
    menu = models.CharField(max_length=255, db_column='menu')
    date = models.IntegerField(db_column='date')

    class Meta:
        managed = False
        db_table = 'team_record'