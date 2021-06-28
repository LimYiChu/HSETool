from .models import Tenant

def get_hostname(request):
    return request.get_host().split(':')[0].lower()

def get_tenant(request):
    hostname = get_hostname(request)
    Subdomain = hostname.split('.')[0]
    return Tenant.objects.filter(Subdomain=Subdomain).first()