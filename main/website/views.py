from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from users.models import CustomUser


def index(request):
    return render(request, "website/index.html")

def about(request):
    return render(request, "website/about.html")

def contact(request):
    return render(request, "website/contact.html")

def resources(request):
    return render(request, "website/resources.html")

def basics(request):
    return render(request, "website/basic-topics.html")

def advanced(request):
    return render(request, "website/advanced-topics.html")

def linkeddata(request):
    return render(request, "website/linked-data.html")

def semantic(request):
    return render(request, "website/url-semantic-web.html")



#send user to login form
def login_form(request):
    context = {
            "state": "login",
            "error": ""
        }
    return render(request, "website/account.html", context)


#log user in
def login_view(request):
    username = request.POST["inputUsername"]
    password = request.POST["inputPassword"]

    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        #return render(request, "website/index.html")
        return HttpResponseRedirect(reverse("mainindex"))

    else:
        context = {
            "state": "login",
            "error": "Invalid credentials, try again."
            }
        return render(request, "website/account.html", context)


#log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("mainindex"))


def account(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "website/index.html", context)
        #return render(request, "website/home.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    context = {
        "state": "loggedin",
        "error"  : "",
        "update" : ""
        }

    if request.method == 'POST':

        pwform = PasswordChangeForm(request.user, request.POST)

        if pwform.is_valid():
            print("form IS valid")
            user = pwform.save()
            update_session_auth_hash(request, user)  # Important!
            #messages.success(request, 'Your password was successfully updated!')
            #return redirect('main')
            context["update"] = "Password updated successfully!"
            #return HttpResponseRedirect(reverse("mainindex"))
        else:
            print("form not valid")
            context["error"] = "Problem changing password."
            #return HttpResponseRedirect(reverse("mainindex"))
            #messages.error(request, 'Please correct the error below.')


    context["user"] = username

    #devform = DevkeyForm(initial={"inputDevKey": username.devkey})
    #bibform = BibgroupForm(initial={"inputBibgroup": username})
    pwform = PasswordChangeForm(request.user)

    #context["devform"] = devform
    #context["bibform"] = bibform
    context["pwform"] = pwform

    return render(request, "website/account.html", context)


#send user to registration page
def register(request):
    context = {
        "state": "register",
        "error" : ""
        }
    return render(request, "website/account.html", context)


#register new user
def registering(request):
    try:
        username = request.POST["inputUsername"]
        firstname = request.POST["inputFirst"]
        lastname = request.POST["inputLast"]
        email = request.POST["inputEmail"]
        password = request.POST["inputPassword"]

    except ValueError:

        context = {
            "state": "register",
            "error" : "Please fill out this form entierly."
            }
        
        return render(request, "website/account.html", context)

    user = CustomUser.objects.create_user(username,email,password)
    user.save

    user1 = CustomUser.objects.get(username=username)
    user1.first_name = firstname
    user1.last_name = lastname
    user1.save()

    return HttpResponseRedirect(reverse("mainindex"))



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