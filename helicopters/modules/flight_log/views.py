# # Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render
from flight_log.forms import LoginForm,  LogForm, SearchForm, FuelForm,\
    PilotForm
from flight_log.models import LogSection, Location, Customer, Employee,\
    LogEmployee, Log, A1C, Slot_Purpose, Log_Location, Fuel
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
from PyPDF2 import PdfFileWriter
from django.forms.models import modelformset_factory

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
    
    log_ob = Log.objects.order_by('log_number').all()
    if log_ob:
        log_count = log_ob.count()
        log_n = log_ob[log_count-1].log_number + 1
    else:
        log_n = 1
    list_emp = Employee.objects.all().order_by('first_name')   
    
    extra_value = 1
    extra_value_pilot = 1
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
    
    PilotFormSet = modelformset_factory(model = LogEmployee, form = PilotForm, 
                                       can_delete=True, max_num=10, extra = extra_value_pilot)
    
    if request.method == 'POST':
        print "moi vao post"
        
        formset = FuelFormSet(request.POST, request.FILES)
        formset_pilot = PilotFormSet(request.POST, request.FILES, prefix='pilots')
        
        form = LogForm(request.POST, customer = request.POST.get('customer'), 
                                model = request.POST.get('model'))
        
        if form.is_valid() and formset.is_valid() and formset_pilot.is_valid():
            pk_id = request.POST.get('id_log')
            
            save_data_form_grid(request, pk_id, form, formset, formset_pilot)
            print "sau goi ham  save_data_form_grid"
            delete_session(request)
            try:
                submit = request.POST[constant.submit]
                
                if submit:
                    print "vao submit"
                    link_return = "/search/"
            except:
                print "vao pass form.is_valid() and list_object"
                pass
            return HttpResponseRedirect(link_return)

    else:#Get data from DB and reload data into sessions
        delete_session(request)
        
        try:
            """ Initial data for session flight log  """
            log_id = request.GET["log_id"]
            formset = FuelFormSet(queryset=Log_Location.objects.filter(log_id=log_id))
            formset_pilot = PilotFormSet(queryset=LogEmployee.objects.filter(log=log_id), prefix='pilots')
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
            
            form = LogForm(reload = True, customer = log_object.customer, model = log_object.a1c.model,
                                            instance=log, initial={"model": mod})
            
        except Exception as e:
            form = LogForm(customer = request.POST.get('customer'), model = request.POST.get('model'), 
                        initial={'log_number': log_n, 'user_id': request.session[constant.usernameParam]})
            formset = FuelFormSet(queryset=Log_Location.objects.none())
            formset_pilot = PilotFormSet(queryset=LogEmployee.objects.none(), prefix='pilots')
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
        "emp_number" : request.session[constant.usernameParam],
        "log_loc_list" : log_loc_list
        }
    c.update(csrf(request))
    
    return render(request, "flights/index.html", c)


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
        print "get employee number"
        pass
    submit = None
    try:
        submit = request.POST.get("submit")
    except Exception as e:
        print 'Loi o kt submit'
        print e
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
        
    formset_pilot = formset_pilot.save(commit=False)
    for f in formset_pilot:
        f.log = Log.objects.get(pk=pk_id) if pk_id else log_ob[log_count-1]
        f.save()
    # Flight Leg section (Pop up)
    try:
        list_flight_log = get_list_session_object(request, Log.objects.filter(id_log = pk_id)[0])
    except Exception as e:
        print 'save trong ham save 230'
        print e
        list_flight_log = get_list_session_object(request, log_ob[log_count-1])
        
    for flight_log in list_flight_log:
        flight_log.save()


def home(request):
    print "submit home"
    if not is_login(request):
        return response_redirect_login(request)
    print "sau check login"
    announce_message = None
    print"truoc check POST"
    if request.method == constant.POST:
        print "vao check POST"
        data = request.POST
        print "data of request"
        print data
        
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
    
    i = request.GET["i"]
    arr = i.split(',')
    for nu in arr:
        pdf = render_to_pdf_response("flights/pdf.html", '', 'flight_log_' + nu + '.pdf')
        # save pdf file in server
        pdf_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/../helicopters/static/media/pdf_export/flight_log_' + nu + '.pdf'
        op = PdfFileWriter() 

        op.addBlankPage(793, 1122)
        ops = file(pdf_path, "wb")  
        op.write(ops)  
        ops.close() 
    # zip all file to one
    buffer = StringIO.StringIO()
    zf = zipfile.ZipFile(buffer, mode='w')
    for nu in arr:
        try:
            zf.write(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/../helicopters/static/media/pdf_export/flight_log_' + nu + '.pdf', 'flight_log_' + nu + '.pdf')
        finally:
            pass
    zf.close()
    buffer.seek(0)
    response = HttpResponse(buffer.read())
    if(i.find(',') == -1):
        return pdf
    else:
        name = i.replace(',','')
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

