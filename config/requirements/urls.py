from django.urls import path
from . import views

app_name = 'requirements'

urlpatterns = [
    path('artifacttypes/<int:artifact_type_id>/',views.artifactList, name='artifact-list'),
    path('artifacttypes/<int:artifact_type_id>/create/',views.ArtifactCreate.as_view(), name='artifact-create'),
    path('artifact/<int:artifact_id>/dynamicdetails/',views.ArtifactDetailsView,name='aritifact-details'),
    path('artifact/<int:artifact_id>/details/',views.artifactFields,name="artifact-fields"),
    path('projectslist/',views.ProjectList,name='projectlist'),
    path('export/<int:project_id>/',views.TestDocument,name='export-doc'),
    path('',views.home,name="home"),


]
