
from .models import *
def load_versioning(request):

    versioning = str(Parameters.objects.all().first().Versioning)

    return {"Version" : versioning}