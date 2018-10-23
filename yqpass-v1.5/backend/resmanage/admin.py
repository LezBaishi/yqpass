from django.contrib import admin
from backend.resmanage.models import *
from django.db.models import Count

__author__ = 'mc'

class BuildingInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'creator', 'gmt_created', 
                    'modifier', 'gmt_modified', )
    search_fields = ('building', )
    ordering = ('id', )


    def save_model(self, request, obj, form, change):
        if change: # 更改的时候
            # obj_original = self.model.objects.get(pk=obj.pk)
            pass
        else: # 新增的时候
            # obj_original = None
            obj.creator = request.user.username
  
        obj.modifier = request.user.username
        obj.save()


class BuildingRoomInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_building_info', 'room', 'description', 
                    'creator', 'gmt_created', 'modifier', 'gmt_modified', )
    search_fields = ('building_info__building', 'room', 'description', )
    ordering = ('id', )

    def get_building_info(self, obj):
        return obj.building_info
    get_building_info.short_description = '楼栋'
    get_building_info.admin_order_field = 'building_info'


    def save_model(self, request, obj, form, change):
        if change: # 更改的时候
            # obj_original = self.model.objects.get(pk=obj.pk)
            pass
        else: # 新增的时候
            # obj_original = None
            obj.creator = request.user.username
  
        obj.modifier = request.user.username
        obj.save()

class OcableSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ocable_name', 'get_bri_A','get_bri_Z', 
                    'core_num', 'ocable_length', 'ocable_type', 'ocable_level', 
                    'ofiber_type', 'creator', 'gmt_created', 'modifier', 'gmt_modified', )
    search_fields = ('ocable_name', 'ocable_type', 'ocable_level', 'ofiber_type', )
    # list_filter = ('bri_A__building_info', 'ocable_type', 'ocable_level', 'ofiber_type',)
    fieldsets = (
        (None, {
            'fields': ('bri_A', 'name_A', 'bri_Z','name_Z',
                        'core_num', 'ocable_length', 'ocable_type', 
                        'ocable_level', 'ofiber_type', 'notes', )}
        ),
    )
    ordering = ('id', )
    # filter_horizontal = ()

    def get_bri_A(self, obj):
        return obj.bri_A
    get_bri_A.short_description = 'A端楼栋机房号'
    get_bri_A.admin_order_field = 'bri_A'

    def get_bri_Z(self, obj):
        return obj.bri_Z
    get_bri_Z.short_description = 'Z端楼栋机房号'
    get_bri_Z.admin_order_field = 'bri_Z'


    def save_model(self, request, obj, form, change):
        if change: # 更改的时候
            # obj_original = self.model.objects.get(pk=obj.pk)
            pass
        else: # 新增的时候
            # obj_original = None
            obj.creator = request.user.username

        obj.ocable_name = obj.name_A + '-' + obj.name_Z   
        obj.modifier = request.user.username
        obj.save()

class OfiberCoreAdmin(admin.ModelAdmin):
    list_display = ('get_ocable', 'core_no', 'ocable_odf_A', 'ocable_odf_Z', 
                    'ocable_cor', 'core_quality', 'creator', 'gmt_created',
                    'modifier', 'gmt_modified', )
    search_fields = ('ocable_section__ocable_name', 'ocable_cor', 'core_quality', )
    fieldsets = (
        (None, {
            'fields': ('ocable_section', 'core_no', 'ocable_odf_A', 'ocable_odf_Z',
                        'core_quality', 'notes', )}
        ),
    )
    ordering = ('ocable_section', 'core_no', )

    def get_ocable(self, obj):
        return obj.ocable_section
    get_ocable.short_description = '光缆段名称（A-Z）'
    get_ocable.admin_order_field = 'ocable_section'

    def save_model(self, request, obj, form, change):
        if change: # 更改的时候
            obj_original = self.model.objects.get(pk=obj.pk)

        else: # 新增的时候
            # obj_original = None
            obj.creator = request.user.username
            
            # 纤芯序号
            # num = self.model.objects.filter(ocable_section=obj.ocable_section).count() + 1 
            
        # ocable_cor=光缆名称+纤芯数+'芯之'+纤芯序号
        obj.ocable_cor = obj.ocable_section.ocable_name + '-' +str(obj.ocable_section.core_num) + '芯之' + str(obj.core_no)
               
        obj.modifier = request.user.username
        obj.save()

class RouteInfoAdmin(admin.ModelAdmin):
    list_display = ('circuit_num', 'get_ofiber_core', 'route_no', 
                    'route_where', 'state', 'get_application_detail', 
                    'creator', 'gmt_created','modifier', 'gmt_modified', )
    search_fields = ('circuit_num', 'ofiber_core__ocable_cor', )
    fieldsets = (
        (None, {
            'fields': ('circuit_num', 'ofiber_core', 'route_no', 'route_where',
                        'state', 'application_detail', )}
        ),
    )
    ordering = ('circuit_num', 'route_no','route_where', 'ofiber_core', )

    def get_ofiber_core(self, obj):
        return obj.ofiber_core
    get_ofiber_core.short_description = '对应光缆纤芯'
    get_ofiber_core.admin_order_field = 'ofiber_core'

    def get_application_detail(self, obj):
        return obj.application_detail
    get_application_detail.short_description = '对应工单明细'
    get_application_detail.admin_order_field = 'application_detail'

    def save_model(self, request, obj, form, change):
        if change: # 更改的时候
            # obj_original = self.model.objects.get(pk=obj.pk)
            pass
        else: # 新增的时候
            # obj_original = None
            obj.creator = request.user.username
  
        obj.modifier = request.user.username
        obj.save()


# Register your models here.
admin.site.register(BuildingInfo, BuildingInfoAdmin)
admin.site.register(BuildingRoomInfo, BuildingRoomInfoAdmin)
admin.site.register(OcableSection, OcableSectionAdmin)
admin.site.register(OfiberCore, OfiberCoreAdmin)
admin.site.register(RouteInfo, RouteInfoAdmin)