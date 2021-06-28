from django.db import models

# Create your models here.
# class Tenant(models.Model):
#     name = models.CharField(max_length=200)
#     Subdomain = models.CharField(max_length=200)

# class TenantAwareModel(models.Model):
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

# class Member(TenantAwareModel):
#     name = models.CharField(max_length=200)