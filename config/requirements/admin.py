from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ArtifactType)
admin.site.register(models.Project)
admin.site.register(models.Artifact)
admin.site.register(models.Link)
admin.site.register(models.LinkType)
admin.site.register(models.LinksAllowed)
admin.site.register(models.Field)
admin.site.register(models.FieldValues)
admin.site.register(models.ArtifactFields)
admin.site.register(models.ArtifactFieldValues)
admin.site.register(models.Usecase)
admin.site.register(models.Scenario)
admin.site.register(models.Step)
