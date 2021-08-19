from django_tenants_portal.core.models.admin_models import Address, CompanyDetails
from django_tenants_portal.core.decorators import unauthenticated_user
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from .EmailBackEnd import EmailBackEnd
from django.core.checks import messages
from django.contrib import messages
# Create your views here.
from groups_manager.models import Group, GroupType, Member

def showDemoPage(request):
    return render(request, 'demo.html')

@unauthenticated_user
def ShowLoginPage(request):
    company_address = Address.objects.get_or_create(id=1)
    #organization = GroupType.objects.create(label='Organization')
    company_details = CompanyDetails.objects.get_or_create(id=1)
    return render(request, 'login_page.html', {"company_details": company_details, "company_address": company_address})


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