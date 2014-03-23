# into your database.
from __future__ import unicode_literals

from django.db import models

class A1C(models.Model):
    id_a1c = models.AutoField(primary_key=True, db_column = "a/c_id")
    empty_weight = models.FloatField()
    a1c_name = models.CharField(max_length=255L, db_column = "name")
    model = models.ForeignKey('Model', null=True, 
                              db_column='model_id', blank=True)
    class Meta:
        db_table = 'A/C'
        ordering = ('a1c_name',)
    
    def __unicode__(self):
        return u'%s' %self.a1c_name

class Base(models.Model):
    id_base = models.AutoField(primary_key=True, db_column = "base_id")
    base_name = models.CharField(max_length=255L, db_column = "name")
    
    class Meta:
        db_table = 'Base'
        ordering = ('base_name',)
    
    def __unicode__(self):
        return u'%s' %self.base_name

class Contract1Chater(models.Model):
    id_contract1chater = models.AutoField(primary_key=True, 
                                          db_column='contract/charter_id')
    con_name = models.CharField(max_length=255L, db_column = "name")
    customer = models.ForeignKey('Customer', db_column='customer_id')
    class Meta:
        db_table = 'Contract/Charter'
        ordering = ('con_name',)
    
    def __unicode__(self):
        return u'%s' %self.con_name
    

class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True, 
                                      db_column='customer_id')
    address = models.CharField(max_length=255L, db_column = "address")
    alt_name = models.CharField(max_length=255L, db_column = 'alt_name')
    ar_site_number = models.IntegerField(db_column = "ar_site_number")
    city = models.CharField(max_length=255L, db_column = "city")
    country = models.CharField(max_length=255L, db_column = "country")
    cus_name = models.CharField(max_length=255L, db_column = "name")
    processed = models.IntegerField(db_column = "processed")
    state = models.CharField(max_length=255L, db_column = "state")
    class Meta:
        db_table = 'Customer'
        ordering = ('cus_name',)
    def __unicode__(self):
        return u'%s' %self.cus_name

# Temporary User for debug
class UserTemp(models.Model):    
    employee_number = models.IntegerField(primary_key=True, db_column='employee_Number', max_length=32)
    password = models.CharField(max_length=10)
    email = models.EmailField(unique= True,max_length=255L,blank=True,)
    class Meta:
        db_table = 'UserTemp'
    def __unicode__(self):
        return u'%s' %self.employee_number        

class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True, db_column='employee_id') # Field name made lowercase.
    first_name = models.CharField(max_length=255L)
    last_name = models.CharField(max_length=255L)
    
    employee_number = models.OneToOneField(UserTemp)
#     employee_number = models.IntegerField(unique=True,  max_length=32)
    
    email = models.EmailField(unique= True,max_length=255L,blank=True,)
    phone = models.IntegerField(max_length=255L)
    password = models.CharField(max_length=255L)
    processed = models.IntegerField(max_length=16, null=True)
    job_title = models.ForeignKey('JobTitle', null=True, db_column='job_title', blank=True)
    class Meta:
        db_table = 'Employee'
        ordering = ('employee_number',)
    
    def __unicode__(self):
        return u'%s' % (self.employee_number)

class JobTitle(models.Model):
    id_job_title = models.AutoField(primary_key=True, 
                                       db_column='job_title_id')
    job_name = models.CharField(max_length=255L, db_column = "name")
    class Meta:
        db_table = 'Job_Title'
    def __unicode__(self):
        return u'%s' %self.job_name

class Location(models.Model):
    id_location = models.AutoField(primary_key=True, 
                                   db_column='location_id')
    lat = models.FloatField(null=True, blank=True, default = 0, db_column='lat')
    long = models.FloatField(null=True, blank=True, default = 0, db_column='long')
    location_name = models.CharField(max_length=255L, db_column='name')
    location_type = models.ForeignKey('LocationType', null=True, db_column='location_type_id', blank=True)
    class Meta:
        db_table = 'Location'
    def __unicode__(self):
        return self.location_name
    

class LocationType(models.Model):
    id_location_type = models.AutoField(max_length = 32, primary_key=True, 
                                           db_column='location_type_id')
    location_type_name = models.CharField(max_length=255L, db_column = "name")
    class Meta:
        db_table = 'Location_type'

class Log(models.Model):
    id_log = models.AutoField(primary_key=True, db_column='log_id')
    a1c_empty_weight = models.FloatField(db_column='a/c_empty_weight')
    allowable_takeoff_weight = models.FloatField()
    co_pilot_employee_number = models.ForeignKey('Employee', db_column='co_pilot_employee_number', 
                                                 related_name ='co_pilot_employee_number', blank=True, null=True)
    co_pilot_weight = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey('Customer', null=True, db_column='customer', blank=True)
    fuel = models.FloatField(null=True, blank=True)
    log_date = models.DateField()
    log_number = models.IntegerField()
    opterational_weight = models.FloatField(null=True, blank=True)
    payload_available = models.FloatField(null=True, blank=True)
    pilot_employee_number = models.ForeignKey('Employee', null=True, db_column='pilot_employee_number', 
                                              related_name ='pilot_employee_number', blank=True)
    pilot_weight = models.FloatField()
    a1c = models.ForeignKey(A1C, null=True, db_column='a/c_id', blank=True)
    base = models.ForeignKey(Base, null=True, db_column='base_id', blank=True)
    contract1charter = models.ForeignKey(Contract1Chater, null=True, db_column='contract/charter_id', blank=True)
    is_submited = models.BooleanField(db_column='is_submitted', default = 0, blank = True)
    user_id = models.CharField(max_length=255L, db_column='employee_number')
    
    class Meta:
        db_table = 'Log'
        ordering = ('-log_number',)

class LogEmployee(models.Model):
    id_log_employee = models.AutoField(primary_key=True, db_column='log_employee_id') # Field name made lowercase.
    day = models.FloatField(null=True, blank=True)
    ifr = models.FloatField(null=True, blank=True)
    long_in = models.FloatField(null=True, blank=True)
    night = models.FloatField(null=True, blank=True)
    nvg = models.FloatField(null=True, blank=True)
    sic = models.FloatField(null=True, blank=True)
    employee = models.ForeignKey(Employee, null=True, db_column='employee_id', blank=True)
    log = models.ForeignKey(Log, null=True, db_column='log', blank=True)
    pic = models.FloatField(null=True, blank=True)
    
    #Add fiedl for CRs
    vfr =  models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'Log_Employee'
    
class LogSection(models.Model):
    id_log_section = models.AutoField(primary_key=True, 
                                      db_column='log_section_id')
    all_ifr = models.BooleanField(verbose_name = "ALL IFR")
    all_nfr = models.BooleanField(db_column='all_vfr', verbose_name = "ALL VFR")
    flight_data_amount = models.CharField(null=True, blank=True, max_length = 255L,
                                          db_column='amount',
                                           verbose_name = "Amount")
    flight_data_block_time = models.FloatField(null=True, blank=True,
                                               db_column='block_time',
                                               verbose_name = "Block Time")
    flight_data_cargo_weight = models.FloatField(null=True, blank=True,
                                                 db_column='cargo_weight', 
                                                 verbose_name = "Cargo")
    flight_data_cg = models.FloatField(null=True, blank=True, 
                                       verbose_name = "CG", db_column='cg')
    emp_by = models.ForeignKey(Customer, null=True, db_column='emp_by', 
                               blank=True, verbose_name = "Emp By")
    flight_data_fuel = models.FloatField(verbose_name = "Fuel", 
                                         db_column='fuel')
    flight_data_fuel_amount = models.FloatField(null=True, blank=True,
                                                db_column='fuel_amount',
                                                verbose_name = "Fuel Amount")
    flight_data_fuel_station = models.ForeignKey(Location, null=True, blank=True, 
                                                 related_name = "fuel_station",
                                                 db_column='fuel_station_id',
                                                verbose_name = "Fuel Station")
    fuel_wheels_down = models.FloatField(db_column='fuel_wheels_down',
                                          verbose_name = "Fuel at Wheels Down")
    load_schedule = models.BooleanField(verbose_name = "Load schedule",
                                         db_column='load_schedule')
    log = models.ForeignKey(Log, null=True, blank=True, 
                            db_column='log_id',
                            editable=False, on_delete=models.CASCADE)
    manifest_number = models.FloatField(null=True, blank=True,
                                        db_column='manifest_number',
                                          verbose_name = "Manifest#", max_length=9)
    order = models.IntegerField(verbose_name = "Flight #",
                                db_column='order',
                                default=1, max_length=9)
    off = models.CharField(max_length = 5, db_column='off')
    on = models.CharField(max_length = 5, db_column='on')
    partial_nfr = models.IntegerField(null=True, blank=True, 
                                   db_column='partial_vfr', verbose_name = "Partial VFR")
    
    passenger = models.IntegerField(db_column='Passenger')
    
    flight_time = models.IntegerField(verbose_name = "Flight time", 
                                     db_column='flight_time', max_length=9)
    
    from_field = models.ForeignKey(Location, db_column='from', verbose_name = "From") 
    to = models.ForeignKey(Location, db_column='to', 
                           related_name='to', verbose_name = "To")
    flight_data_patient = models.IntegerField(null=True, blank=True, 
                                            db_column='patient', verbose_name = "Patient", max_length=9)
    flight_data_range_from = models.FloatField(null=True, blank=True, 
                                               db_column='range_from',verbose_name = "Range From", max_length=9)
    flight_data_range_to = models.FloatField(null=True, blank=True, 
                                             db_column='range_to', verbose_name = "Range To", max_length=9)
    flight_data_tlo_w = models.FloatField(verbose_name = "T/O W",db_column='t/o_w')
    slot_purpose_id =  models.ForeignKey('Slot_Purpose',db_column='slot_purpose_id',
                                          verbose_name = "Slot_Purpose") 
    
    #Add new field for CRs
    day = models.FloatField(db_column = "day")
    night = models.FloatField(db_column = "night")
    pilot_nvg = models.FloatField(null=True, blank=True, db_column = "pilot_nvg")
    co_pilot_nvg = models.FloatField(null=True, blank=True, db_column = "co_pilot_nvg")
    
    class Meta:
        db_table = 'Log_Section'

class Model(models.Model):
    id_model = models.AutoField(primary_key=True, db_column='model_id')
    max_passenger = models.IntegerField(max_length=16)
    mo_name = models.CharField(max_length=50, db_column='name')
    me_load_schedule_cg_range_from = models.FloatField()
    me_load_schedule_cg_range_to = models.FloatField()
    max_gross_weight = models.FloatField()
    class Meta:
        db_table = 'Model'
        ordering = ('mo_name',)
    def __unicode__(self):
        return u'%s' %self.mo_name
    
class Slot_Purpose(models.Model):
    id_slot_purpose = models.AutoField(primary_key=True, 
                                          db_column='slot_purpose_id')
    slot_purpose_name = models.CharField(max_length=255L, db_column = "name")
    class Meta:
        db_table = 'Slot_Purpose'
    def __unicode__(self):
        return u'%s' %self.slot_purpose_name
        
class Log_Location(models.Model):
    id_log_location = models.AutoField(max_length = 32, primary_key=True, db_column='log_location_id') # Field name made lowercase.
    amount = models.CharField(max_length=255L, null=True, blank=True)
    location_id = models.ForeignKey(Location, null=True, blank=True, db_column='location_id')
    gallons = models.FloatField(null=True, blank=True)
    log_id = models.ForeignKey(Log, null=True, blank=True, db_column='log_id')
    owner = models.CharField(max_length=255L, null=True, blank=True)
    
    class Meta:
        db_table = 'Log_Location'



class Fuel (models.Model):
    location = models.CharField(max_length=30L)
    gallons = models.CharField(max_length=30L)
    owner = models.CharField(max_length=30L)
    amount = models.IntegerField()
        