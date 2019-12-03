from .models import Usecase, Scenario, Step, ArtifactFieldValues,ArtifactFields,Field,FieldValues,ArtifactType
from django.forms import ModelForm
from django import forms
from .models import Artifact
from django.shortcuts import get_object_or_404

class UsecaseForm(ModelForm):
    class Meta:
        model = Usecase
        fields = ['name','description','preConditions','postConditions']

class ArtifactForm(ModelForm):
    artifact_type_id = None

    class Meta:
        model = Artifact
        fields = ['name','project']

    def form_valid(self, form):
        print('reached form.valid function...')
        self.artifact_type_id = self.kwargs['artifact_type_id']
        artifacttype = get_object_or_404(ArtifactType,id=self.artifact_type_id)
        form.instance.type = artifacttype
        return super(ArtifactForm, self).form_valid(form)

class ArtifactDetailsForm(forms.Form):
    empty = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        artifact = kwargs.pop('artifact')
        artifactfields = ArtifactFields.objects.filter(artifactType=artifact.type)
        super(ArtifactDetailsForm, self).__init__(*args, **kwargs)
        # ("Text Field", "Text Field"),
        # ("Text Area", "Text Area"),
        # ("Drop Down", "Drop Down"),
        # ("Radio", "Radio"),
        # ("Checkbox", "checkbox")
        for f in artifactfields:
            fieldvalue = ArtifactFieldValues.objects.filter(artifact=artifact, artifactField=f).first()
            if not fieldvalue:
                fieldvalue = ArtifactFieldValues()
            choices = []
            for choice in f.field.options.all():
                choices.append((choice.id, choice.value))

            if f.field.widgetType == 'Radio':
                self.fields['custom_%s' %f.id] = forms.ChoiceField(label=f.field.label,
                                                                         choices=choices,
                                                                         widget=forms.RadioSelect)
                self.fields['custom_%s' % f.id].initial = fieldvalue.value

            elif f.field.widgetType == 'Text Field':
                self.fields['custom_%s' %f.id] = forms.CharField(label=f.field.label)
                self.fields['custom_%s' % f.id].initial = fieldvalue.value
            elif f.field.widgetType == 'Checkbox':
                self.fields['custom_%s' % f.id] = forms.MultipleChoiceField(label=f.field.label,
                                                                    widget=forms.CheckboxSelectMultiple,
                                                                    choices=choices)
                self.fields['custom_%s' % f.id].initial = fieldvalue.value
            elif f.field.widgetType == 'Drop Down':
                self.fields['custom_%s' %f.id] = forms.ChoiceField(label=f.field.label,
                                                                    widget=forms.Select,
                                                                    choices=choices)
                self.fields['custom_%s' % f.id].initial = fieldvalue.value

            elif f.field.widgetType == 'Text Area':
                self.fields['custom_%s' %f.id] = forms.CharField(label=f.field.label,widget=forms.Textarea)
                self.fields['custom_%s' % f.id].initial = fieldvalue.value



    def field_values(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (name.split('_')[1], value)

