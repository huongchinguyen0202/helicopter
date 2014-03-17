#Manage draft flight log
from models import Log
from flight_log import constant
from django.shortcuts import redirect

"""
    Process data from draft when choose to delete or edit
"""
def edit_delete(request):
    print "vao"
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
                        announce_message = "The selected flight log(s) is deleted successfully"
                    else:
                        flight_log.is_submited = True
                        flight_log.save()
                        announce_message = "The selected flight log(s) is submitted successfully"
            except:
                pass
    return redirect(constant.home_url, announce_mess = announce_message)
