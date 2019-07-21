from django.contrib import admin
from app.models import *


class AccessLevelAdmin(admin.ModelAdmin):
    model = AccessLevel

admin.site.register(AccessLevel, AccessLevelAdmin)


class PermitAdmin(admin.ModelAdmin):
    list_display = ['number', 'get_person', 'date_from', 'date_to', 'level', 'status']
    list_filter = ['status']
    search_fields = ['number']
    model = Permit

    def get_person(self, obj):
        try:
            person = Person.objects.get(permit__token=obj.token)
            return person
        except Person.DoesNotExist:
            return '-'
    get_person.short_description = 'Сотрудник'

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
    list_filter = ['contractor__username']

    inlines = [
        DocumentInline,
        EquipmentInline
    ]

admin.site.register(Person, PersonAdmin)


class TypeDocumentAdmin(admin.ModelAdmin):
    model = TypeDocument

admin.site.register(TypeDocument, TypeDocumentAdmin)


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['person', 'get_contractor', 'date_from', 'date_to', 'type_doc', 'status']
    list_filter = ['type_doc', 'status', 'person__contractor']
    search_fields = ['person__last_name']

    def get_contractor(self, obj):
        return obj.person.contractor
    get_contractor.short_description = 'Подрядчик'


admin.site.register(Document, DocumentAdmin)


class EquipmentTypeAdmin(admin.ModelAdmin):
    model = EquipmentType

admin.site.register(EquipmentType, EquipmentTypeAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment
    list_display = ['person', 'type_eq', 'number', 'access']
    list_filter = ['type_eq']
    search_fields = ['number']

admin.site.register(Equipment, EquipmentAdmin)


class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(Event, EventAdmin)
