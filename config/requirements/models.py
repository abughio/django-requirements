from django.db import models

class ArtifactType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Artifact(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ArtifactType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='artifacts', blank=True, null=True)

    def __str__(self):
        return self.name

class LinkType(models.Model):
    name = models.CharField(max_length=200)
    reverseName = models.CharField(max_length=200)

    def __str__(self):
        return self.name+" -  "+self.reverseName

    def getName(self):
        return self.name

    def getReverseName(self):
        return self.reverseName

class LinksAllowed(models.Model):
    linkType = models.ForeignKey(LinkType, on_delete=models.CASCADE, related_name='allowed_linked')
    source = models.ForeignKey(ArtifactType, on_delete=models.CASCADE, related_name='source_links')
    target = models.ForeignKey(ArtifactType, on_delete=models.CASCADE, related_name='target_links')

    def __str__(self):
        return self.source.__str__()+" "+self.linkType.getName()+" "+self.target.__str__()+" and "+self.target.__str__()\
               +" "+self.linkType.getReverseName()+" "+self.source.__str__()

class Link(models.Model):
    linkType = models.ForeignKey(LinkType, on_delete=models.CASCADE, related_name='links')
    source = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='source_links')
    target = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='target_links')

    def __str__(self):
        return self.source.__str__()+" "+self.linkType.getName()+" "+self.target.__str__()+" and "+self.target.__str__()\
               +" "+self.linkType.getReverseName()+" "+self.source.__str__()


class Field(models.Model):
    WIDGET_TYPES = (
        ("Text Field", "Text Field"),
        ("Text Area", "Text Area"),
        ("Drop Down", "Drop Down"),
        ("Radio", "Radio"),
        ("Checkbox", "checkbox")
    )
    INPUT_TYPES = (
        ("Numberic", "Numberic"),
        ("Text","Text"),
        ("Boolean","Boolean")
    )
    label = models.CharField(max_length=200)
    HelpText = models.TextField
    widgetType = models.CharField(max_length=200, choices=WIDGET_TYPES)
    valueType = models.CharField(max_length=200,choices=INPUT_TYPES)

    def __str__(self):
        return self.label

class FieldValues(models.Model):
    value = models.CharField(max_length=500)
    field = models.ForeignKey(Field,on_delete=models.CASCADE,related_name="options")

    def __str__(self):
        return self.value+" "+self.field.__str__()


class ArtifactFields(models.Model):
    artifactType = models.ForeignKey(ArtifactType, on_delete=models.CASCADE,related_name="fields")
    field = models.ForeignKey(Field,on_delete=models.CASCADE,related_name="artifacts")
    required = models.BooleanField(default=True)
    inputValues = models.IntegerField(null=True)

    def __str__(self):
        return self.artifactType.__str__()+" - "+self.field.__str__()

class ArtifactFieldValues(models.Model):
    value = models.CharField(max_length=500)
    artifactField = models.ForeignKey(ArtifactFields,on_delete=models.CASCADE, related_name="value")
    artifact = models.ForeignKey(Artifact,on_delete=models.CASCADE,related_name='fieldvalues')

    def __str__(self):
        return " {}.{} = {}".format(self.artifact.name, self.artifactField.field.label,self.value)

class Usecase(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    preConditions = models.CharField(max_length=2000)
    postConditions = models.CharField(max_length=2000)

    def __str__(self):
        return  self.name

class Scenario(models.Model):
    SCENARIO_TYPES = (
        ("Normal Flow", "Normal Flow"),
        ("Alternate Flow", "Alternate Flow"),
        ("Exception Flow", "Exception Flow")
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=SCENARIO_TYPES)
    usecase = models.ForeignKey(Usecase,on_delete=models.CASCADE,related_name="scenarios")

    def __str__(self):
        return self.type.__str__()+" - "+self.name.__str__()

class Step(models.Model):
    stepNo = models.IntegerField()
    description = models.CharField(max_length=500)
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE,related_name="steps")

    def __str__(self):
        return self.stepNo.__str__()+". "+self.description.__str__()
