# # Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render
from flight_log.forms import LoginForm,  LogForm, SearchForm, FuelForm,\
    PilotForm
from flight_log.models import LogSection, Location, Customer, Employee,\
    LogEmployee, Log, A1C, Slot_Purpose, Log_Location, Fuel, Model, Base,\
    Contract1Chater
from django.http import HttpResponseRedirect
import json
from orca.dbusserver import obj
import constant
from django.http.response import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers
import os
from django.contrib import messages
from django_xhtml2pdf.utils import render_to_pdf_response
import zipfile
import cStringIO as StringIO
from utility import convertHtmlToPdf
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from django.template.loader import render_to_string
list_object_pilot = []
list_object_fuel = []

def signin(request):
    form = LoginForm()
    if is_login(request):
        return HttpResponseRedirect(constant.home_url)
    if request.method == constant.POST:
        form = LoginForm(request.POST)
        
        if (form.is_valid()):
            cd = form.cleaned_data
            username = cd.get(constant.employee_number)
            password = cd.get(constant.password)
            time_exp = 0 # clear session when close browser
            request.session[constant.login] = True # you are login now and whenever session expire
            request.session[constant.usernameParam] = username # save login to show
            hrr = HttpResponseRedirect(constant.search_url)
            if cd.get(constant.remember): # if remember me
                time_exp = 86400*7 # a week
                hrr.set_cookie(constant.usernameParam, username, max_age = time_exp) # expire cookie
                hrr.set_cookie(constant.password, password, max_age = time_exp)
            else:
                time_exp = 3600
                if request.COOKIES.has_key(constant.usernameParam):
                    hrr.delete_cookie(constant.usernameParam)
                    hrr.delete_cookie(constant.password)
            request.session.set_expiry(time_exp)
            return hrr
        
    return render(request, constant.signin, {constant.form:form})

def is_login(request): 
    return request.session.get(constant.login, None)

def response_redirect_login(request):
    hrr = HttpResponseRedirect(constant.login)
    return hrr

def logout(request):
    if request.session.get(constant.login, None) :
        del request.session[constant.login]
    return response_redirect_login(request)

def log(request):
    if not is_login(request):
        return response_redirect_login(request)
    link_return = "/"
    """" Initial for flight log table and fuel table """
    
    flight_table = []
    log_emp_list = []
    log_loc_list = []
    log_model = None
    log = None
    max_pax = None
    locations = None
    payload_available = None
    
    log_ob = Log.objects.order_by('log_number').all()
    if log_ob:
        log_count = log_ob.count()
        log_n = log_ob[log_count-1].log_number + 1
    else:
        log_n = 1
    list_emp = Employee.objects.all().order_by('first_name')   
    
    extra_value = 1
    extra_value_pilot = 0
    if "log_id" in request.GET:
        id = request.GET["log_id"]
        a = Log_Location.objects.filter(log_id = id).count()  if id else 0
        if a >= 1: 
            extra_value = 0
        b = LogEmployee.objects.filter(log = id).count()  if id else 0
        if b >= 1: 
            extra_value_pilot = 0
        
    FuelFormSet = modelformset_factory(model = Log_Location, form = FuelForm, 
                                       can_delete=True, max_num=10, extra = extra_value)
    
    PilotFormSet = formset_factory(form = PilotForm, 
                                       max_num=10, extra = extra_value_pilot)
    
    if request.method == 'POST':
        formset = FuelFormSet(request.POST, request.FILES)
        formset_pilot = PilotFormSet(request.POST, request.FILES, prefix='pilots')
        
        form = LogForm(request.POST, customer = request.POST.get('customer'), 
                                model = request.POST.get('model'))
        
        if form.is_valid() and formset.is_valid() and formset_pilot.is_valid():
            pk_id = request.POST.get('id_log')
            
            save_data_form_grid(request, pk_id, form, formset, formset_pilot)
            delete_session(request)
            try:
                submit = request.POST[constant.submit]
                
                if submit:
                    link_return = "/search/"
            except:
                pass
            return HttpResponseRedirect(link_return)

    else:#Get data from DB and reload data into sessions
        delete_session(request)
        try:
            """ Initial data for session flight log  """
            log_id = request.GET["log_id"]
            
            formset = FuelFormSet(queryset=Log_Location.objects.filter(log_id=log_id))
            cur_login_user = LogEmployee.objects.filter(log=log_id).values()
            formset_pilot = PilotFormSet(initial=cur_login_user, prefix='pilots')
            
            log_emp_list = LogEmployee.objects.filter(log = log_id)
            log_loc_list = Log_Location.objects.filter(log_id = log_id)
            log_object = Log.objects.get(id_log = log_id)
            flight_table = LogSection.objects.filter(log = log_object)
            list_flight_log = []
            for flight_log in flight_table:
                list_flight_log.append(serializers.serialize('json', [flight_log, ]))
            request.session[constant.list_flight_log] = list_flight_log
            
            """ Reload data for LogForm Section and AirCraft """
            log_id = request.GET["log_id"]
            log = Log.objects.get(id_log = log_id)
            log_n = log.log_number
            mod = 0

            if log.a1c.id_a1c:
                ac = log.a1c.id_a1c
                if A1C.objects.get(id_a1c = ac):
                    log_model = A1C.objects.get(id_a1c = ac).model
                    mod = log_model.id_model
                    max_pax = log_model.max_passenger
                    payload_available = max_pax - log.opterational_weight
            
            form = LogForm(reload = True, customer = log_object.customer, model = log_object.a1c.model,
                                            instance=log, initial={"model": mod})
            
        except Exception as e:
            form = LogForm(customer = request.POST.get('customer'), model = request.POST.get('model'), 
                        initial={'log_number': log_n, 'user_id': request.session[constant.usernameParam]})
            formset = FuelFormSet(queryset=Log_Location.objects.none())
            list = []
            sic = pic = night = day = vfr = ifr = nvg = co_nvg = 0
            pilot = LogEmployee()
            pilot.sic = sic
            pilot.day = day
            pilot.night = night
            pilot.nvg = nvg
            pilot.vfr = vfr
            pilot.ifr = ifr
            pilot.employee = Employee.objects.get(employee_number = request.session[constant.usernameParam])
            list.append(todict(pilot))
            formset_pilot = PilotFormSet(initial=list, prefix='pilots')
            pass
        
        list_flight_log = get_list_session_object(request)
        locations = []
        for flight_log in list_flight_log:
            if flight_log.flight_data_fuel_station:
                location = Location.objects.get(id_location = flight_log.flight_data_fuel_station.id_location) 
                if location:
                    if location not in locations:
                        locations.append(location)

        import operator
        locations.sort(key=operator.attrgetter("location_name"))
    
    c = {
         'flight_table':flight_table,
        'form': form,
        'formset': formset,
        'formset_pilot': formset_pilot,
        'id': log_n,
        'list_emp': list_emp,
        'locations': locations,
        constant.forms:flight_table,
        "log_emp_list":log_emp_list,
        "log_model" : log_model,
        "max_pax":max_pax,
        "payload_available":payload_available,
        "emp_number" : request.session[constant.usernameParam],
        "log_loc_list" : log_loc_list
        }
    c.update(csrf(request))
    
    return render(request, "flights/index.html", c)

def log_pdf(log_id):

    log_loc_list = Log_Location.objects.filter(log_id = log_id)
    flight_table = LogSection.objects.filter(log = log_id)
        
    flight_leg_details = ['FLIGHT#','SLOT PURPOSE','FROM','OFF','FUEL','TO','ON','MANIFEST#','PASSENGERS',\
                         'EMP BY','T/O W','CG','RANGE','CARGO WEIGHT','FUEL STATION','FUEL AMOUNT',\
                         'AMOUNT','FLIGHT TIME','DAY','NIGHT','IFR','VFR','BLOCK TIME','PATIENTS']
    
    list_flight_log = []
    dic_prop_order = {}
    dic_slot = {}
    dic_from = {}
    dic_off = {}
    dic_fuel = {}
    dic_to = {}
    dic_on = {}
    dic_manifest = {}
    dic_passengers = {}
    dic_emp_by = {}
    dic_tow = {}
    dic_cg = {}
    dic_range = {}
    dic_cargo_weight = {}
    dic_fuel_station = {}
    dic_fuel_amount = {}
    dic_amount = {}
    dic_flight_time = {}
    dic_day = {}
    dic_night = {}
    dic_ifr = {}
    dic_vfr = {}
    dic_block_time = {}
    dic_patient = {}
    dic_total = {}
    
    dic_prop_order['title'] =flight_leg_details[0]
    dic_slot['title'] =flight_leg_details[1]
    dic_from['title'] =flight_leg_details[2]
    dic_off['title'] =flight_leg_details[3]
    dic_fuel['title'] =flight_leg_details[4]
    dic_to['title'] =flight_leg_details[5]
    dic_on['title'] =flight_leg_details[6]
    dic_manifest['title'] =flight_leg_details[7]
    dic_passengers['title'] =flight_leg_details[8]
    dic_emp_by['title'] =flight_leg_details[9]
    dic_tow['title'] =flight_leg_details[10]
    dic_cg['title'] =flight_leg_details[11]
    dic_range['title'] =flight_leg_details[12]
    dic_cargo_weight['title'] =flight_leg_details[13]
    dic_fuel_station['title'] =flight_leg_details[14]
    dic_fuel_amount['title'] =flight_leg_details[15]
    dic_amount['title'] =flight_leg_details[16]
    dic_flight_time['title'] =flight_leg_details[17]
    dic_day['title'] =flight_leg_details[18]
    dic_night['title'] =flight_leg_details[19]
    dic_ifr['title'] =flight_leg_details[20]
    dic_vfr['title'] =flight_leg_details[21]
    dic_block_time['title'] =flight_leg_details[22]
    dic_patient['title'] =flight_leg_details[23]

    for i in range(11):
        dic_prop_order[i] =  dic_prop_order['total']= None
        dic_slot[i] =  dic_slot['total']= None
        dic_from[i] =  dic_from['total']= None
        dic_off[i] =  dic_off['total']= None
        dic_fuel[i] =  dic_fuel['total']= None
        dic_to[i] =  dic_to['total']= None
        dic_on[i] =  dic_on['total']= None
        dic_manifest[i] =  dic_manifest['total']= None
        dic_passengers[i] =  dic_passengers['total']= None
        dic_emp_by[i] = dic_emp_by['total']= None
        dic_tow[i] = dic_tow['total']= None
        dic_cg[i] = dic_cg['total']= None
        dic_range[i] = dic_range['total']= None
        dic_cargo_weight[i] = dic_cargo_weight['total']= None
        dic_fuel_station[i] = dic_fuel_station['total']= None
        dic_fuel_amount[i] = dic_fuel_amount['total']= None
        dic_amount[i] = dic_amount['total']= None
        dic_flight_time[i] = dic_flight_time['total']= None
        dic_day[i] = dic_day['total']= None
        dic_night[i] = dic_night['total']= None
        dic_ifr[i] = dic_ifr['total']= None
        dic_vfr[i] = dic_vfr['total']= None
        dic_block_time[i] = dic_block_time['total']= None
        dic_patient[i] = dic_patient['total']= None
        dic_total[i] = dic_total['total'] =  None
    
    sum_flight_time = sum_cargo = sum_blocktime = sum_patient = sum_pax = 0
    i = 0
    
    for flight_log in flight_table:
        if flight_log.flight_time:
            sum_flight_time = sum_flight_time +  flight_log.flight_time 
        
        if flight_log.flight_data_cargo_weight:
            sum_cargo = sum_cargo + flight_log.flight_data_cargo_weight 
        
        if flight_log.flight_data_block_time:
            sum_blocktime = sum_blocktime + flight_log.flight_data_block_time 
        
        if flight_log.flight_data_patient:
            sum_patient = sum_patient + flight_log.flight_data_patient
        if flight_log.passenger:
            sum_pax = sum_pax + flight_log.passenger 
        
        dic_prop_order[i] = flight_log.order
        
        slot_purpose_name = from_location = to_location = flight_data_fuel_station= amount = None
        vfr = False
        
        if flight_log.slot_purpose_id:
            slot_purpose_name = Slot_Purpose.objects.get(id_slot_purpose = flight_log.slot_purpose_id.id_slot_purpose).slot_purpose_name
        
        dic_slot[i] = slot_purpose_name
        
        if flight_log.from_field:
            from_location = Location.objects.get(id_location = flight_log.from_field.id_location).location_name
            to_location = Location.objects.get(id_location = flight_log.from_field.id_location).location_name
        dic_from[i] = from_location
        
        dic_off[i] = flight_log.off
        dic_fuel[i] = flight_log.fuel_wheels_down
        dic_to[i] = to_location
        dic_on[i] = flight_log.on
        dic_manifest[i] = flight_log.manifest_number
        dic_passengers[i] = flight_log.passenger
        dic_emp_by[i] = flight_log.emp_by
        dic_tow[i] = flight_log.flight_data_tlo_w
        dic_cg[i] = flight_log.flight_data_cg
        dic_range[i] = flight_log.flight_data_range_from
        dic_cargo_weight[i] = flight_log.flight_data_cargo_weight
        
        if flight_log.flight_data_fuel_station:
            flight_data_fuel_station = Location.objects.get(id_location = flight_log.flight_data_fuel_station.id_location).location_name
        dic_fuel_station[i] = flight_log.flight_data_fuel_station
        
        dic_fuel_amount[i] = flight_log.flight_data_fuel_amount
        
        if flight_log.flight_data_amount:
            amount = flight_log.flight_data_amount
        dic_amount[i] = amount
        
        dic_flight_time[i] = flight_log.flight_time
        dic_day[i] = flight_log.day
        dic_night[i] = flight_log.night
        dic_ifr[i] = flight_log.all_ifr
        
        if flight_log.all_nfr:
            vfr = True
        dic_vfr[i] = vfr
        
        dic_block_time[i] = flight_log.flight_data_block_time
        dic_patient[i] = flight_log.flight_data_patient
        
        i = i + 1
    ## end for
    
    dic_flight_time['total'] = sum_flight_time if sum_flight_time > 0 else None
    dic_cargo_weight['total'] = sum_cargo if sum_cargo > 0 else None
    dic_block_time['total'] = sum_blocktime if sum_blocktime > 0 else None
    dic_patient['total'] = sum_patient if sum_patient > 0 else None
    dic_passengers['total'] = sum_pax if sum_pax > 0 else None
        
    list_flight_log.append(dic_prop_order)
    list_flight_log.append(dic_slot)
    list_flight_log.append(dic_from)
    list_flight_log.append(dic_off)
    list_flight_log.append(dic_fuel)
    list_flight_log.append(dic_to)
    list_flight_log.append(dic_on)
    list_flight_log.append(dic_manifest)
    list_flight_log.append(dic_passengers)
    list_flight_log.append(dic_emp_by)
    list_flight_log.append(dic_tow)
    list_flight_log.append(dic_cg)
    list_flight_log.append(dic_range)
    list_flight_log.append(dic_cargo_weight)
    list_flight_log.append(dic_fuel_station)
    list_flight_log.append(dic_fuel_amount)
    list_flight_log.append(dic_amount)
    list_flight_log.append(dic_flight_time)
    list_flight_log.append(dic_day)
    list_flight_log.append(dic_night)
    list_flight_log.append(dic_ifr)
    list_flight_log.append(dic_vfr)
    list_flight_log.append(dic_block_time)
    list_flight_log.append(dic_patient)
    
    """ Reload data for LogForm Section and AirCraft """
    log = Log.objects.get(id_log = log_id)
    
    a1c_name = A1C.objects.get(id_a1c = log.a1c.id_a1c)
    id_model = a1c_name.model.id_model
    model_name = Model.objects.get(id_model = id_model)
    max_gross_weight = model_name.max_gross_weight
    me_load_schedule_cg_range_from = model_name.me_load_schedule_cg_range_from
    me_load_schedule_cg_range_to = model_name.me_load_schedule_cg_range_to
    base_name = Base.objects.get(id_base = log.base.id_base)
    contract1charter_name = customer_name = customer_id = None
    if log.customer:
        customer_name = Customer.objects.get(id_customer = log.customer.id_customer)
        customer_id = customer_name.cus_name
    if log.contract1charter:
        contract1charter_name = Contract1Chater.objects.get(id_contract1chater = log.contract1charter.id_contract1chater)
    log = log.__dict__
    
    PilotFormSet = formset_factory(form = PilotForm, 
                                       max_num=10, extra = 0)
    cur_login_user = LogEmployee.objects.filter(log=log_id).values()
    formset_pilot = PilotFormSet(initial=cur_login_user, prefix='pilots')
    
    log['a1c_id'] = a1c_name.a1c_name
    log['model_id'] = model_name.mo_name
    log['base_id'] = base_name.base_name
    log['customer_id'] = customer_id
    log['contract1chater_id'] = contract1charter_name
    log['max_gross_weight']=  max_gross_weight
    log['payload_available'] = log['max_gross_weight'] - log['opterational_weight']
    log['me_load_schedule_cg_range_from'] = me_load_schedule_cg_range_from
    log['me_load_schedule_cg_range_to'] = me_load_schedule_cg_range_to
       
    c = {
        'formset_pilot':formset_pilot,
        'log': log,
        'list_flight_log':list_flight_log,
        "log_loc_list" : log_loc_list
        }
    return c

""" Save data in form, pilot section and fuel section """
def save_data_form_grid(request, pk_id, form, formset, formset_pilot):
    if pk_id:
        LogSection.objects.filter(log = pk_id).delete()
        log = Log.objects.get(pk=pk_id)
        if log:
            form = LogForm(request.POST, customer = request.POST.get('customer'), 
                            model = request.POST.get('model'), instance=log)
            
    form = form.save(commit = False)
    try:
        em = Employee.objects.filter(employee_number = request.session[constant.usernameParam])
        if em:
            form.pilot_employee_number = em[0] 
    except:
        pass
    submit = None
    try:
        submit = request.POST.get("submit")
    except Exception as e:
        pass
    if submit:
        form.is_submited = True
        messages.success(request, 'Flight Log is submitted successfully.')
    else:
        messages.info(request, 'Flight Log is saved successfully.')
        
    form.save()
    
    log_ob = Log.objects.order_by('log_number').all()
    log_count = log_ob.count()

    formset = formset.save(commit=False)
    for f in formset:
        f.log_id = Log.objects.get(pk=pk_id) if pk_id else log_ob[log_count-1]
        f.save()
    
    '''Delete older Log Employee'''
    if pk_id:
            LogEmployee.objects.filter(log = pk_id).delete()    
    for f in formset_pilot:
        f = f.save(commit=False)
        f.log = Log.objects.get(pk=pk_id) if pk_id else log_ob[log_count-1]
        f = f.save()
    # Flight Leg section (Pop up)
    try:
        list_flight_log = get_list_session_object(request, Log.objects.filter(id_log = pk_id)[0])
    except Exception as e:
        list_flight_log = get_list_session_object(request, log_ob[log_count-1])
        
    for flight_log in list_flight_log:
        flight_log.save()


def home(request):
    if not is_login(request):
        return response_redirect_login(request)
    announce_message = None
    if request.method == constant.POST:
        data = request.POST
        
        list_log_id = []
        delete = None
        
        try:
            list_log_id = data.getlist(constant.flight_log_id)
            delete = data[constant.delete]
        except:
            pass
        
        for id in list_log_id:
            try:
                if data[constant.row_check + id]:
                    flight_log = Log.objects.get(id_log = id)
                    
                    if delete:
                        flight_log.delete()
                        announce_message = constant.mess_delete_suc
                    else:
                        flight_log.is_submited = True
                        flight_log.save()
                        announce_message = constant.mess_submit_suc
            except:
                pass

    empty_flight_log = None
    LIST_FLIGHT_LOG = []
    allFlightLog = Log.objects.filter(user_id = request.session[constant.usernameParam],
                                      is_submited = False) 
    
    for flight in allFlightLog:
        LIST_FLIGHT_LOG.append(flight)
        
    if len(LIST_FLIGHT_LOG) == 0:
        empty_flight_log = " "
        
    paginator = Paginator(LIST_FLIGHT_LOG, constant.number_page)
    page = request.GET.get(constant.page)
     
    try:
        LIST_FLIGHT_LOG = paginator.page(page)
    except PageNotAnInteger:
        LIST_FLIGHT_LOG = paginator.page(1)
    except EmptyPage:
        LIST_FLIGHT_LOG = paginator.page(paginator.num_pages)

    return render(request, constant.home_page,{constant.empty_flight_log:empty_flight_log,
                                        constant.list_flight_log:LIST_FLIGHT_LOG,
                                        constant.announce_mess : announce_message})



def print_pdf(request):
    log_id = request.GET.get('log_id', False)
    if not log_id:
        #return render(request, "flights/pdf.html", log_pdf(3))
        return HttpResponse("<html><body>please select a flight log to print</body></html>")
    # one file
    if(log_id.find(',') == -1):
        #return render(request, "flights/pdf.html", log_pdf(log_id))
        return render_to_pdf_response("flights/pdf.html",  log_pdf(log_id), 'flight_log_' + log_id + '.pdf')
    
    arr = log_id.split(',')
    dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) +'/../helicopters/static/media/pdf_export/'
    pdf_files = []
    for nu in arr:
        pdf_file = 'flight_log_' + nu + '.pdf'
        pdf_files.append(pdf_file)
        try:
            "--------- start try pdf "               
            pdf = render_to_string("flights/pdf.html", log_pdf(nu))
            convertHtmlToPdf(pdf,dirname + pdf_file) 
        except Exception as e:
            print "---------error on pdf "
            print e
        finally:
            pass             

    # zip all file to one
    buffer = StringIO.StringIO()
    zf = zipfile.ZipFile(buffer, mode='w')
    for pdf_file in pdf_files:
        try:
            zf.write(dirname + pdf_file, pdf_file)
        finally:
            pass
    zf.close()
    buffer.seek(0)
    response = HttpResponse(buffer.read())
    name = log_id.replace(',','')
    response['Content-Disposition'] = 'attachment; filename=flight_log_' + name + '.zip'
    response['Content-Type'] = 'application/x-zip'
    return response


def search (request):
    if not is_login(request):
        return response_redirect_login(request)
    form = SearchForm()
    empty_flight_log = None
    
    LIST_FLIGHT_LOG = Log.objects.filter(user_id = request.session[constant.usernameParam], is_submited = True) 
    if len(LIST_FLIGHT_LOG) == 0:
        empty_flight_log = " " 
        
    paginator = Paginator(LIST_FLIGHT_LOG, constant.number_page) 
    page = request.GET.get(constant.page)
    try:
        LIST_FLIGHT_LOG = paginator.page(page)
    except PageNotAnInteger:
        LIST_FLIGHT_LOG = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        LIST_FLIGHT_LOG = paginator.page(paginator.num_pages)
    
    c = {
        constant.form: form,
        constant.empty_flight_log:empty_flight_log,
        constant.list_flight_log:LIST_FLIGHT_LOG
        }
    
    return render(request, constant.home_submitted, c)
    

def get_list_session_object(request, log = None):
    list_log_section = []
    try:
        data = request.session[constant.list_flight_log]
        for obj in data:
            obj = json.loads(obj)
            list_log_section.append(deserializer_log_section(obj[0]['fields'], obj[0]['pk'], log))
    except:
        pass
    return list_log_section


"""
    Revert to object
"""        
def deserializer_log_section(obj1, id_log_section, log = None):
    log_section_object = LogSection()
    log_section_object.id_log_section = id_log_section
    log_section_object.all_ifr = obj1['all_ifr']
    log_section_object.all_nfr = obj1['all_nfr']
    log_section_object.log = log
    log_section_object.order = obj1['order']
    log_section_object.flight_time = obj1['flight_time']
    log_section_object.load_schedule = obj1['load_schedule']
    log_section_object.manifest_number = obj1['manifest_number']
    log_section_object.off = obj1['off']
    log_section_object.on = obj1['on']
    log_section_object.passenger = obj1['passenger']
    if obj1['from_field'] != None:
        log_section_object.from_field = \
            Location.objects.get(id_location = obj1['from_field'])
    else:
        log_section_object.from_field = obj1['from_field']
    if obj1['to'] != None:
        log_section_object.to = Location.objects.get(id_location = obj1['to'])
    else:
        log_section_object.to = obj1['to']
    if obj1['emp_by'] != None:
        log_section_object.emp_by = Customer.objects.get(id_customer = obj1['emp_by'])
    else:
        log_section_object.emp_by = obj1['emp_by']
    log_section_object.flight_data_amount = obj1['flight_data_amount']
    log_section_object.flight_data_block_time = obj1['flight_data_block_time']
    log_section_object.flight_data_cargo_weight = obj1['flight_data_cargo_weight']
    log_section_object.flight_data_cg = obj1['flight_data_cg']
    log_section_object.flight_data_fuel = obj1['flight_data_fuel']
    log_section_object.fuel_wheels_down = obj1['fuel_wheels_down']
    log_section_object.partial_nfr = obj1['partial_nfr']
    if obj1['slot_purpose_id'] != None:
        log_section_object.slot_purpose_id = \
            Slot_Purpose.objects.get(id_slot_purpose = obj1['slot_purpose_id'])
    else:
        log_section_object.slot_purpose_id = obj1['slot_purpose_id']
    if obj1['flight_data_fuel_station'] != None:
        log_section_object.flight_data_fuel_station = \
            Location.objects.get(id_location = obj1['flight_data_fuel_station'])
    else:
        log_section_object.flight_data_fuel_station = obj1['flight_data_fuel_station']
    log_section_object.flight_data_fuel_amount = obj1['flight_data_fuel_amount']
    log_section_object.flight_data_patient = obj1['flight_data_patient']
    log_section_object.flight_data_range_from = obj1['flight_data_range_from']
    log_section_object.flight_data_range_to = obj1['flight_data_range_to']
    log_section_object.flight_data_tlo_w = obj1['flight_data_tlo_w']
    log_section_object.day = obj1['day']
    log_section_object.night = obj1['night']
    log_section_object.pilot_nvg = obj1['pilot_nvg']
    log_section_object.co_pilot_nvg = obj1['co_pilot_nvg']
    return log_section_object
    

def convert_dict(station, gallon, owner, amount):
    return {
            constant.location:station,
            constant.gallon:gallon,
            constant.owner:owner,
            constant.amount:amount,
            }
    
    
def delete_session(request):
    '''
       Delete session after save into database 
    '''    
    try:
        del request.session[constant.list_flight_log]
        del request.session[constant.list_fuel_cal]
        del request.session["current_index"]
    except:
        pass

def fuel_station_list(request): 
    list_flight_log = get_list_session_object(request)
    list_fuel_station = {}
    for flight_log in list_flight_log:
        if flight_log.flight_data_fuel_station:
            location = Location.objects.get(id_location = flight_log.flight_data_fuel_station.id_location) 
            if location:
                list_fuel_station[str(location.id_location)] = str(location.location_name)
    return list_fuel_station

def check_float(num):
    check = num.replace('.','',1).isnumeric()
    return check

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.iteritems() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj