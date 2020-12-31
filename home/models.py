from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    position = models.CharField(max_length=500,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']

    def __str__(self):
        return "{}".format(self.email)

class Task(models.Model):
	title = models.CharField(max_length=10000,null=True)
	supplier_name = models.CharField(max_length=10000,null=True)
	cell_phone = models.CharField(max_length=10000,null=True)
	contract_no = models.CharField(max_length=10000,null=True)
	types_of_security = models.CharField(max_length=10000,null=True)
	form_of_Security = models.CharField(max_length=10000,null=True)
	issuing_bank = models.CharField(max_length=100000,null=True)
	Reference_no = models.CharField(max_length=10000,null=True)
	issuing_date = models.DateField(auto_now=False,auto_now_add=False)
	extend_remindat = models.DateField(auto_now=False,auto_now_add=False)
	last_remindat = models.DateField(auto_now=False,auto_now_add=False)
	expiry_date = models.DateField(auto_now=False,auto_now_add=False)
	amount = models.IntegerField(default=0)
	extended = models.IntegerField(default=0)
	daysleft = models.CharField(max_length=10000,null=True)
	remark = models.CharField(max_length=1000,null=True)
	user = models.ManyToManyField(User, blank=True,related_name='user_tasks')


	@classmethod
	def create():
		Task = cls(title = title)
		return Task
   
    
        
    
 