from django.contrib import admin

# Register your models here.
from backend.workflow.models import Transition, CustomField, Workflow, State, WorkflowScript
from service.common.base_services import ModelBaseAdmin


class WorkflowAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description') + ModelBaseAdmin.list_display


class StateAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'order_id', 'type_id', 'workflow_id', 'sub_workflow_id', 'distribute_type_id',
                    'is_hidden',) + ModelBaseAdmin.list_display


class TransitionAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'workflow_id', 'transition_type_id', 'source_state_id', 'destination_state_id',
                    'alert_enable') + ModelBaseAdmin.list_display


class CustomFieldAdmin(ModelBaseAdmin):
    search_fields = ('workflow_id',)
    list_display = ('id', 'workflow_id', 'field_type_id', 'field_key', 'field_name',
                    'order_id') + ModelBaseAdmin.list_display


class WorkflowScriptAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description', 'is_active') + ModelBaseAdmin.list_display


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(WorkflowScript, WorkflowScriptAdmin)
