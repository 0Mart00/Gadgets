import os
from django.core.files.storage import default_storage
from .models import Submission, Gadget

class FileProcessor:
    @staticmethod
    def handle_upload(gadget_id: int, file_obj) -> Submission:
        """
        Fájl mentése, validálása és Submission rekord létrehozása.
        """
        # 1. Fájl mentése (Storage réteg)
        file_name = f"vault/{gadget_id}/{file_obj.name}"
        saved_path = default_storage.save(file_name, file_obj)
        
        # 2. Üzleti logika (pl. vírusellenőrzés placeholder)
        is_safe = True 
        
        # 3. Rekord létrehozása
        submission = Submission.objects.create(
            gadget_id=gadget_id,
            file_path=saved_path,
            status='verified' if is_safe else 'rejected'
        )
        return submission