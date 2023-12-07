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
    country = models.CharField(max_length=255,null=True,blank=True,verbose_name="Country")
    counsel_for_claimant = models.CharField(max_length=255,null=True,blank=True,verbose_name="Counsel For Claimant")
    counsel_for_employer = models.CharField(max_length=255,null=True,blank=True,verbose_name="Counsel For Employer/Carrier")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)

class Schedule(models.Model):
    ojcc_case = models.ForeignKey(OjccCase,on_delete=models.CASCADE)
    hearing_type = models.CharField(max_length=255,null=True,blank=True,verbose_name="Hearing Type")
    event_date = models.CharField(max_length=255,null=True,blank=True,verbose_name="Event Date")
    start_time = models.CharField(max_length=255,null=True,blank=True,verbose_name="Start Time*")
    current_status = models.CharField(max_length=255,null=True,blank=True,verbose_name="Current Status")
    current_status = models.CharField(max_length=255,null=True,blank=True,verbose_name="Event Date")
    _with = models.CharField(max_length=255,null=True,blank=True,verbose_name="With")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)

class Docket(models.Model):
    ojcc_case = models.ForeignKey(OjccCase,on_delete=models.CASCADE)
    date = models.CharField(max_length=255,null=True,blank=True,verbose_name="Date")
    proceedings = models.CharField(max_length=255,null=True,blank=True,verbose_name="Proceedings")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now=True)

