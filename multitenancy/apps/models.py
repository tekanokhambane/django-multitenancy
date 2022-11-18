from django.conf import settings
from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase
from django_tenants.utils import get_tenant_type_choices
from multitenancy.subscriptions.models import Subscription

# from ..billing.models import Charge

DEFAULT_TYPE = "personal"


class Package(models.Model):
    name = models.CharField(max_length=100, default=DEFAULT_TYPE, choices=get_tenant_type_choices())
    price = models.DecimalField(default=75,  # type: ignore
                                max_digits=12, verbose_name="Price", decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def annual_price(self):
        price = self.price * 12
        return price


class TenantType(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, default=DEFAULT_TYPE, choices=get_tenant_type_choices())

    def __str__(self) -> str:
        return self.name


class Tenant(TenantBase):
    id = models.AutoField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=200, default=DEFAULT_TYPE, choices=get_tenant_type_choices())
    name = models.CharField(max_length=100)
    is_template = models.BooleanField(default=True)
    plan = models.ForeignKey(Package, null=True, on_delete=models.PROTECT)
    subscription = models.OneToOneField(Subscription, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    # paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['id', 'name']


class DomainTld(models.Model):
    TLD = (
        ('.co.za', '.co.za'),
        ('.com', '.com'),
        ('.org', '.org'),
        ('.org.za', '.org.za'),
        ('.net', '.net'),
        ('.africa', '.africa'),
        ('.web.za', '.web.za'),
        ('.net.za', '.net.za'),
        ('.joburg', '.joburg'),
        ('.capetown', '.capetown'),
        ('.durban', '.durban'),
        ('.za.com', '.za.com'),
        ('.sa.com', '.sa.com'),
        ('.mobi', '.mobi'),
        ('.info', '.info'),
        ('.biz', '.biz'),
        ('.name', '.name'),
        ('.co', '.co'),
        ('.cc', '.cc'),
        ('.co.uk', '.co.uk'),
        ('.org.uk', '.org.uk'),
        ('.gr', '.gr'),
        ('.me', '.me'),
        ('.mx', '.mx'),
        ('.us', '.us'),
        ('.tv', '.tv'),
        ('.vc', '.vc'),
        ('.ws', '.ws'),
        ('.academy', '.academy'),
        ('.agency', '.agency'),
        ('.art', '.art'),
        ('.bargains', '.bargains'),
        ('.bike', '.bike'),
        ('.build', '.build'),
        ('.builders', '.builders'),
        ('.camera', '.camera'),
        ('.camp', '.camp'),
        ('.careers', '.careers'),
        ('.center', '.center'),
        ('.city', '.city'),
        ('.clothing', '.clothing'),
        ('.cloud', '.cloud'),
        ('.club', '.club'),
        ('.codes', '.codes'),
        ('.coffee', '.coffee'),
        ('.company', '.company'),
        ('.computer', '.computer'),
        ('.construction', '.construction'),
        ('.consulting', '.consulting'),
        ('.contractors', '.contractors'),
        ('.diamonds', '.diamonds'),
        ('.directory', '.directory'),
        ('.design', '.design'),
        ('.domains', '.domains'),
        ('.education', '.education'),
        ('.email', '.email'),
        ('.energy', '.energy'),
        ('.engineering', '.engineering'),
        ('.enterprises', '.enterprises'),
        ('.enterprises', '.enterprises'),
        ('.equipment', '.equipment'),
        ('.estate', '.estate'),
        ('.farm', '.farm'),
        ('.florist', '.florist'),
        ('.fund', '.fund'),
        ('.gallery', '.gallery'),
        ('.glass', '.glass'),
        ('.global', '.global'),
        ('.graphics', '.graphics'),
        ('.green', '.green'),
        ('.guru', '.guru'),
        ('.healthcare', '.healthcare'),
        ('.holiday', '.holiday'),
        ('.one', '.one'),
        ('.online', '.online'),
        ('.marketing', '.marketing'),
        ('.ninja', '.ninja'),
        ('.rocks', '.rocks'),
        ('.run', '.run'),
        ('.services', '.services'),
        ('.solutions', '.solutions'),
        ('.space', '.space'),
        ('.store', '.store'),
        ('.tips', '.tips'),
        ('.tech', '.tech'),
        ('.trade', '.trade'),
        ('.university', '.university'),
    )
    name = models.CharField(max_length=30, blank=False, null=True, choices=TLD)  # type: ignore
    price = models.DecimalField(decimal_places=2, max_digits=5)
    transfer_price = models.DecimalField(default=50, decimal_places=2, max_digits=5)  # type: ignore
    # transfered = models.BooleanField(default=False)
    period = models.IntegerField(default=1)

    def __str__(self):
        # return self.name
        return "{} Year/s {} domain @ R{}".format(self.period, self.name, self.price)

    class Meta:
        unique_together = ['name', 'price']


class RegisteredDomain(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    tld = models.ForeignKey(DomainTld, null=True, on_delete=models.CASCADE)
    sld = models.CharField(max_length=250, null=True)

    # created = models.DateField(auto_now_add=True, null=True)

    # nameserver1 = models.CharField(max_length=150, null=True)
    # nameserver2 = models.CharField(max_length=150, null=True)
    # nameserver3 = models.CharField(max_length=150, null=True)
    # nameserver4 = models.CharField(max_length=150, null=True)
    # dnsmanagement = models.IntegerField(default=1)
    # emailforwarding = models.IntegerField(default=1)
    # idprotection = models.IntegerField(default=1)
    # firstname = models.CharField(max_length=250, null=True)
    # lastname = models.CharField(max_length=250, null=True)
    # companyname = models.CharField(max_length=250, null=True)
    # address1 = models.CharField(max_length=250, null=True)
    # address2 = models.CharField(max_length=250, null=True)
    # city = models.CharField(max_length=250, null=True)
    # state = models.CharField(max_length=250, null=True)
    # country = models.CharField(max_length=250, null=True)
    # postcode = models.CharField(max_length=150, null=True)
    # phonenumber = PhoneNumberField(null=True)
    # email = models.EmailField()
    # adminfirstname = models.CharField(max_length=250, null=True)
    # adminlastname = models.CharField(max_length=250, null=True)
    # admincompanyname = models.CharField(max_length=250, null=True)
    # adminaddress1 = models.CharField(max_length=250, null=True)
    # adminaddress2 = models.CharField(max_length=250, null=True)
    # admincity = models.CharField(max_length=250, null=True)
    # adminstate = models.CharField(max_length=250, null=True)
    # admincountry = models.CharField(max_length=250, null=True)
    # adminpostcode = models.CharField(max_length=250, null=True)
    # adminphonenumber = PhoneNumberField(null=True)
    # adminemail = models.EmailField(null=True)

    def __str__(self) -> str:
        return '{}{}'.format(self.sld, self.tld)


class Domain(DomainMixin):
    dns = models.OneToOneField(RegisteredDomain, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.domain
