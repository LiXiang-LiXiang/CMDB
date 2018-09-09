from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Asset, Server, NetworkDevice, Software, CPU, RAM, Disk, NIC, RaidAdaptor, \
    Manufactory, BusinessUnit, Contract, IDC, Tag, EventLog, NewAssetApprovalZone


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    list_filter = ('user', 'phone', 'token')

class BaseAdmin(object):
    """自定义admin类"""

    choice_fields = []
    fk_fields = []
    dynamic_fk = None
    dynamic_list_display = []
    dynamic_choice_fields = []
    m2m_fields = []


class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    #readonly_fields = ['create_date']

class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']

class NICInline(admin.TabularInline):
    model = models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']

class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']

class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','asset_type','sn','name','manufactory','management_ip','idc','business_unit','admin','trade_date')
    inlines = [ServerInline,CPUInline,RAMInline,DiskInline,NICInline]
    search_fields = ['sn',]
    # list_filter = ['idc','manufactory','business_unit','asset_type']
    choice_fields = ('asset_type')
    fk_fields = ('manufactory','idc','business_unit','admin')
    list_per_page = 10
    list_filter = ('asset_type','manufactory','idc','business_unit','admin','trade_date')
    dynamic_fk = 'asset_type'
    dynamic_list_display = ('model','sub_asset_type','os_type','os_distribution')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)

class NicAdmin(admin.ModelAdmin):
    list_display = ('name','macaddress','ipaddress','netmask','bonding')
    search_fields = ('macaddress','ipaddress')


class EventLogAdmin(admin.ModelAdmin,BaseAdmin):
    list_display = ('name','colored_event_type','asset','component','detail','date','user')
    search_fields = ('asset',)
    list_filter = ('event_type','component','date','user')


from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn','asset_type','manufactory','model','cpu_model','cpu_count','cpu_core_count','ram_size','os_distribution','os_release','date','approved','approved_by','approved_date')
    actions = ['approve_selected_objects']
    # modeladmin是这个admin本身，可以写成self，queryset是选中的待批准资产对象，选了几个就传过来几个
    # selected 是选中的id，ContentType这张表存了所有表的表名，可以用来动态关联多张表

    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        # ct.pk指待批准资产表--NewAssetApprovalZone在content_type表中的主键id
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "批准入库"

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.IDC)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC,NicAdmin)
admin.site.register(models.RAM)
admin.site.register(models.Manufactory)
admin.site.register(models.Tag)
admin.site.register(models.Software)
admin.site.register(models.EventLog,EventLogAdmin)
admin.site.register(models.NewAssetApprovalZone,NewAssetApprovalZoneAdmin)


# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Asset)
# admin.site.register(Server)
# admin.site.register(NetworkDevice)
# admin.site.register(BusinessUnit)
# admin.site.register(Software)
# admin.site.register(CPU)
# admin.site.register(Disk)
# admin.site.register(NIC)
# admin.site.register(RAM)
# admin.site.register(Tag)
# admin.site.register(EventLog)
# admin.site.register(NewAssetApprovalZone)
# admin.site.register(IDC)
# admin.site.register(Contract)
# admin.site.register(Manufactory)