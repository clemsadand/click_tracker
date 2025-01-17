from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Click
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def increment_click(request):
    try:
        if request.method == 'POST':
            label = request.POST.get('label')
            session_key = request.session.session_key

            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            click, _ = Click.objects.get_or_create(label=label, session_key=session_key)
            click.increment()

            request.session['last_click_label'] = label
            return JsonResponse({"label": label, "count": click.count})

        return JsonResponse({"error": "Invalid request method."}, status=405)
    except Exception as e:
        logger.error(f"Error in increment_click: {e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def undo_last_click(request):
    try:
        if request.method == 'POST':
            session_key = request.session.session_key
            label = request.session.get('last_click_label')

            if not label:
                return JsonResponse({"error": "No click to undo."}, status=400)

            try:
                click = Click.objects.get(label=label, session_key=session_key)
                click.decrement()
                request.session['last_click_label'] = None
                return JsonResponse({"label": label, "count": click.count})
            except Click.DoesNotExist:
                return JsonResponse({"error": "Click not found."}, status=404)

        return JsonResponse({"error": "Invalid request method."}, status=405)
    except Exception as e:
        logger.error(f"Error in undo_last_click: {e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def clear_all(request):
    try:
        if request.method == "POST":
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            Click.objects.filter(session_key=session_key).update(count=0)
            return JsonResponse({"success": "All button counts have been reset!"})

        return JsonResponse({"error": "Invalid request method"}, status=400)
    except Exception as e:
        logger.error(f"Error in clear_all: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def get_chart_data(request):
    try:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        buttons = Click.objects.filter(session_key=session_key)
        total = sum([button.count for button in buttons])

        if total == 0:
            return JsonResponse([], safe=False)

        data = [{"label": button.label, "count": button.count * 100 / total} for button in buttons]
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(f"Error in get_chart_data: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def index(request):
    buttons = ['<=14', '15', '16', '17', '18', '19', '20>=']
    return render(request, 'tracker/index.html', {'buttons': buttons})

