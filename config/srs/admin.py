from django.contrib import admin
from .models import (
Project,Usecase,Actor,Requirement,Businessrule,Flow,Step,Message
)
from django import forms
from django.db import models


class StepInLine(admin.TabularInline):
    model = Step

class FlowAdmin(admin.ModelAdmin):
    inlines = [ StepInLine]

class StepAdmin(admin.ModelAdmin):
    list_filter = ['flow']

class FlowInLine(admin.StackedInline):
    model = Flow

class BusinessruleInLine(admin.TabularInline):
    model = Businessrule

class ActorInLine(admin.TabularInline):
    model = Actor

class RequirementInLine(admin.StackedInline):
    model = Requirement

class UsecaseAdmin(admin.ModelAdmin):
   fields = ['project','name','preconditions','postconditions']
   inlines = [ FlowInLine, BusinessruleInLine]
# Register your models here.
admin.site.register(Project)
admin.site.register(Usecase,UsecaseAdmin)
admin.site.register(Actor)
admin.site.register(Requirement)
admin.site.register(Businessrule)
admin.site.register(Flow, FlowAdmin)
admin.site.register(Step,StepAdmin)
admin.site.register(Message)

