# from ..accounts.models import Account
# from django_tenants_portal.portal.models.admin_models import Address, CompanyDetails
# from django_tenants_portal.portal.decorators import unauthenticated_user

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
# from ..portal.forms import CreateUserForm

from django_multitenancy.users.models import TenantUser
# from .EmailBackEnd import EmailBackEnd
from django.core.checks import messages
from django.contrib import messages
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
#from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage

def showDemoPage(request):
    return render(request, 'demo.html')

@unauthenticated_user
def ShowLoginPage(request):
    company_address = Address.objects.get_or_create(id=1)
    #organization = GroupType.objects.create(label='Organization')
    company_details = CompanyDetails.objects.get_or_create(id=1)
    return render(request, 'registration/login_page.html', {"company_details": company_details, "company_address": company_address})

@unauthenticated_user
def RegistrationPage(request):
    form = CreateUserForm()
    if request.method  == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.user_type = 3
            OPEN = 'OPEN'
            #user.status = OPEN        
            user.save()
                        
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            #user.email_user(subject, message)
            #return redirect('activation_sent')
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})

def activation_sent_view(request):
    return render(request, 'registration/activation_sent.html')


def activate(request, uidb64, token, backend='tenant_users.permissions.backend.UserBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = TenantUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, TenantUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.signup_confirmation = True
        user.is_varified = True
        user.save()
        login(request, user, backend='tenant_users.permissions.backend.UserBackend')
        return redirect('customer_dashboard')
    else:
        return render(request, 'registration/activation_invalid.html')

    
def SaveRegistration(request):
 
    if request.method  == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.usertype = 3
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})

def doLogin(request):
    if request.method != "POST":
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))
        if user != None:
            login(request, user, backend='tenant_users.permissions.backend.UserBackend')
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_dashboard"))
            else:
                return HttpResponseRedirect(reverse("customer_dashboard"))
            # return HttpResponse("Email : "+request.POST.get("email")+" Password : "+request.POST.get("password"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+" usertype : "+request.user.usertype)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


#def password_reset_request(request):
#	if request.method == "POST":
#		password_reset_form = PasswordResetForm(request.POST)
#		if password_reset_form.is_valid():
#			data = password_reset_form.cleaned_data['email']
#			associated_users = User.objects.filter(Q(email=data))
#			if associated_users.exists():
#				for user in associated_users:
#					subject = "Password Reset Requested"
#					email_template_name = "main/password/password_reset_email.txt"
#					c = {
#					"email":user.email,
#					'domain':'127.0.0.1:8000',
#					'site_name': 'Website',
#					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
#					"user": user,
#					'token': default_token_generator.make_token(user),
#					'protocol': 'http',
#					}
#					email = render_to_string(email_template_name, c)
#					try:
#						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
#					except BadHeaderError:
#						return HttpResponse('Invalid header found.')
#					return redirect ("/password_reset/done/")
#	password_reset_form = PasswordResetForm()
#	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})