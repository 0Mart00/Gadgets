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