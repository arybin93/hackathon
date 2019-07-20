from django.contrib import admin
from app.models import *


class AccessLevelAdmin(admin.ModelAdmin):
    model = AccessLevel

admin.site.register(AccessLevel, AccessLevelAdmin)


class PermitAdmin(admin.ModelAdmin):
    list_display = ['number', 'date_from', 'date_to', 'level', 'status']
    model = Permit

admin.site.register(Permit, PermitAdmin)


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 0


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['first_name', 'last_name', 'position', 'contractor', 'permit', 'status']
    search_fields = ['first_name', 'last_name', 'position']

    inlines = [
        DocumentInline,
        EquipmentInline
    ]

admin.site.register(Person, PersonAdmin)


class TypeDocumentAdmin(admin.ModelAdmin):
    model = TypeDocument

admin.site.register(TypeDocument, TypeDocumentAdmin)


class DocumentAdmin(admin.ModelAdmin):
    model = TypeDocument

admin.site.register(Document, DocumentAdmin)


class EquipmentTypeAdmin(admin.ModelAdmin):
    model = EquipmentType

admin.site.register(EquipmentType, EquipmentTypeAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment

admin.site.register(Equipment, EquipmentAdmin)


class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(Event, EventAdmin)
