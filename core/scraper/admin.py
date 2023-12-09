from django.contrib import admin
from .models import Docket , OjccCase , Schedule , StreamScraper

from solo.admin import SingletonModelAdmin
# Register your models here.

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    readonly_fields = ("hearing_type","event_date","start_time","current_status","current_status","_with")   
    exclude = ["created_date","updated_date"]


class DocketInline(admin.TabularInline):
    model = Docket
    extra = 0
    readonly_fields = ("date","proceeding")   
    exclude = ["created_date","updated_date"]

@admin.register(OjccCase)
class OjccCaseAdmin(admin.ModelAdmin):

    list_display = ["ojcc_case_number"]
    list_display_links = list_display
    readonly_fields = ["url","case_status","case_id","case_yr","case_num","ojcc_case_number","judge","mediator","carrier","accident_date","date_assigned","district","county","counsel_for_claimant","counsel_for_employer"]
    inlines = [
    ScheduleInline,
    DocketInline
        ]
    exclude = ["id","created_date","updated_date"]

@admin.register(StreamScraper)
class StreamScraperAdmin(SingletonModelAdmin):
    readonly_fields = ["updated_at","created_at","current_page","status","Progress_bar"]
    exclude = ["stopped"]