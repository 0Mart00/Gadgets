from django.db import models
from apps.core.mixins import JsonQueryMixin
from django.contrib.auth.models import User


class Gadget(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    specs = models.JSONField(default=dict, blank=True)
    # Új mezők a README és a főkép számára
    readme_content = models.TextField(blank=True, help_text="Írj Markdown formátumban, mint a GitHubon")
    external_links = models.JSONField(default=list, blank=True) # [ {"label": "Docs", "url": "..."}, ... ]
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Comment(models.Model): # <--- Figyelj a nagybetűs Model-re és a szülőosztályra!
    gadget = models.ForeignKey('Gadget', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='comments/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.gadget.name}"

class Vote(models.Model):
    VOTE_CHOICES = ( (1, 'Up'), (-1, 'Down') )
    gadget = models.ForeignKey('Gadget', on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('gadget', 'user') # Egy felhasználó csak egyszer szavazhat egy gadgetre