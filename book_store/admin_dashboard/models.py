from django.db import models


# Create your models here.

class book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length= 100)
    year_of_publish = models.DateField()
    no_of_pages = models.IntegerField()
    genre = models.CharField(max_length = 100)
    price = models.FloatField()
    author = models.CharField(max_length = 100)
    book_status = models.CharField(max_length = 100)

    def __str__(self):
        return self.title
