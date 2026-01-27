from django.utils.text import slugify
from .models import Gadget

class ChallengeService:
    @staticmethod
    def create_with_specs(name: str, specs_data: dict) -> Gadget:
        """
        Üzleti logika a Gadget létrehozásához.
        Itt történhet validáció, adat-transzformáció, vagy külső API hívás.
        """
        # Példa logika: slug generálás és specifikáció tisztítás
        clean_slug = slugify(name)
        
        # Validáció (példa)
        if 'battery_capacity' not in specs_data:
            specs_data['battery_capacity'] = 'unknown'

        gadget = Gadget.objects.create(
            name=name,
            slug=clean_slug,
            specs=specs_data
        )
        return gadget
    
class InteractionService:
    @staticmethod
    def cast_vote(user, gadget_id, value):
        from .models import Vote
        # Ha már van szavazat, frissítjük, ha nincs, létrehozzuk
        vote, created = Vote.objects.update_or_create(
            user=user, 
            gadget_id=gadget_id,
            defaults={'value': value}
        )
        return vote

    @staticmethod
    def add_comment(user, gadget_id, text, image=None):
        from .models import Comment
        return Comment.objects.create(
            author=user,
            gadget_id=gadget_id,
            text=text,
            image=image
        )

class GadgetService:
    @staticmethod
    def create_gadget(name, readme_content="", main_image=None, specs=None, external_links=None):
        # Automatikus slug generálás
        slug = slugify(name)
        
        # Alapértelmezett értékek kezelése
        if specs is None: specs = {}
        if external_links is None: external_links = []
        
        # Mentés az adatbázisba
        gadget = Gadget.objects.create(
            name=name,
            slug=slug,
            readme_content=readme_content,
            main_image=main_image,
            specs=specs,
            external_links=external_links
        )
        return gadget