from django.db import models

# Create your models here.
class SearchResults(models.Model):
    id = 0
    Title = models.CharField(max_length= 20)
    Link = models.CharField(max_length = 30)
    Description = models.TextField()
    Blogger_Name = models.CharField(max_length = 10)
    Blogger_Link = models.CharField(max_length = 30)
    Post_Date = models.DateField()
    Post_Contents = models.TextField()
