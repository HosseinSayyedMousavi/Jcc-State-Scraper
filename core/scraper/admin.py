from django.contrib import admin
from .models import Docket , OjccCase , Schedule
# Register your models here.

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    readonly_fields = ("hearing_type","event_date","start_time","current_status","current_status","_with")   
    exclude = ["created_date","updated_date","ojcc_case"]

class DocketInline(admin.TabularInline):
    model = Docket
    extra = 0
    readonly_fields = ("date","proceedings")   
    exclude = ["created_date","updated_date","ojcc_case"]

class OjccCaseAdmin(admin.ModelAdmin):

    list_display = ["ojcc_case_number"]
    list_display_links = list_display
    readonly_fields = ["case_id","case_yr","case_num","ojcc_case_number","judge","mediator","carrier","accident_date","date_assigned","district","country","counsel_for_claimant","counsel_for_employer"]
    inlines = [
    ScheduleInline,
    DocketInline
        ]
    exclude = ["id","created_date","updated_date"]
    