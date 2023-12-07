from django.db import models

# Create your models here.

class OjccCase(models.Model):
    case_id = models.CharField(max_length=255,null=True,blank=True,verbose_name="CaseID")
    case_yr = models.CharField(max_length=255,null=True,blank=True,verbose_name="caseYr")
    case_num = models.CharField(max_length=255,null=True,blank=True,verbose_name="caseNum")
    ojcc_case_number = models.CharField(max_length=255,null=True,blank=True,verbose_name="OJCC Case Number")
    judge = models.CharField(max_length=255,null=True,blank=True,verbose_name="Judge")
    mediator = models.CharField(max_length=255,null=True,blank=True,verbose_name="Mediator")
    carrier = models.CharField(max_length=255,null=True,blank=True,verbose_name="Carrier")
    accident_date = models.CharField(max_length=255,null=True,blank=True,verbose_name="Accident Date")
    date_assigned = models.CharField(max_length=255,null=True,blank=True,verbose_name="Date Assigned")
    district = models.CharField(max_length=255,null=True,blank=True,verbose_name="District")
    county = models.CharField(max_length=255,null=True,blank=True,verbose_name="County")
    counsel_for_claimant = models.CharField(max_length=255,null=True,blank=True,verbose_name="Counsel For Claimant")
    counsel_for_employer = models.CharField(max_length=255,null=True,blank=True,verbose_name="Counsel For Employer/Carrier")
    case_status = models.CharField(max_length=255,null=True,blank=True,verbose_name="case status")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "OJCC Case"
        verbose_name_plural = "OJCC Cases"

    def __str__(self) :
        return "OJCC Case Number " + self.ojcc_case_number


class Schedule(models.Model):
    ojcc_case = models.ForeignKey(OjccCase,on_delete=models.CASCADE)
    hearing_type = models.CharField(max_length=255,null=True,blank=True,verbose_name="Hearing Type")
    event_date = models.CharField(max_length=255,null=True,blank=True,verbose_name="Event Date")
    start_time = models.CharField(max_length=255,null=True,blank=True,verbose_name="Start Time*")
    current_status = models.CharField(max_length=255,null=True,blank=True,verbose_name="Current Status")
    _with = models.CharField(max_length=255,null=True,blank=True,verbose_name="With")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedule"


class Docket(models.Model):
    ojcc_case = models.ForeignKey(OjccCase,on_delete=models.CASCADE)
    date = models.CharField(max_length=255,null=True,blank=True,verbose_name="Date")
    proceeding = models.TextField(max_length=255,null=True,blank=True,verbose_name="Proceedings")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Docket"
        verbose_name_plural = "Docket"

