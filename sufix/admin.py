# -*- coding: utf-8 -*-
from django.db.models import F
from django.contrib import admin
from .models import *
from django import forms

# Globally disable delete selected
admin.site.disable_action('delete_selected')

def make_all_delete(modeladmin, request, queryset):
    queryset.delete()
make_all_delete.short_description = "Delete selected"



class PartnersDetailsInline(admin.StackedInline):
    model = PartnerDetails
    extra = 0
    fields = (('inn','kpp','ogrn','tel_fax','email'),('adress_legal'),('adress_actual'),('details_of_bank'))

class PartnerDescriptionInline(admin.StackedInline):
    model = PartnersDescriptions
    extra = 0

class PartnersAdmin (admin.ModelAdmin):
    list_display = ("partner_shortname","type","status")
    #list_editable = ("status","type")
    fields = ('partner_name', 'partner_shortname', ('type', 'status'))
    search_fields = ['partner_name','partner_shortname']
    list_filter = ('type', 'status')
    inlines = [PartnersDetailsInline,PartnerDescriptionInline]



class ContactDescriptionsInline(admin.StackedInline):
    model = ContactsDescriptions
    fields = ('description',)
    extra = 0

class ContactDetailsInline(admin.StackedInline):
    model = ContactDetails
    fields = ('poosition', ('email','mobile_tel', 'work_tel'), 'adress_location')
    extra = 0

class ContactsAdmin (admin.ModelAdmin):
    list_display = ('upper_case_name',"partner","active")
    #list_display_links =('last_name','first_name','patronymic')
    list_filter = ('partner','active')
    list_per_page = 10
    list_select_related = True
    fields = (('partner'),('last_name'),('first_name','patronymic'),'active')
    search_fields = ['first_name','last_name','patronymic']
    inlines = [ContactDetailsInline,ContactDescriptionsInline]
    def upper_case_name(self, obj):
      return ("%s %s %s" % (obj.first_name, obj.last_name,obj.patronymic)).upper()
    upper_case_name.short_description = 'Фамилия Имя Отчество'

class CatValWorkDescriptionInline(admin.StackedInline):
    model = CatValWorkDescription
    extra = 1

class CatValWorkInline(admin.StackedInline):
    model = CatValWork
    fields = (('work_num','work_name'), ('work_price', 'work_pir_price','unit'))
    extra = 0
    inlines = [CatValWorkDescriptionInline]


class CatValWorkAdmin(admin.ModelAdmin):
    model = CatValWork
    fields = (('work_num','work_name'), ('work_price', 'work_pir_price','unit'))
    extra = 0
    inlines = [CatValWorkDescriptionInline]


class DocsInline (admin.StackedInline):
    model = Docs
    extra = 0
    fields = [('doc_name','reg_num',),('type','status_add','status','doc_date','doc_data')]


class Docs4ProjectsInline (admin.StackedInline):
    model = Docs4Projects
    extra = 0
    fields = [('doc_name','reg_num',),('type','status_add','status','doc_date','doc_data')]

class ProjectsDescriptionsInline(admin.StackedInline):
    model = ProjectsDescriptions
    extra = 0

class ProjectsAdmin (admin.ModelAdmin):

    list_display = ("project_shortname","type","status","date_in","date_out","project_to_partner")
    fields = (('project_name'),('project_shortname', 'project_to_partner'),('date_in','date_out','date_closed'),('type','status'))
    search_fields = ['project_shortname']
    list_filter = ('type', 'status')
    inlines = [Docs4ProjectsInline,CatValWorkInline,ProjectsDescriptionsInline]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_to_partner":
            kwargs["queryset"] = Partners.objects.filter(type_id=2,status_id=1)
        return super(ProjectsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class NomenclatereInline (admin.StackedInline):
    model = OrderNomenclature
    extra = 0
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "val_work":
            kwargs["queryset"] = CatValWork.objects.filter(project_name_id=F('project_name__orders__project_name__id'))
        return super(NomenclatereInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class OrdersDescriptionsInline(admin.StackedInline):
    model = OrdersDescription
    extra = 0


class OrdersAdmin (admin.ModelAdmin):
    list_display = ("order_name", "project_name","date_in","date_out","type","status","subcontractor_name")
    fields = ('order_name',('project_name','subcontractor_name'),('date_in','date_out'),('type','status','date_inreal','date_outreal'))
    search_fields = ['order_name']
    list_filter = ('type', 'status')
    list_editable = ["status"]
    inlines = [DocsInline,NomenclatereInline,OrdersDescriptionsInline]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subcontractor_name":
            kwargs["queryset"] = Partners.objects.filter(type_id=3,status_id=1)
        return super(OrdersAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
class DocsDescriptionInline (admin.StackedInline):
    model = DocsDescription
    extra = 0

class DocsAdmin (admin.ModelAdmin):
    list_display = ("doc_name", "reg_num", "doc_date", "status", "type", "status_add")
    fields = [('doc_name', 'reg_num'), 'doc_data', ('status', 'type', 'status_add', 'doc_date')]
    inlines = [DocsDescriptionInline]


class DocsDescription4ProjectsInline (admin.StackedInline):
    model = DocsDescription4Projects
    extra = 0

class Docs4ProjectsAdmin (admin.ModelAdmin):
    list_display = ("doc_name", "reg_num", "doc_date", "status", "type", "status_add")
    fields = [('doc_name', 'reg_num'), 'doc_data', ('status', 'type', 'status_add', 'doc_date')]
    inlines = [DocsDescription4ProjectsInline]


class DocsDescription4PaymentsInline (admin.StackedInline):
    model = DocsDescription4Payments
    extra = 0

class Docs4PaymentsAdmin (admin.ModelAdmin):
    list_display = ("doc_name", "reg_num", "doc_date", "status", "type", "status_add")
    fields = [('doc_name', 'reg_num'), 'doc_data', ('status', 'type', 'status_add', 'doc_date')]
    inlines = [DocsDescription4PaymentsInline]


class Docs4PaymentsInline (admin.StackedInline):
    model = Docs4Payments
    extra = 0
class PaymentsDescriptionInline (admin.StackedInline):
    model = PaymentsDescription
    extra = 0

class PayDetailsInline (admin.StackedInline):
    model = PayDetails
    extra = 0

class PaymentsAdmin (admin.ModelAdmin):
    list_display = ("order_name", "pay_date", "status", "intention")
    fields = ['order_name', ('pay_date', 'status','intention')]
    inlines = [PayDetailsInline,PaymentsDescriptionInline]
    actions = [make_all_delete]





admin.site.register(Partners, PartnersAdmin)
admin.site.register(PartnerType)
admin.site.register(PartnerStatus)

admin.site.register(Contacts, ContactsAdmin)

admin.site.register(Projects, ProjectsAdmin)
admin.site.register(ProjectType)
admin.site.register(ProjectStatus)


admin.site.register(Orders, OrdersAdmin)
#admin.site.register(OrderNomenclature)
#admin.site.register(CatValWork, CatValWorkAdmin)


admin.site.register(Docs, DocsAdmin)
admin.site.register(Docs4Projects, Docs4ProjectsAdmin)
admin.site.register(Docs4Payments, Docs4PaymentsAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(PayType)
admin.site.register(PayStatus)
admin.site.register(PayIntention)


