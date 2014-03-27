# # from flight_log.forms import FlightLogDetail
# # print FlightLogDetail()
# 
# # into your database.
# from __future__ import unicode_literals
# 
# from django.db import models
# 
# class A1C(models.Model):
#     id_a1c = models.IntegerField(primary_key=True)
#     empty_weight = models.CharField(max_length=50L)
#     max_gross_weight = models.CharField(max_length=50L)
#     name = models.CharField(max_length=50L)
#     model = models.ForeignKey('Model', null=True, db_column='model', blank=True)
#     class Meta:
#         db_table = 'A1C'
# 
# class Base(models.Model):
#     id_base = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'Base'
# 
# class Contract1Chater(models.Model):
#     id_contract1chater = models.IntegerField(primary_key=True, db_column='id_Contract1Chater') # Field name made lowercase.
#     name = models.CharField(max_length=50L)
#     customer = models.ForeignKey('Customer', db_column='customer_id')
#     class Meta:
#         db_table = 'Contract1Chater'
#     
#     def __unicode__(self):
#         return u'%s' %self.name
#     
# 
# class Customer(models.Model):
#     id_customer = models.IntegerField(primary_key=True, db_column='id_Customer') # Field name made lowercase.
#     address = models.CharField(max_length=50L)
#     alt_name = models.CharField(max_length=50L)
#     ar_site_number = models.CharField(max_length=50L)
#     city = models.CharField(max_length=50L)
#     country = models.CharField(max_length=50L)
#     name = models.CharField(max_length=50L)
#     processed = models.CharField(max_length=50L)
#     state = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'Customer'
#     def __unicode__(self):
#         return u'%s' %self.name
# 
# class Employee(models.Model):
#     id_employee = models.IntegerField(primary_key=True, db_column='id_Employee') # Field name made lowercase.
#     name = models.CharField(max_length=50L)
#     processed = models.CharField(max_length=50L)
#     job_title = models.ForeignKey('JobTitle', null=True, db_column='job_title', blank=True)
#     class Meta:
#         db_table = 'Employee'
# 
# class JobTitle(models.Model):
#     id_job_title = models.IntegerField(primary_key=True, db_column='id_Job_Title') # Field name made lowercase.
#     name = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'Job_Title'
# 
# class Location(models.Model):
#     id_location = models.IntegerField(max_length = 32, primary_key=True, db_column='id_Location') # Field name made lowercase.
#     lat = models.FloatField(null=True, blank=True)
#     long = models.FloatField(null=True, blank=True)
#     location_name = models.CharField(max_length=50L)
#     location_type = models.ForeignKey('LocationType', null=True, db_column='location_type', blank=True)
#     owner = models.ForeignKey('Owner', db_column='owner')
#     class Meta:
#         db_table = 'Location'
#     def __unicode__(self):
#         return self.name    
#     
# 
# class LocationType(models.Model):
#     id_location_type = models.IntegerField(max_length = 32, primary_key=True, db_column='id_Location_type') # Field name made lowercase.
#     location_type_name = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'Location_type'
# 
# class Log(models.Model):
#     id_log = models.IntegerField(primary_key=True)
#     a1c_empty_weight = models.CharField(max_length=50L)
#     allowable_takeoff_weight = models.CharField(max_length=50L)
#     block_time = models.CharField(max_length=50L)
#     customer_info = models.CharField(max_length=50L)
#     data_created = models.CharField(max_length=50L)
#     last_updated = models.CharField(max_length=50L)
#     log_date = models.CharField(max_length=50L)
#     log_number = models.CharField(max_length=50L)
#     opterational_weight = models.CharField(max_length=50L)
#     payload_available = models.CharField(max_length=50L)
#     pilot_weight = models.CharField(max_length=50L)
#     base = models.ForeignKey(Base, null=True, db_column='base', blank=True)
#     a1c = models.ForeignKey(A1C, null=True, db_column='a1c', blank=True)
#     contract1charter = models.ForeignKey(Contract1Chater, null=True, db_column='contract1charter', blank=True)
#     no_flight_status = models.ForeignKey('NoFlightStatus', null=True, db_column='no_flight_status', blank=True)
#     class Meta:
#         db_table = 'Log'
# 
# class LogEmployee(models.Model):
#     id_log_employee = models.IntegerField(primary_key=True, db_column='id_Log_Employee') # Field name made lowercase.
#     day = models.CharField(max_length=50L)
#     ifr = models.CharField(max_length=50L)
#     long_in = models.CharField(max_length=50L)
#     night = models.CharField(max_length=50L)
#     nvg = models.CharField(max_length=50L)
#     sic = models.CharField(max_length=50L)
#     employee = models.ForeignKey(Employee, null=True, db_column='employee', blank=True)
#     log = models.ForeignKey(Log, null=True, db_column='log', blank=True)
#     class Meta:
#         db_table = 'Log_Employee'
#         
# class LogSection(models.Model):
#     id_log_section = models.IntegerField(primary_key=True, db_column='id_Log_Section')
#     flight_data_amount = models.FloatField(null=True, blank=True)
#     flight_data_block_time = models.IntegerField(max_length=16)
#     flight_data_cargo_weight = models.FloatField()
#     flight_data_cg = models.FloatField()
#     flight_data_fuel = models.FloatField()
#     flight_data_fuel_station = models.IntegerField(max_length=16, null=True, blank=True)
#     flight_data_fuel_amount = models.FloatField(null=True, blank=True)
#     flight_data_patient = models.IntegerField(max_length=16)
#     flight_data_range = models.CharField(max_length=50L)
#     flight_data_rmks = models.CharField(max_length=50L)
#     flight_data_tlo_w = models.FloatField()
#     int = models.CharField(max_length=50L)
#     flight_time = models.IntegerField()
#     load_schedule = models.BooleanField(max_length=50L)
#     manifest_number = models.IntegerField(max_length=16, null=True, blank=True)
#     off = models.DateField()
#     on = models.DateField()
#     order = models.IntegerField(max_length=16)
#     passenger = models.CharField(max_length=16)
#     from_field = models.ForeignKey(Location, null=True, db_column='from', 
#                                    blank=True, verbose_name = "from") # Field renamed because it was a Python reserved word.
#     to = models.ForeignKey(Location, null=True, db_column='to', blank=True, related_name='to')
#     emp_by = models.ForeignKey(Customer, null=True, db_column='emp_by', blank=True)
#     log = models.ForeignKey(Log, null=True, db_column='log', blank=True)
#     class Meta:
#         db_table = 'Log_Section'
# 
# class Model(models.Model):
#     id_model = models.IntegerField(primary_key=True)
#     max_passenger = models.IntegerField()
#     name = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'Model'
# 
# class NoFlightStatus(models.Model):
#     id_no_flight_status = models.IntegerField(primary_key=True, db_column='id_No_Flight_status') # Field name made lowercase.
#     name = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'No_Flight_status'
#     
#     def __unicode__(self):
#         return u'%s' %self.name
# 
# class Owner(models.Model):
#     id_owner = models.IntegerField(max_length = 32, primary_key=True, db_column='id_Owner') # Field name made lowercase.
#     owner_name = models.CharField(max_length=50L)
#     class Meta:
#         db_table = 'Owner'


