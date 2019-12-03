from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Usecase(models.Model):
    name = models.CharField(max_length=200)
    preconditions = models.TextField()
    postconditions = models.TextField()
    project = models.ForeignKey(Project,models.DO_NOTHING,related_name='usecases')

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=200)
    usecase = models.ManyToManyField(Usecase,null=True,blank=True,related_name='actors')

class Requirement(models.Model):
    FUNCTIONAL = 1
    NON_FUNCTIONAL = 2
    REQUIREMENTS_TYPE = (
        (FUNCTIONAL,'Functional'),
        (NON_FUNCTIONAL,'Non-Functional')
    )
    description = models.TextField()
    requiremnt_type  = models.PositiveIntegerField(
        choices=REQUIREMENTS_TYPE,
        default=FUNCTIONAL
    )
    usecases = models.ManyToManyField(Usecase,blank=True,null=True)

    def __str__(self):
        return self.description

class Businessrule(models.Model):
    name = models.CharField(max_length=200)
    usecase = models.ForeignKey(Usecase,on_delete=models.DO_NOTHING, blank=True,null=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    WARNING = 1
    ERROR = 2
    INFO = 3
    SMS = 4
    EMAIL = 5
    GENERAL = 6
    MESSAGE_TYPE = (
        (WARNING,'Warning'),
        (ERROR,'Error'),
        (INFO,'Information'),
        (SMS,'SMS'),
        (EMAIL,'Email'),
        (GENERAL,'General')
    )

    en_message = models.CharField(max_length=200)
    ar_message = models.CharField(max_length=200)

    def __str__(self):
        return self.en_message


class Flow(models.Model):
    NORMAL_FLOW = 1
    ALTERNATE_FLOW = 2
    EXCEPTION_FLOW = 3
    FLOW_TYPE = (
        (NORMAL_FLOW,'Normal Flow'),
        (ALTERNATE_FLOW,'Alternate Flow'),
        (EXCEPTION_FLOW,'Exceptional Flow')
    )
    name = models.CharField(max_length=200)
    flow_type = models.PositiveIntegerField(
        choices=FLOW_TYPE,default=NORMAL_FLOW
    )
    usecase = models.ForeignKey(Usecase,on_delete=models.CASCADE , related_name='flows')

    def __str__(self):
        return self.usecase.name+' - '+self.name

class Step(models.Model):
    description = models.CharField(max_length=200)
    flow = models.ForeignKey(Flow,on_delete=models.CASCADE, related_name='steps')
    messages = models.ManyToManyField(Message,related_name='steps', blank=True,null=True)

    def __str__(self):
        return self.description

