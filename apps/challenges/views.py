# apps/challenges/views.py

from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .services import ChallengeService, GadgetService
import markdown
from django.utils.safestring import mark_safe

from .models import Gadget, Vote

# 1. A Dashboard a HTML megjelenítéséhez
class DashboardView(View):
    def get(self, request):
        gadgets = Gadget.objects.all().order_by('operating_cost')
        
        # Itt egy listát kellene vezetni a felhasználó által már "birtokolt" gadgetekről
        # Teszt jelleggel tegyük fel, hogy az alap cuccok (0 költség) megvannak
        user_unlocked_ids = [g.id for g in gadgets if g.operating_cost == 0]

        return render(request, 'challenges/index.html', {
            'gadgets': gadgets,
            'user_unlocked_ids': user_unlocked_ids
        })
@method_decorator(csrf_exempt, name='dispatch')
class GadgetCreateView(View):
    def get(self, request):
        return render(request, 'challenges/create_gadget.html')

    def post(self, request):
        # A Service-t hívjuk meg itt is!
        gadget = GadgetService.create_gadget(
            name=request.POST.get('name'),
            readme_content=request.POST.get('readme_content'),
            main_image=request.FILES.get('main_image')
        )
        return redirect('challenges:detail', slug=gadget.slug)
        
class GadgetDetailView(View):
    def get(self, request, slug):
        gadget = get_object_or_404(Gadget, slug=slug)
        # Markdown konvertálása HTML-re
        readme_html = mark_safe(markdown.markdown(gadget.readme_content, extensions=['extra', 'codehilite']))
        
        comments = gadget.comments.all().order_by('-created_at')
        return render(request, 'challenges/detail.html', {
            'gadget': gadget, 
            'readme_html': readme_html,
            'comments': comments
        })
    def post(self, request, slug):
        gadget = get_object_or_404(Gadget, slug=slug)
        text = request.POST.get('text')
        image = request.FILES.get('image') # Itt kapjuk el a képet!

        if text:
            from .models import Comment
            Comment.objects.create(
                gadget=gadget,
                author=request.user,
                text=text,
                image=image
            )
        
        return redirect('challenges:detail', slug=slug)


@method_decorator(csrf_exempt, name='dispatch')
class GadgetAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            gadget = GadgetService.create_gadget(
                name=data.get('name'),
                readme_content=data.get('readme', ""),
                specs=data.get('specs', {}),
                external_links=data.get('links', [])
            )
            return JsonResponse({
                "status": "success",
                "slug": gadget.slug,
                "url": f"/gadget/{gadget.slug}/"
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)



class GadgetVoteView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Be kell jelentkezned!'}, status=403)
            
        data = json.loads(request.body)
        value = int(data.get('value', 0))
        
        if value not in [1, -1]:
            return JsonResponse({'status': 'error', 'message': 'Érvénytelen érték.'}, status=400)

        # Szavazat mentése vagy frissítése
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            gadget_id=pk,
            defaults={'value': value}
        )

        # Új összpontszám kiszámítása
        gadget = Gadget.objects.get(pk=pk)
        total_score = sum(v.value for v in gadget.votes.all())

        return JsonResponse({
            'status': 'success',
            'total_score': total_score
        })