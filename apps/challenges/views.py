# apps/challenges/views.py

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Gadget
from .services import ChallengeService

# 1. A Dashboard a HTML megjelenítéséhez
class DashboardView(View):
    def get(self, request):
        gadgets = Gadget.objects.all().order_by('-created_at')
        stats = {
            "total_gadgets": gadgets.count(),
        }
        return render(request, 'challenges/index.html', {
            'gadgets': gadgets,
            'stats': stats
        })

# 2. Az API a létrehozáshoz
@method_decorator(csrf_exempt, name='dispatch')
class GadgetCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            specs = data.get('specs', {})

            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)

            gadget = ChallengeService.create_with_specs(name=name, specs_data=specs)

            return JsonResponse({
                "id": gadget.id,
                "slug": gadget.slug,
                "message": "Gadget created"
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)