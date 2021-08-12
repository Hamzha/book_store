from django.db import models


# Create your models here.

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    year_of_publish = models.DateField(blank=True, null=True)
    no_of_pages = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100)
    price = models.FloatField()
    author = models.CharField(max_length=100)
    book_status = models.CharField(max_length=100, default='Pending')
    cover_photo = models.ImageField(null=True, blank=True, upload_to='images')

    def __str__(self):
        return self.title
