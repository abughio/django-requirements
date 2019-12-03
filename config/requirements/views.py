from io import StringIO,BytesIO

from django.shortcuts import get_object_or_404, render, redirect,render_to_response,reverse
from django.utils.six import StringIO
from django.views.generic import (
    ListView, DetailView, UpdateView,
    CreateView
)
from docx import *
from docx.shared import Inches
from datetime import date
from .documentexport import DocumentToExport
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import modelform_factory

from django.conf import settings
from .forms import UsecaseForm, ArtifactDetailsForm, ArtifactForm
from .models import ArtifactType, Artifact, ArtifactFields, FieldValues, ArtifactFieldValues, LinksAllowed, LinkType, \
    Project



def ProjectList(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, template_name="requirements/projectlist.html", context=context)


# Create your views here.
def TestDocument(request,project_id):
    document = DocumentToExport(project_id)
    docx_title = "TEST_DOCUMENT.docx"
    # Prepare document for download
    # -----------------------------
    f = BytesIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response


def usecaseCreate(request):
   form = UsecaseForm()
   context = {"usecaseform":form}
   return render(request,template_name="requirements/usecase-create.html",context=context)

def home(request):
    artifactTypes = ArtifactType.objects.all()
    context = { 'message':"hello World!! from requirements home page.",
                'artifactTypes':artifactTypes
    }
    return render(request, template_name="requirements/home.html", context=context)

def artifactList(request, artifact_type_id):
    artifactType = get_object_or_404(ArtifactType, id=artifact_type_id)
    artifactList = Artifact.objects.filter(type=artifactType)
    print(artifact_type_id)
    form = None
    if request.method == 'POST':
        form = ArtifactForm(request.POST)
        form.artifact_type_id = artifact_type_id
        form.instance.type = artifactType
        if form.is_valid():
            form.save()
    else:
        form = ArtifactForm()

    context = {'artifactList': artifactList,'form':form,'artifacttype':artifactType
               }
    return render(request, template_name="requirements/artifactlist.html", context=context)

def artifactCreate(request, artifact_type_id):
    if request.method == 'POST':
            form = ArtifactForm(request.POST)
            if form.is_valid():
                #save the form.
                return HttpResponseRedirect('/thanks/')
    else:
        form = ArtifactForm()
    context = {'form':form
    }
    return render(request, template_name="requirements/createartifact.html",context=context)

def artifactFields(request, artifact_id):
    form = []
    values = []
    artifact = get_object_or_404(Artifact,id=artifact_id)
    fields = ArtifactFields.objects.filter(artifactType=artifact.type)

    if request.method == 'POST':
        #save the form.
        # create Field values object
        # fill it with values from form
        # save the object.
        for f in fields:
            value = request.POST[f.field.label]
            if value:
                fieldvalue = ArtifactFieldValues.objects.filter(artifact = artifact,artifactField=f).first()
                if not fieldvalue:
                    #save
                    fieldvalue = ArtifactFieldValues()
                fieldvalue.value = value
                fieldvalue.artifactField = f
                fieldvalue.artifact = artifact
                fieldvalue.save()
                f.field.valueType = value
            form.append(f.field)
            return redirect("requirements:artifact-list",artifact.type.id)
    else:

        print(artifact)
        for f in fields:
            fieldvalue = ArtifactFieldValues.objects.filter(artifact=artifact, artifactField=f).first()
            if fieldvalue:
                f.field.valueType = fieldvalue.value
            form.append(f.field)

    context = {"form":form,"artifact":artifact
    }
    return render(request,template_name="requirements/artifactdetails.html",context=context)


class ArtifactCreate(CreateView):
    model = Artifact
    fields = (
        'name', 'project'
    )
    artifact_type_id = None

    def get_success_url(self):
        return reverse('requirements:home')

    def get_context_data(self, *args, **kwargs):
        context = super(ArtifactCreate, self).get_context_data(*args, **kwargs)
        self.artifact_type_id = self.kwargs['artifact_type_id']
        artifacttype = get_object_or_404(ArtifactType, id=self.artifact_type_id)
        context['artifacttype'] = artifacttype
        return context

    def form_valid(self, form):
        self.artifact_type_id = self.kwargs['artifact_type_id']
        artifacttype = get_object_or_404(ArtifactType,id=self.artifact_type_id)
        form.instance.type = artifacttype
        return super(ArtifactCreate, self).form_valid(form)


def ArtifactDetailsView(request,artifact_id):
    artifact = get_object_or_404(Artifact, id=artifact_id)
    form = ArtifactDetailsForm(request.POST or None,artifact=artifact)
    if form.is_valid():
        for (afid, value) in form.field_values():
            save_values(request,afid,value,artifact)
        return redirect("requirements:artifact-list",artifact.type.id)

    context = {'form':form,'artifact':artifact.name}
    return render(request,template_name="requirements/dynamic_form.html", context = context)

def save_values(request,afid,value,artifact):
    f = ArtifactFields.objects.filter(id=afid).first()
    fieldvalue = ArtifactFieldValues.objects.filter(artifact=artifact, artifactField=f).first()
    if not fieldvalue:
        # save
        fieldvalue = ArtifactFieldValues()
    fieldvalue.value = value
    fieldvalue.artifact = artifact
    fieldvalue.artifactField = f
    fieldvalue.save()
    return True