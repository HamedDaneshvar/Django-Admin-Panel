from .models import Settings

def settings(request):
	settings = Settings.objects.first()
	return {"settings": settings,}