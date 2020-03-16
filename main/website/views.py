from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    #return HttpResponse("Hello, world. You're at the main website index.")
    return render(request, "website/index.html")

def about(request):
    return render(request, "website/about.html")

def contact(request):
    return render(request, "website/contact.html")

# # contact form
# def contact(request):

# # email sent from contact form
# def send_email(request):
#     name = request.POST["name"]
#     email = request.POST["email"]
#     subject = request.POST["subject"]
#     message = request.POST["message"]

#     msg = MIMEText(msg)

#     msg['Subject'] = subject
#     msg['From'] = me
#     msg['To'] = you

#     #Test Info
#     #s = smtplib.SMTP('127.0.0.1:1025')
    
#     #Live Info
#     s = smtplib.SMTP()
#     s.connect(host,port)
#     s.login(username,password)
    
#     #Test & Live
#     s.sendmail(me, [you], msg.as_string())
#     s.quit()

#     #return 'Email sent'

#     # if success, send confirmation to user

#     # if fail, send error

    
#         return render(request, "bibtool/index.html", context)