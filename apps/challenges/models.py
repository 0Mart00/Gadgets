from django.db import models
from apps.core.mixins import JsonQueryMixin
from django.contrib.auth.models import User



class Gadget(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    specs = models.JSONField(default=dict, blank=True)
    main_image = models.ImageField(upload_to='gadgets/%Y/%m/%d/', null=True, blank=True)
    # Stratégiai és erőforrás mezők
    operating_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    # Research Tree: Önmagára mutat, így építhető egymásra a technológia
    operating_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    prerequisite = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='unlocks'
    )

    readme_content = models.TextField(
        blank=True, 
        help_text="Írj Markdown formátumban, mint a GitHubon"
    )
    external_links = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    @property
    def total_score(self):
        # A szavazatok összegzése a property segítségével
        return sum(v.value for v in self.votes.all())


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