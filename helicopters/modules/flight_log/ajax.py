from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from flight_log.forms import FlightLogDetail, PilotForm
from dajax.core import Dajax
from dajaxice.utils import deserialize_form
from django.core import serializers
from flight_log.views import get_list_session_object, fuel_station_list, todict
from django.shortcuts import render
from django.template.loader import render_to_string
from flight_log.models import A1C, Model, Employee, Contract1Chater, Log,\
    Location,UserTemp, LogEmployee
import constant
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from utility import format6
@dajaxice_register
def add_flight_log(request, next_order_id, fuel, max_pax):
    '''
        Get list object from session
    '''
    list_log_section = get_list_session_object(request)
    try:
        fuel = list_log_section[len(list_log_section)-1].fuel_wheels_down
    except:
        pass
    '''
        Initial Flight Log Session form 
    '''
    form = FlightLogDetail(next_order_id = next_order_id, fuel = fuel, max_pax = max_pax)
    
    render = render_to_string(constant.popup_page ,{constant.single_form:form,
                                                    constant.IS_EDIT : "false"})
    
    dajax = Dajax()
    dajax.script(constant.prepend_table_popup %render.replace('\n', ""))
    pour_fuel_station_popup(dajax)
    return dajax.json()


@dajaxice_register
def send_email(request, arr):
    render = render_to_string(constant.email_popup_page)
    dajax = Dajax() 
    html = render.replace('\n', "")
    dajax.script(constant.append_flight_email_popup %html)
    emails = UserTemp.objects.filter(employee_number=request.session[constant.usernameParam])
    html = ''
    val = ''
    j = 0
    from flight_log.views import log_pdf
    from flight_log.utility import convertHtmlToPdf
    for i in arr:
        log = Log.objects.get(id_log=i) or None
        if not log:
            continue
        num_formated = format6(log.log_number)
        html = html + "<div class=\"attack_file\"><input class=\"attack_file\" readonly=\"true\" name=\"attack_file_" + i + "\" value=\"" + num_formated +"\" type=\"text\" /><div class=\"close-attack\">x</div></div>"
        if(j == 0):
            val = val + num_formated
            j = 1
        else:
            val = val + ',' + num_formated
        pdf_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/../helicopters/static/media/pdf_export/' + num_formated
        pdf = render_to_string("flights/pdf.html", log_pdf(i))
        convertHtmlToPdf(pdf, pdf_path)
        
    # POST lost dot, so we remove it and add on recived
    val = val.replace(".pdf", "")
    html = html + '<input class="hiden_attack" name="hiden_attack" val="'+ val + '" type="input" />'
    dajax.script("var e_html = '" + html +"';\
        jQuery('.attack_files').html(e_html);")
    for email in emails:
        dajax.script("jQuery('.email_from').val('" + email.email + "');")
    return dajax.json()

    
@dajaxice_register
def edit_flight_log(request, index, max_pax, is_submitted = False):
    dajax = Dajax()
    
    request.session["current_index"] = index - 1
    
    fuel_station_name = None
    list_log_section = get_list_session_object(request)
    edit_object = list_log_section[index-1]
    
    if edit_object.flight_data_fuel_station:
        fuel_station_name = edit_object.flight_data_fuel_station.location_name
    form = FlightLogDetail(instance = edit_object, partial_range = edit_object.flight_time,
                           max_pax = max_pax)
    
    render = render_to_string(constant.popup_page ,{constant.single_form:form,
                                                    constant.IS_EDIT : "true",
                                                    constant.is_submitted:is_submitted})
    dajax.script(constant.prepend_table_popup %render.replace('\n', ""))
    dajax.script("if($(\"#id_load_schedule\").is(\":checked\")){\
            $(\"#id_flight_data_cg\").parent().find(\"span span\").css(\"display\", \"none\");\
            $(\"#id_flight_data_range_from\").parent().find(\"span span\").css(\"display\", \"none\");\
            $(\"#id_flight_data_range_to\").parent().find(\"span span\").css(\"display\", \"none\");\
            }");

    '''
        Generate data into fuel station
    '''
    pour_fuel_station_popup(dajax)
    if fuel_station_name:
        scr_name = 'set_fuel_station("'+ str(fuel_station_name) +'");' 
        dajax.script(scr_name)
    return dajax.json()
    
@dajaxice_register
def delete_flight_log(request, index, loc_temp, max_pax, list_fuel_location, co_pilot, id_log):
    dajax = Dajax()
    
    list_object = get_list_session_object(request)
    
    count = 0
    current_object = None
    for obj in list_object:
        if obj.order == int(index):
            current_object = obj
            
    for obj in list_object:
        if obj.flight_data_fuel_station and current_object.flight_data_fuel_station:
            if obj.flight_data_fuel_station == current_object.flight_data_fuel_station:
                if str(obj.flight_data_fuel_station.location_name).strip() in list_fuel_location:
                    count += 1
    if count == 1:
        dajax.alert(constant.announce_mess_fuel_location_change);
        return dajax.json()
    
    '''
        Change all session here
    '''
    temp_list = []
    i = 1
    for obj in list_object:
        if obj.order != int(index):
            obj.order = i
            temp_list.append(serializers.serialize(constant.json, [obj, ]))
            i += 1 
    
    '''
        Add all flight leg into session
    '''
    request.session[constant.list_flight_log] = temp_list
    ''' Remove old flight legs table at home page '''
    dajax.remove(constant.id_rs_flight_log_form)
    ''' Render data into new flight legs table '''
    render = render_to_string(constant.flight_log_table_page,
                              {constant.forms:get_list_session_object(request)})
    ''' Insert new flight legs table into home  page '''
    dajax.script(constant.prepend_flight_log_table 
                 %render.replace('\n', ""))
    
    '''
        Announce message in home page if passenger of model is out of range
    '''
    list_log_section = []
    try:
        list_log_section = get_list_session_object(request)
    except:
        pass
    msg = pax_error(max_pax, list_log_section)
    dajax.script(constant.append_error_mess % msg)
    if msg:
        dajax.script(constant.remove_save_succ_mess)
    
    ''' Modify data for hidden combobox and used for fuel expenses sessio '''
    dajax.remove("#hiddenff option")
    dajax.remove("#fuel_tbl select option")
    import operator
    sorted_list_fuel_station = sorted(fuel_station_list(request).items(), key=operator.itemgetter(1))
    for local_id, name in sorted_list_fuel_station:
        dajax.append('#hiddenff', 'innerHTML', "<option value="+str(local_id)+">"+str(name)+"</option>")
        dajax.append('#fuel_tbl select', 'innerHTML', "<option value="+str(local_id)+">"+str(name)+"</option>")
    load_copilot_sub(request, co_pilot, id_log, dajax)
    dajax.script('load_combo();')
    dajax.script("jQuery('#result').val('" + str(loc_temp) + "');")
    dajax.script('change_location_del();')
    return dajax.json()
     
def save_add_case(request, result):
    list_object = []
    try:
        list_object = request.session[constant.list_flight_log]
    except:
        pass
    list_object.append(serializers.serialize(constant.json, [result, ]))
    ''' Reinput data into session for flight legs saved '''
    request.session[constant.list_flight_log] = list_object
    ''' Change new order for flight log '''
    request.session[constant.limit] = result.order+1
    
    '''
        This "msg" will be a new row at table flight log
    '''
    msg = "<tr>\
        <td>"+str(result.order)+"</td>\
        <td>"+str(result.from_field)+"</td>\
        <td>"+str(result.to)+"</td>\
        <td class = \"cls_pas\">"+str(result.passenger)+"</td>\
                        <td>"+str(result.off)+"</td>\
        <td>"+str(result.on)+"</td>\
        <td class = \"cls_flight_time\">"+str(result.flight_time)+"</td>\
        <td>"+str(result.flight_data_tlo_w)+"</td>\
        <td>"+str(result.flight_data_cg)+"</td>\
        <td>"+str(result.flight_data_fuel)+"</td>\
        <td class = \"cls_cargo\">"+str(result.flight_data_cargo_weight)+"</td>\
        <td class = \"cls_block_time\">"+str(result.flight_data_block_time)+"</td>\
        <td class = \"patient\">"+str(result.flight_data_patient)+"</td>\
        <td>\
            <a href=\"#log-box\" class = \"edit_flight_log\">\
                <img src=\"/static/media/edit.png\" \
                    alt=\"add flight log\"> \
            </a>\
            <a href=\"#log-box\" class = \"delete_flight_log\">\
                <img src=\"/static/media/delete.png\" \
                    alt=\"delete flight log\"> \
            </a>\
        </td>\
        </tr>"
    return  msg
     
@dajaxice_register
def save_flight_log(request, forms, max_pax, partial_range, 
                    before_fuel_location, list_fuel_location,
                    is_edit, co_pilot, id_log):
    dajax = Dajax()
    
    ''' Remove all errors message in popup '''
    dajax.remove(constant.class_error_mess)
    ''' Generate new form '''
    form = FlightLogDetail(deserialize_form(forms), partial_range = partial_range, max_pax = max_pax)
    if form.is_valid():
        ''' Get object form data '''
        result = form.save(commit = False)
        
        ''' If add new flight legs '''
        if is_edit == "false":
            dajax.script(constant.append_flight_log_form 
                         %save_add_case(request, result))
            """
                Announce after saved
            """
            dajax.script(constant.append_save_succ_mess %constant.add_succ_mess)
        
        ''' Edit flight legs '''
        if is_edit == "true":
            current_location = None
            location_name = None
            try:
                location = Location.objects.get(id_location = before_fuel_location)
                if location:
                    before_fuel_location = location.location_name
            except:
                pass
        

            if result.flight_data_fuel_station:
                current_location = result.flight_data_fuel_station.location_name
                
            '''
                Check location in fuel expenses is conflict with flight log session or not
                - If not when change
                - If has conflict so announce and return
            '''
            remove_older_location = False
            list_location_temp = ['Choose One']
            list_object = get_list_session_object(request)
            
            ''' Get older station location '''
            for obj in list_object:
                if obj.flight_data_fuel_station:
                    location_name = obj.flight_data_fuel_station.location_name
                    if location_name:
                        list_location_temp.append(str(location_name.strip()))
                if before_fuel_location == str(location_name) != "None" and not remove_older_location:
                    list_location_temp.remove(before_fuel_location)
                    remove_older_location = True
            ''' Input new station into list '''
            if current_location:   
                list_location_temp.append(current_location.strip())
            ''' Verify whether conflict '''    
            for val in list_fuel_location:
                if str(val) != "None" and str(val) != "" and str(val) not in list_location_temp:
                    dajax.alert(constant.announce_mess_fuel_location_change)
                    pour_fuel_station_popup(dajax)
                    dajax.script(constant.prevent_default)
                    return dajax.json()
                
            ''' Change data of flight log in session '''    
            lst = request.session[constant.list_flight_log]
            lst[request.session["current_index"]] = serializers.serialize(constant.json, [result, ])
            request.session[constant.list_flight_log] = lst
            
            """
                Announce after edited
            """
            dajax.script(constant.append_save_succ_mess %constant.edited_succ_mess)
            
        ''' Modify data for hidden combobox and used for fuel expenses sessio '''
        dajax.remove("#hiddenff option")
        import operator
        sorted_list_fuel_station = sorted(fuel_station_list(request).items(), key=operator.itemgetter(1))
        dajax.append('#fuel_tbl select', 'innerHTML', "<option value="">Choose One</option>")
        for local_id, name in sorted_list_fuel_station:
            dajax.append('#hiddenff', 'innerHTML', "<option value="+str(local_id)+">"+str(name)+"</option>")
     
        '''
            Modify flight legs table
        '''
        dajax.remove(constant.id_rs_flight_log_form)
        render = render_to_string(constant.flight_log_table_page,
                                  {constant.forms:get_list_session_object(request)})
        dajax.script(constant.prepend_flight_log_table 
                     %render.replace('\n', ""))
        
        dajax.script('load_combo();')
        dajax.script('change_location();')
        
    else:#Form not valid
        dajax.remove(constant.class_pop_main)
        render = render_to_string(constant.popup_page ,{constant.single_form:form})
        dajax.script(constant.prepend_table_popup %render.replace('\n', ""))
        dajax.script("if(!$('#id_load_schedule').is(':checked') & \
                ($('#id_flight_data_range_from').val() == '' || \
                $('#id_flight_data_range_to').val() == '')){\
                $('#range_to_error_id').css('display','block');}")
        
        ''' Pour data for fuel station in popup '''
        pour_fuel_station_popup(dajax)
        
        dajax.script(constant.prevent_default)
    
    ''' Announce message when edit flight legs '''
    list_log_section = []
    try:
        list_log_section = get_list_session_object(request)
    except:
        pass
    msg = pax_error(max_pax, list_log_section)
    
    dajax.script(constant.append_error_mess % msg)
    if msg:
        dajax.script(constant.remove_save_succ_mess)
        
    pour_fuel_station_popup(dajax)
    
    ''' Reload pilot section'''
    load_copilot_sub(request, co_pilot, id_log, dajax)
    return dajax.json()


@dajaxice_register(method=constant.GET)
def ajax_contract_request(request, cus_id):
    list_contract = []
    if cus_id:
        list_contract = Contract1Chater.objects.filter(customer=cus_id)
    dic = []
    for con in list_contract:
        dic.append({'name': con.con_name, 'id': con.id_contract1chater})
    return simplejson.dumps({constant.list_contract: dic})


@dajaxice_register(method=constant.GET)
def ajax_model_request(request, mode):
    
    from_value = ""
    to_value = ""
    mass_gross = ""
    list_ac = []
    model_obj = None
    msg = ""
    max_pax = ""
    dic = []
    
    if mode:
        list_ac = A1C.objects.filter(model=mode)
        model_obj = Model.objects.get(id_model=mode)
     
        for c in list_ac:
            dic.append({'name': c.a1c_name, 'id': c.id_a1c})
            
        """
            Check max_passenger of model
        """
        list_log_section = []
        mass_gross = model_obj.max_gross_weight
        from_value = model_obj.me_load_schedule_cg_range_from
        to_value = model_obj.me_load_schedule_cg_range_to
        max_pax = model_obj.max_passenger
        try:
            list_log_section = get_list_session_object(request)
        except:
            pass
        msg = pax_error(model_obj.max_passenger, list_log_section)
    """
        Render to html
    """
    return simplejson.dumps({'list_ac': dic, 
                             'mass_gross':mass_gross,
                             'from':from_value,
                             'to' : to_value,
                             'pass_message':msg,
                             'delete_mess':"delete",
                             'max_pax': max_pax})

@dajaxice_register(method=constant.GET)
def ajax_fill_pilot(request):
    list_emp = Employee.objects.all()
    list_emp_name = []
    list_emp_id = []
    for e in list_emp:
        list_emp_name.append(e.emp_name)
        list_emp_id.append(e.id_employee)
    return simplejson.dumps({'list_emp_name': list_emp_name, 'list_emp_id': list_emp_id})

def pax_error(current_max_pass, list_log_section):
    list_order_object_error = ""
    msg = ""
    
    try:
        for flight_log in list_log_section:
            if long(current_max_pass) < long(flight_log.passenger):
                list_order_object_error += str(flight_log.order) + ", "
    except:
        pass
    
    if list_order_object_error:
        msg = constant.msg_out_of_passenger %list_order_object_error[:-2]
    return msg

"""
    Search by dynamic params, pagination by search results and draft log
"""
@dajaxice_register(method=constant.GET)
def ajax_search(request, pg, is_sub, **param):
    
    kwargs = {
        constant.user_id: request.session[constant.usernameParam],
        constant.is_submited: is_sub
    }

    for key, value in param.iteritems():
        if key == constant.log_num and value and value.isnumeric():
            kwargs[ constant.log_number ] = value
        elif key == constant.customer and value:
            kwargs[ constant.contract1charter__customer__cus_name__ilike ] = '%' + value.strip() + '%'
        elif key == constant.model and value:
            kwargs[ constant.a1c__model__mo_name__ilike ] = '%' + value.strip() + '%'
        elif key == constant.date and value:
            # change format of date
            import datetime
            try:
                d = datetime.datetime.strptime(value, constant.format_mdy)          
                date_new = d.strftime(constant.format_ymd)
                kwargs[ constant.log_date ] =  date_new
            except:
                kwargs[ constant.log_date ] =  None
        elif key == constant.ac and value:
            kwargs[ constant.a1c__a1c_name__ilike ] = '%' + value + '%'
        
    allFlightLog = Log.objects.filter(**kwargs)
       
    paginator = Paginator(allFlightLog, constant.number_page) 
    try:
        # pg is passed as page current  
        allFlightLog = paginator.page(pg)
    except PageNotAnInteger:
        allFlightLog = paginator.page(1)
    except EmptyPage:
        allFlightLog = paginator.page(paginator.num_pages)
    
    json = []
    page = []
    if allFlightLog:
        page = allFlightLog.paginator.page_range
        json = get_json_for_search(allFlightLog)
  
    return simplejson.dumps({constant.list_json:json, constant.page: page, 
                             constant.page_current: allFlightLog.number, 'is_sub':is_sub })   


""" create json array for search """
def get_json_for_search(allFlightLog):
    json = []
    customer = ""
    mo_name = ""
    
    for flight in allFlightLog:
        
        contract = str(flight.contract1charter) if flight.contract1charter else ""
        customer = str(flight.customer) if flight.customer else ""
            
        if flight.a1c:
            a1c_name = str(flight.a1c)
            mo_name = str(flight.a1c.model) if flight.a1c.model else ""
        else:
            a1c_name = ""
            
        date = str(flight.log_date) if flight.log_date else ""
    
        json.append({constant.id_log: flight.id_log, constant.log_number: flight.log_number, 
                     constant.cus: customer, constant.date: date,
                     constant.contract: contract, 
                     constant.mo_name: mo_name, constant.a1c_name : a1c_name})
    return json

def pour_fuel_station_popup(dajax):
    ''' Pour data for fuel station in popup '''
    locations = Location.objects.all().order_by("location_name")
    list_loc_name = []
    for location in locations:
        list_loc_name.append(location.location_name.encode('ascii', 'ignore'))
    dajax.script("load_ajax_popop("+str(list_loc_name)+");")

@dajaxice_register(method=constant.GET)
def load_copilot(request, co_pilot, id_log):
    dajax = Dajax()
    load_copilot_sub(request, co_pilot, id_log, dajax)
    '''Return'''
    return dajax.json()

def load_copilot_sub(request, co_pilot, id_log, dajax):
    '''Create formset'''
    PilotFormSet = formset_factory( form = PilotForm, 
                                       max_num=10, extra = 0)
    '''Load data for table'''
    list = []
    '''Get list flight log in session and calculate sum value'''
    lst_flight_log = get_list_session_object(request)
    sic = pic = night = day = vfr = ifr = nvg = co_nvg = 0

    for flight in lst_flight_log:
        sic = sic + flight.flight_time
        pic = pic + flight.flight_time
        day = day + flight.day
        night = night + flight.night
        if flight.pilot_nvg:
            nvg = nvg + flight.pilot_nvg
        if flight.co_pilot_nvg:
            co_nvg = co_nvg + flight.co_pilot_nvg
        if flight.partial_nfr != "":
            vfr = vfr + flight.flight_time + flight.partial_nfr
            ifr = ifr + 2*flight.flight_time - flight.partial_nfr
        else:
            vfr = vfr + flight.flight_time
            ifr = ifr + 2*flight.flight_time
    
    pilot = LogEmployee()
    pilot.pic = pic
    pilot.day = day
    pilot.night = night
    pilot.nvg = nvg
    pilot.vfr = vfr
    pilot.ifr = ifr
    try:
        log_temp = Log.objects.filter(id_log=id_log)
        if log_temp:
            pilot.log = log_temp[0]
    except:
        pass
    emp_temp = Employee.objects.filter(employee_number = request.session[constant.usernameParam])
    if emp_temp:
        pilot.employee = emp_temp[0]
    list.append(todict(pilot))

    if co_pilot != "Choose One" and request.session[constant.usernameParam] != co_pilot:
        co_pilot_object = LogEmployee()
        co_pilot_object.sic = sic
        co_pilot_object.day = day
        co_pilot_object.night = night
        co_pilot_object.nvg = co_nvg
        co_pilot_object.vfr = vfr
        co_pilot_object.ifr = ifr
        try:
            log_temp = Log.objects.filter(id_log=id_log)
            if log_temp:
                co_pilot_object.log = log_temp[0]
        except:
            pass
        emp_temp = Employee.objects.filter(employee_number = co_pilot)
        if emp_temp:
            co_pilot_object.employee = emp_temp[0]
        list.append(todict(co_pilot_object))
    
    '''Remove older table'''
    dajax.remove("#table_pilot")
    dajax.remove("#pi_content")
    
    '''Init data for formset'''
    formset_pilot = PilotFormSet(initial = list, prefix='pilots')
    
    '''Render form'''
    render = render_to_string(constant.pilot_section ,{"formset_pilot":formset_pilot})
    render1 = render_to_string(constant.pilot_form ,{"formset_pilot":formset_pilot})
    
    '''Append form'''
    dajax.script(constant.append_pilot_section %render.replace('\n', ""))
    dajax.script(constant.append_pilot_form %render1.replace('\n', ""))
    
    
@dajaxice_register(method=constant.GET)
def ajax_check_lognumber(request, log_number):
    log = Log.objects.filter(log_number = log_number)
    if log:
        log_number = int(log_number) + 1
     
    return simplejson.dumps({'log_number':log_number})   
 

