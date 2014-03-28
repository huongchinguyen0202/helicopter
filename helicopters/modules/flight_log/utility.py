from flight_log.models import Log
from random import randint
from django.core.mail import BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import constant
import os
from django.contrib import messages
from django_xhtml2pdf.utils import render_to_pdf_response, fetch_resources
import ho.pisa as pisa
from datetime import datetime
def format6(org_log_number):
    #print "org_log_number type", type(org_log_number)
    #org_log_number = long(org_log_number) #"%05d" % i
    leading_zero =  str(org_log_number).zfill(6);
    return "Daily_Flight_Log_" + leading_zero + ".pdf"
# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    pisa.showLogging()
    #print "open output file for writing (truncated binary)", datetime.now().strftime('%H:%M:%S')
    resultFile = open(outputFilename, "w+b")
    #print " convert HTML to PDF", datetime.now().strftime('%H:%M:%S')
    pisaStatus = pisa.CreatePDF(
            sourceHtml.encode("UTF-8"),                # the HTML to convert
            dest=resultFile, encoding='UTF-8',
                   link_callback=fetch_resources)           # file handle to recieve result
    #print " close output file", datetime.now().strftime('%H:%M:%S')
    resultFile.close()                 # close output file
    # return True on success and False on errors
    return pisaStatus.err


def random_with_N_digits(n):
    
    range_start = 10**(n-1)
    range_end = (10**n)-1

    return randint(range_start, range_end)


def generate_log_number():
   
    random = random_with_N_digits(6)
    log_num = str(random)
    log = Log.objects.filter(log_number=log_num)
    
    while log:
        random = random_with_N_digits(11)
        log = Log.objects.filter(log_number=log_num)
        
    return log_num


def send_email(request):
    
    if request.method == constant.POST:
        email_from = constant.emailSender
        #email_from = request.POST.get(constant.email_from)
        email_to = request.POST.get(constant.email_to)
        email_cc = request.POST.get(constant.email_cc)
        email_bcc = request.POST.get(constant.email_bcc)
        email_subject = request.POST.get(constant.email_subject)
        email_content = request.POST.get(constant.email_content)
        #email_file = request.FILES['email_attachment']
        
        if not email_from or not email_to:
            pass
        else:
            try:
                validate_email(email_from)
            except ValidationError:
                return HttpResponseRedirect(request.META.get(constant.HTTP_REFERER))
            else:
                try:
                    to = append_cc_bcc(email_to)
                except ValidationError:
                    return HttpResponseRedirect(request.META.get(constant.HTTP_REFERER))
                else:
                    pass
                
            mcc = append_cc_bcc(email_cc)
                        
            mbcc = append_cc_bcc(email_bcc)
            
            try:
                msg = EmailMultiAlternatives(email_subject, email_content, email_from, to, cc=mcc, bcc=mbcc)
                msg.content_subtype = constant.html
                files = request.POST.get(constant.hiden_attack)
                if not ".zip" in files and not ".pdf" in files:
                    files = files + ".pdf"
                dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) +'/../helicopters/static/media/pdf_export/'
                pdf_path = dirname + files
                if os.path.isfile(pdf_path):
                    msg.attach_file(pdf_path)
                try:
                    msg.send()
                except:
                    pass
                messages.success(request, constant.email_sent)
            except BadHeaderError:
                return HttpResponseRedirect(request.META.get(constant.HTTP_REFERER))
            
    return HttpResponseRedirect(request.META.get(constant.HTTP_REFERER))


def append_cc_bcc(email):

    mcc_bcc = []
    
    if not email :
        pass
    else:
        email = email.replace(';' , ',')
        email = email.replace(' ' , '')
        lst_email = email.split(',')
        for em_cc_bcc in lst_email:
            if em_cc_bcc != "":
                try:
                    validate_email(em_cc_bcc)
                except ValidationError:
                    pass
                else:
                    mcc_bcc.append(em_cc_bcc)
                
    return mcc_bcc


def email_succseful(request):
    
    return render(request, constant.email_succ_page)
