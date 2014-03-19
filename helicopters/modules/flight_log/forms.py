from django import forms
from flight_log.models import Slot_Purpose, LogSection, Employee, Location,\
    LocationType, Log_Location, Fuel, LogEmployee
from flight_log.models import UserTemp
from django.forms.models import ModelForm
from flight_log.models import Log, Customer, Contract1Chater, \
    Model, A1C, Base
from helicopters import settings
import constant
from django.forms.formsets import BaseFormSet

class LoginForm (forms.Form):
    employee_number = forms.CharField(max_length=32)
    password = forms.CharField(max_length=10)
    remember = forms.BooleanField(required=False)  # 'required=False' for valid event not need it
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get(constant.employee_number)
        password = cleaned_data.get(constant.password)
        if username and password:
            if not username.isdigit():  # for positive interger
                msg = constant.mess_account_does_not_exist
                self._errors[ constant.employee_number ] = self.error_class([msg])
            else:
                emp = UserTemp.objects.filter(employee_number=username)  # email is username
                if not emp:
                    msg = constant.mess_account_does_not_exist
                    self._errors[ constant.employee_number ] = self.error_class([msg])
                elif emp[0].password != password:
                    msg = constant.mess_wrong_password
                    self._errors[ constant.password ] = self.error_class([msg])
        """else: # thinking !!!
            if not username:
                msg = constant.mess_account_does_not_exist
                self._errors[ constant.employee_number ] = self.error_class([msg])
        """
        return cleaned_data
    
class FlightLogDetail(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        max_pax = kwargs.pop("max_pax", None)
        print "max_pax"
        print max_pax
        order_id = kwargs.pop("next_order_id", None)
        fuel = kwargs.pop("fuel", None)
        partial_range = kwargs.pop("partial_range", None)
        super(FlightLogDetail, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['order'] = forms.IntegerField(initial=order_id)
            self.fields['order'].widget.attrs['readonly'] = True
            if fuel:
                fuel = float(fuel)
            self.fields['flight_data_fuel'] = forms.FloatField(initial=fuel)
            self.fields['flight_data_fuel'].widget.attrs['readonly'] = True
            self.fields['flight_time'].widget.attrs['readonly'] = True
            self.fields['flight_data_tlo_w'] = forms.FloatField(min_value = 0, max_value = 999999999)
            self.fields['flight_data_cg'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_range_from'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_range_to'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_patient'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_fuel_amount'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_cargo_weight'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_block_time'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['fuel_wheels_down'] = forms.FloatField(required = True, min_value = 0,max_value = 999999999)
            self.fields['night'] = forms.FloatField(required = True, min_value = 0,max_value = 999999999)
            self.fields['day'] = forms.FloatField(required = True, min_value = 0,max_value = 999999999)
            self.fields['pilot_nvg'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['co_pilot_nvg'] = forms.FloatField(required = False, min_value = 0,max_value = 999999999)
            self.fields['flight_data_fuel_station'] = forms.CharField(required = False)
            self.fields['from_field'] = forms.ModelChoiceField(
                                                    queryset=Location.objects.all().order_by("location_name"), 
                                                    empty_label="Choose One", required=True)
            self.fields['to'] = forms.ModelChoiceField(
                                                    queryset=Location.objects.all().order_by("location_name"), 
                                                    empty_label="Choose One", required=True)
            self.fields['slot_purpose_id'] = forms.ModelChoiceField(
                                                    queryset=Slot_Purpose.objects.all().order_by("slot_purpose_name"), 
                                                    empty_label="Choose One", required=True)
            self.fields['emp_by'] = forms.ModelChoiceField(
                                                    queryset=Customer.objects.all().order_by("cus_name"), 
                                                    empty_label="Choose One", required=False)
            
            self.fields['slot_purpose_id'].widget.attrs['class'] = 'req'
            self.fields['to'].widget.attrs['class'] = 'req'
            self.fields['from_field'].widget.attrs['class'] = 'req'
            self.fields['flight_data_tlo_w'].widget.attrs['class'] = 'req'
            self.fields['off'].widget.attrs['class'] = 'req'
            self.fields['on'].widget.attrs['class'] = 'req'
            self.fields['from_field'].widget.attrs['class'] = 'req'
            self.fields['slot_purpose_id'].widget.attrs['class'] = 'req'
            self.fields['to'].widget.attrs['class'] = 'req'
            self.fields['fuel_wheels_down'].widget.attrs['class'] = 'req'
            self.fields['flight_data_cg'].widget.attrs['class'] = 'req'
            self.fields['flight_data_range_from'].widget.attrs['class'] = 'req'
            self.fields['flight_data_range_to'].widget.attrs['class'] = 'req'
            self.fields['day'].widget.attrs['class'] = 'req'
            self.fields['night'].widget.attrs['class'] = 'req'
            
            CHOICES = [(-1,'Choose One'),]
            if partial_range:
                for index in range(0, int(partial_range)+1):
                    CHOICES.append((index, str(index)))
            self.fields['partial_nfr'] = forms.ChoiceField(choices=CHOICES, required = False)
            
            init_array = [("",'Choose One'),]
            for i in range(0,int(max_pax) + 1):
                obj = (i,str(i))
                init_array.append(obj)
            self.fields['passenger'] = forms.ChoiceField(
                                                choices = init_array
                                                , required=True)
            self.fields['passenger'].widget.attrs['class'] = 'req'
            
    def clean_flight_data_fuel_station(self):
        data = self.cleaned_data['flight_data_fuel_station'] or None
        if data:
            try:
                data = Location.objects.get(location_name = data)
            except:
                data = location = Location(location_name = data, long = 0, lat = 0, location_type = LocationType.objects.get(id_location_type = 1))
                location.save()
        return data
    
    class Meta:
        model = LogSection

class LogForm(ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label="Choose One", required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.all(), empty_label="Choose One", widget=forms.Select(attrs={'class':'req'}))
    base = forms.ModelChoiceField(queryset=Base.objects.all(), empty_label="Choose One", widget=forms.Select(attrs={'class':'req'}))
    log_number = forms.CharField(widget=forms.HiddenInput())
    id_log = forms.CharField(widget=forms.HiddenInput(), required=False)
    log_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    a1c_empty_weight = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    pilot_weight = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    opterational_weight = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    allowable_takeoff_weight = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    payload_available = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    is_submited = forms.CharField(widget=forms.HiddenInput(), required=False)
    user_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    fuel = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    co_pilot_weight = forms.FloatField(widget=forms.TextInput(attrs={'onblur':'verify_blur(this);', 'class':'req'}))
    model = forms.ModelChoiceField(queryset=Model.objects.all(), 
            empty_label="Choose One", widget=forms.Select(attrs={'class':'req'}))
    
    def __init__(self, *args, **kwargs):
        reload = None
        try:
            reload = kwargs.pop('reload') or None
        except:
            pass
        cus = kwargs.pop('customer')
        mod = kwargs.pop('model')
        super(LogForm, self).__init__(*args, **kwargs)
        self.fields['co_pilot_employee_number'] = forms.ModelChoiceField(queryset=Employee.objects.all(), 
                                                  empty_label="Choose One", widget=forms.Select(attrs={'class':'req'}))
        if cus:
            self.fields['contract1charter'] = forms.ModelChoiceField(queryset=Contract1Chater.objects.filter(customer=cus), empty_label="Choose One", required=False)
        else:
            self.fields['contract1charter'] = forms.ModelChoiceField(queryset=Contract1Chater.objects.none(), empty_label="Choose One", required=False)
        if mod:
            print mod
            self.fields['a1c'] = forms.ModelChoiceField(queryset=A1C.objects.filter(model=mod), empty_label="Choose One", widget=forms.Select(attrs={'class':'req'}))
        elif reload:
            self.fields['a1c'] = forms.ModelChoiceField(queryset=A1C.objects.all(), empty_label="Choose One", required=False, widget=forms.Select(attrs={'class':'req'}))
        else:
            self.fields['a1c'] = forms.ModelChoiceField(queryset=A1C.objects.none(), empty_label="Choose One", widget=forms.Select(attrs={'class':'req'}))
    class Meta:
        model = Log
        fields = ['id_log', 'log_date', 'contract1charter', 'fuel', 'pilot_employee_number', 'co_pilot_employee_number', 'co_pilot_weight',
                  'a1c', 'base', 'a1c_empty_weight', 'pilot_weight', 'opterational_weight', 'customer',
                  'allowable_takeoff_weight', 'payload_available', 'log_number', 'is_submited', 'user_id']
        
class SearchForm(ModelForm):  
    customer = forms.CharField(widget=forms.TextInput(attrs={'id':'cus'}), max_length=30L, required=False)
    model = forms.CharField(widget=forms.TextInput(attrs={'id':'mod'}), max_length=30L, required=False)
    a1c = forms.CharField(max_length=30L, required=False)
    class Meta:
        model = Log
        fields = ['log_date', 'a1c', 'log_number']
        
        
class FuelForm(ModelForm):
    gallons = forms.FloatField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super(FuelForm, self).__init__(*args, **kwargs)
        self.fields['location_id'] = forms.ModelChoiceField(queryset=Location.objects.none(), empty_label="Choose One", required=False)

    class Meta:
        model = Log_Location
        fields = ['id_log_location', 'location_id', 'gallons', 'owner', 'amount']
        
class PilotForm(ModelForm):
    pilot = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(PilotForm, self).__init__(*args, **kwargs)
        cur_emp = kwargs.pop('instance').employee
        self.fields["pilot"].initial = cur_emp.last_name + "," + cur_emp.first_name
    class Meta:
        model = LogEmployee

        
        
                