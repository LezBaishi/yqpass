from django.contrib import admin

# Register your models here.


# Register your models here.
from backend.ticket.models import TicketFlowLog, TicketRecord, TicketCustomField
from service.common.base_services import ModelBaseAdmin


class TicketRecordAdmin(ModelBaseAdmin):
    search_fields = ('sn', 'title')
    list_display = ('id', 'sn', 'title', 'workflow_id', 'state_id', 'parent_ticket_id', 'participant_type_id',
                    'participant') + ModelBaseAdmin.list_display


class TicketFlowLogAdmin(ModelBaseAdmin):
    search_fields = ('ticket_id',)
    list_display = ('id', 'ticket_id', 'transition_id', 'suggestion', 'participant_type_id', 'participant',
                    'state_id') + ModelBaseAdmin.list_display


class TicketCustomFieldAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'ticket_id', 'name', 'field_key') + ModelBaseAdmin.list_display


admin.site.register(TicketRecord, TicketRecordAdmin)
admin.site.register(TicketFlowLog, TicketFlowLogAdmin)
admin.site.register(TicketCustomField, TicketCustomFieldAdmin)
