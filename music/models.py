from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField()
    last_update = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

class Albom(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    cover = models.URLField()
    last_update = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

class Songs(models.Model):
    title = models.CharField(max_length=100)
    cover = models.URLField()
    albom = models.ForeignKey(Albom, on_delete=models.CASCADE, null=True)
    listened = models.PositiveBigIntegerField(default=0)
    last_update = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['id'])
        ]