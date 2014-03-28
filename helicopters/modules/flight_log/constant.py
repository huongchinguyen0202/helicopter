mess_account_does_not_exist = u"Employee Number is incorrrect."
#mess_account_does_not_exist = u"Account does not exist"
#mess_account_does_not_exist = u"Account does not exist"
username = "username"
password = "password"
remember = "remember"
mess_wrong_password = u"Password is incorrect."
POST = 'POST'
GET = 'GET'

employee_number = "employee_number"
usernameParam = "usname"
expire = "expire"
emailSender = "vietcombank.py@gmail.com"

list_contract = "list_contract"
limit = "limit"
json = 'json'

list_flight_log = "list_flight_log"
list_fuel_cal = "list_fuel_cal"
forms = "forms"
formset = "formset"
location = "location"
gallon = "gallon"
owner = "owner"
amount = "amount"
list = "list"
single_form = "single_form"
is_submitted = "is_submitted"
form = "form"

class_error_mess = '.error_message'
class_pop_main = '.popup_main'
id_rs_fuel_expenses_or_usage_form = "#rs_fuel_expenses_or_usage_form"
id_rs_flight_log_form = "#rs_flight_log_form"

prevent_default = "$('#window').preventDefault();"

msg_out_of_passenger = "Flight legs have FTL#: %s have passenger number is out of range."
prepend_table_popup = "$('#table_popup').prepend('%s');" 
prepend_fuel_cal = "$('#div_fuel_cal').prepend('%s');"
prepend_flight_log_table = "$('#div_flight_log_table').prepend('%s');"
append_flight_log_form = "$('#rs_flight_log_form').append('%s');"
append_flight_email_popup = "$('#form_email_popup').append('%s');"
append_error_mess = "$('#div_error_passenger').html('%s');"
append_save_succ_mess = "$('#div_succ_passenger').html('%s');"
remove_save_succ_mess = "$('#div_succ_passenger').html('');"
add_succ_mess = "Flight Leg is added successfully"
edited_succ_mess = "Flight Leg is edited successfully"
mess_delete_suc = "The selected flight log(s) is deleted successfully"
mess_submit_suc = "The selected flight log(s) is submitted successfully"
append_pilot_section = "$('#form_pilot').append('%s');"
append_pilot_form = "$('#pi').append('%s');"

"""
    Html pages
"""
flight_log_table_page = "flights/flight_log_table.html"
fuel_cal_page = "flights/fuel_cal.html"
popup_page = "flights/popup.html"
email_popup_page = "flights/email_popup.html"
home_page = "home.html"
email_succ_page = "flights/email_succseful.html"
signin = "accounts/login.html"
home_submitted = "flights/home_sumitted.html"
pilot_section = "flights/pilot_section.html"
pilot_form = "flights/pilot_form.html"

#edit_delete
flight_log_id = "id"
delete = 'delete'
submit = 'submit'
row_check = "row_check_"

#url
home_url = "/"
search_url = "/search/"
login = '/login/'



#search _ pagination
user_id = "user_id"
is_submited = "is_submited"
log_num = "log_num"
log_number = "log_number"
customer = "customer"
contract1charter__customer__cus_name__ilike = "customer__cus_name__ilike"
model = "model"
a1c__model__mo_name__ilike = "a1c__model__mo_name__ilike"
date = "date"
format_mdy = "%m/%d/%Y"
format_ymd = "%Y-%m-%d"
log_date = "log_date"
a1c__a1c_name__ilike = "a1c__a1c_name__ilike"
list_json = "list"
page_current = "page_current"
status = "status"
mo_name = "mo_name"
a1c_name = "a1c_name"
contract = "contract"
cus = "cus"
id_log = "id"
ac = "ac"

#Utility
POST = "POST"
email_to = "email_to"
email_cc = "email_cc"
email_bcc = "email_bcc"
email_subject = "email_subject"
email_content = "email_content"
email_from = "email_from"
hiden_attack = "hiden_attack"
HTTP_REFERER = "HTTP_REFERER"
html = "html"
email_sent = "The email is sent successfully"

#home
page = 'page'
empty_flight_log = "empty_flight_log"
announce_mess = "announce_mess"
announce_mess_fuel_location_change = "This Fuel Station is being used in Fuel Expenses or Usage section. Please delete that record to continue."
IS_EDIT = "is_edit"
number_page = 10

message_check = "message %s"