from django.contrib import admin

# Register your models here.
from backend.fielddiy.models import ApplicationDetail


class ApplicationDetailAdmin(admin.ModelAdmin):
    search_fields = ('ticket_id', 'bus_sys_name')
    list_display = ('ticket_id', 'field_num', 'bus_sys_name', 'department1_A', 'person1_A',
                    'phone1_A', 'department2_A', 'person2_A', 'phone2_A', 'fk_rid_A',
                    'rack_num_A', 'device_name_A',
                    'port_name_A', 'port_type_A', 'fk_rid_Z', 'rack_num_Z',
                    'device_name_Z', 'port_name_Z', 'port_type_Z', 'department1_Z',
                    'person1_Z', 'phone1_Z', 'department2_Z', 'person2_Z', 'phone2_Z',
                    'bandwidth', 'main_or_spare', 'notes')


admin.site.register(ApplicationDetail, ApplicationDetailAdmin)
