# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
import datetime
from django.db import connections
from django.utils import timezone
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class EoooStudent(models.Model):
    student_id = models.AutoField(primary_key=True)
    ssn = models.IntegerField(unique=True)
    academic_standing = models.CharField(max_length=1, default='g')
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30, blank=True, null=True)
    lname = models.CharField(max_length=30)
    street = models.CharField(max_length=50, null=True, default='none')
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, default='ca')
    zip = models.IntegerField(default='0')
    phone_number = models.IntegerField(default='1110109')
    sex = models.CharField(max_length=1 ,default='m')
    income_status = models.CharField(max_length=50, default='dependent')

    class Meta:
        db_table = 'eooo_student'
    

    def full_name(self):
        return self.fname + " " + self.lname
    def __str__(self):
        return   str(self.student_id)

class EoooParent(models.Model):
    ssn = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30, blank=True, null=True)
    lname = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.IntegerField()
    phone_number = models.IntegerField()
    bday = models.DateField()
    psex = models.CharField(max_length=1)
    status = models.CharField(max_length=50)
    income = models.FloatField()

    class Meta:
        managed = False
        db_table = 'eooo_parent'


class EoooDepartment(models.Model):
    departmentid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'eooo_department'


class EoooLogistics(models.Model):
    departmentid = models.BooleanField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'eooo_logistics'

class EoooOutreach(models.Model):
    departmentid = models.BooleanField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'eooo_outreach'

class EoooApplication(models.Model):
    applicationid = models.IntegerField(primary_key=True)
    requestedamount = models.FloatField()
    appdate = models.DateField()
    apstatus = models.CharField(max_length=30)
    approved = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'eooo_application'

class EoooBudget(models.Model):
    budgetid = models.IntegerField(primary_key=True)
    amount = models.FloatField()
    budate = models.DateField()

    class Meta:
        managed = False
        db_table = 'eooo_budget'

class EoooEmployee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    ssn = models.IntegerField()
    hire_date = models.DateField()
    end_date = models.DateField()
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30, blank=True, null=True)
    lname = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.IntegerField()
    phone_number = models.IntegerField()
    esex = models.CharField(max_length=1)
    departmentid = models.ForeignKey(EoooDepartment, models.DO_NOTHING, db_column='departmentid')

    class Meta:
        managed = False
        db_table = 'eooo_employee'

class EoooReviewboard(models.Model):
    departmentid = models.BooleanField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'eooo_reviewboard'

class EoooSchool(models.Model):
    school_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.IntegerField()
    departmentid = models.ForeignKey(EoooDepartment, models.DO_NOTHING, db_column='departmentid')

    class Meta:
        managed = False
        db_table = 'eooo_school'

class EoooData(models.Model):
    dataid = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=30)
    datadate = models.DateField()
    departmentid = models.ForeignKey('EoooDepartment', models.DO_NOTHING, db_column='departmentid')

    class Meta:
        managed = False
        db_table = 'eooo_data'

class EoooInfor(models.Model):
    sourceid = models.IntegerField(primary_key=True)
    infodate = models.DateField()
    departmentid = models.ForeignKey(EoooDepartment, models.DO_NOTHING, db_column='departmentid')

    class Meta:
        managed = False
        db_table = 'eooo_infor'

@python_2_unicode_compatible
class EoooFapackage(models.Model):
    packageid = models.AutoField(primary_key=True)
    ptype = models.CharField(max_length=30)
    amount = models.FloatField(blank=True, null=True)
    fabudgetid = models.ForeignKey(EoooBudget, models.DO_NOTHING, db_column='fabudgetid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eooo_fapackage'
    def __str__(self):
        return  str(self.packageid) #+ " $" + str(self.amount) + " Type:" + self.ptype

class EoooAttending(models.Model):
    studentid = models.ForeignKey('EoooStudent', models.DO_NOTHING, db_column='studentid', primary_key=True)
    schoolid = models.ForeignKey('EoooSchool', models.DO_NOTHING, db_column='schoolid')

    class Meta:
        managed = False
        db_table = 'eooo_attending'


class EoooBecomes(models.Model):
    appid = models.ForeignKey(EoooApplication, models.DO_NOTHING, db_column='appid', primary_key=True)
    dataid = models.ForeignKey(EoooData, models.DO_NOTHING, db_column='dataid')
    datadescription = models.CharField(max_length=50)
    bdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'eooo_becomes'

@python_2_unicode_compatible
class EoooDistributedto(models.Model):
    studentid = models.ForeignKey('EoooStudent', models.DO_NOTHING, db_column='studentid', primary_key=True)
    fapackageid = models.ForeignKey('EoooFapackage', models.DO_NOTHING, db_column='fapackageid')
    ddate = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'eooo_distributedto'
    def __str__(self):
        return str(self.studentid)#str(self.studentid) + " Financial Aid Package" + str(self.fapackageid) + " Date:" + str(self.ddate)


class EoooFillsout(models.Model):
    studentid = models.ForeignKey('EoooStudent', models.DO_NOTHING, db_column='studentid', primary_key=True)
    applicationid = models.ForeignKey(EoooApplication, models.DO_NOTHING, db_column='applicationid')
    fdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'eooo_fillsout'

class EoooUinfof(models.Model):
    studentid = models.ForeignKey(EoooStudent, models.DO_NOTHING, db_column='studentid', primary_key=True)
    parentssn = models.ForeignKey(EoooParent, models.DO_NOTHING, db_column='parentssn')

    class Meta:
        managed = False
        db_table = 'eooo_uinfof'


class EoooUstoresi(models.Model):
    dataid = models.ForeignKey(EoooData, models.DO_NOTHING, db_column='dataid', primary_key=True)
    dadescription = models.CharField(max_length=30)
    sourceid = models.ForeignKey(EoooInfor, models.DO_NOTHING, db_column='sourceid')
    sourcedate = models.DateField()

    class Meta:
        managed = False
        db_table = 'eooo_ustoresi'
