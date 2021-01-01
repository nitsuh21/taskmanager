from django.shortcuts import render,redirect
from home.models import Task,User
import datetime
from django.contrib import messages
from django.contrib.auth.models import auth
# Create your views here.

def wellcome(request):
	return render(request,'wellcome.html')

def createofficer(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			print(request.user)
			print("superuser")
			if request.method == 'POST':
				username = request.POST['username']
				email = request.POST['email']
				position = request.POST['position']
				password1 = request.POST['password1']
				password2 = request.POST['password2']
				if password1==password2:
					if User.objects.filter(username=username).exists():
						messages.info(request,'Username name taken')
						return redirect('createofficer')
					elif User.objects.filter(email=email).exists():
						messages.info(request,'Email has taken')
						return redirect('createofficer')				
					else:
						user = User.objects.create_user(username=username,password=password1,email=email,position=position)
						user.save()
						user = User.objects.get(email=email)
						return redirect('home')	        
				else:
					messages.info(request,'passwords not matching')
					return redirect('createofficer')
			else:
				return render(request,'createofficer.html')
		else:
			print("not superuser")
			return redirect('home')
	else:
		print("not authenticated")
		return redirect('home')

def login(request):
	if request.method == 'POST':
		email=request.POST['email']
		password=request.POST['password']
		user=auth.authenticate(request,email=email,password=password)
		if user is not None:
			print("not none")
			auth.login(request,user)
			return redirect('home')
		else:
			print("null")
			messages.info(request,'invalid credential')
			return redirect('login')
	else:
		if request.user.is_authenticated:
			return render(request,'home.html')
		else:
			return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def home(request):
	if request.user.is_authenticated:
		user = User.objects.filter(id=request.user.id)
		tasks = Task.objects.filter(user=request.user).order_by('-id').exclude(remark="extended")
		if request.user.is_superuser:
			tasks = Task.objects.all().order_by('-id').exclude(remark="extended")
		now = datetime.datetime.now()
		print("Date: "+ now.strftime("%Y-%m-%d"))
		today = now.date()
		print(today)
		print(tasks)
		for task in tasks:
			print(task.extend_remindat)
			print(today)
			difference = (task.extend_remindat - today)
			print(difference)
			if task.extend_remindat <= today:
				task.remark = "warning"
				task.save()
			if task.last_remindat <= today:
				task.remark = "danger"
				task.save()
			if task.expiry_date <= today:
				task.remark = "expired"
				task.save()
				
			print(task.title)
		context ={
		   'tasks':tasks
		}
		return render(request,'home.html',context)
	else:
		return redirect('login')

def incompletedtasks(request):
	if request.user.is_authenticated:
		tasks = Task.objects.all().order_by('-id')
		ongoingtasks = Task.objects.filter(user=request.user,remark = "safe").order_by('-id')
		warningtasks = Task.objects.filter(user=request.user,remark = "warning").order_by('-id')
		dangertasks = Task.objects.filter(user=request.user,remark = "danger").order_by('-id')
		context ={
		'warningtasks':warningtasks,
		'ongoingtasks':ongoingtasks,
		'dangertasks':dangertasks
		}
		return render(request,'incompletedtasks.html',context)
	else:
		return redirect('login')

def donetasks(request):
	if request.user.is_authenticated:
		user = User.objects.filter(id=request.user.id)
		donetasks = Task.objects.filter(user=request.user,remark = "expired").order_by('-id')
		extendedtasks = Task.objects.filter(user=request.user,remark = "extended").order_by('-id')
		context ={
		'donetasks':donetasks,
		'extendedtasks':extendedtasks,
		}
		return render(request,'donetasks.html',context)
	else:
		return redirect('login')
	

def delete(request,id):
	if request.user.is_authenticated:
		task = Task.objects.filter(id=id).delete()
		return redirect('home')
	else:
		return redirect('login')
	
def edit(request,id):
	if request.user.is_authenticated:
		if request.method == 'POST':
			title=request.POST['title']
			suppliersname=request.POST['suppliersname']
			cellphone=request.POST['cellphone']
			contractno=request.POST.get('contractno')
			typeofsecurity=request.POST['typeofsecurity']
			formofsecurity=request.POST['formofsecurity']
			issuingbank=request.POST['issuingbank']
			referenceno=request.POST['referenceno']
			issuingdate=request.POST['issuingdate']
			expirydate=request.POST['expirydate']
			informsupdate=request.POST['informsupdate']
			informbankdate=request.POST['informbankdate']
			amount=request.POST.get('amount')
			remark="safe"
			
			if expirydate <= issuingdate:
				messages.info(request,'The issuing date can not be after or on expiry date')
				print("wrong")
				return render(request,'guaranteedetail.html')
			elif expirydate <= informsupdate:
				messages.info(request,'The date of communication to suppliers can not be after or on expiry date')
				print("wrong")
				return render(request,'guaranteedetail.html')
			elif expirydate <= informbankdate:
				messages.info(request,'The date of communication to The bank can not be after or on expiry date')
				print("wrong")
				return render(request,'guaranteedetail.html')
			elif issuingdate >= informbankdate:
				messages.info(request,'The date of communication to The bank can not be before or on issuing date date')
				print("wrong")
				return render(request,'guaranteedetail.html')
			elif issuingdate >= informsupdate:
				messages.info(request,'The date of communication to The suppliers can not be before or on issuing date date')
				print("wrong")
				return render(request,'guaranteedetail.html')
			elif informbankdate <= informsupdate:
				messages.info(request,'The date of communication to The bank can not be before or on The date of communication to The suppliers')
				print("wrong")
				return render(request,'guaranteedetail.html')
			else:
				tasks = Task.objects.filter(contract_no=contractno)
				for task in tasks:
					task.remark="extended"
					print(task)
					print("extendedtask")
					task.save()
				task= Task(title=title, supplier_name=suppliersname, cell_phone=cellphone, contract_no=contractno, types_of_security=typeofsecurity,
				form_of_Security=formofsecurity, issuing_date=issuingdate,issuing_bank=issuingbank, extend_remindat=informsupdate, last_remindat=informbankdate,
				expiry_date=expirydate, amount=amount, remark=remark, Reference_no = referenceno)
				task.save()
				print(task.issuing_date)
				print(task.expiry_date)
				task.user.add(request.user)
				return redirect('/home')
		else:
			task = Task.objects.get(id=id)
			print(task.user)
			now = datetime.datetime.now()
			print(now)
			today = now.date()
			daysleft = task.expiry_date - today
			context ={
			   'task':task,
			   'daysleft':daysleft,
			   'today':today
			}
			return render(request,'guaranteedetail.html',context)
	else:
		return redirect('login')
	
def profile(request,id):
	if request.user.is_authenticated:
		user = User.objects.get(id=id)
		print(user.username)
		context ={
		 'user':user
		}
		return render(request,'officerdetail.html',context)
	else:
		return redirect('login')

def printing(request):
	if request.user.is_authenticated:
		user = User.objects.filter(id=request.user.id)
		tasks = Task.objects.filter(user=request.user).order_by('-id')
		if request.user.is_superuser:
			tasks = Task.objects.all().order_by('-id')
		now = datetime.datetime.now()
		print("Date: "+ now.strftime("%Y-%m-%d"))
		today = now.date()
		print(today)
		print(tasks)
		for task in tasks:
			print(task.extend_remindat)
			print(today)
			difference = (task.extend_remindat - today)
			print(difference)
			if task.extend_remindat <= today:
				task.remark = "warning"
				task.save()
			if task.last_remindat <= today:
				task.remark = "danger"
				task.save()
			if task.expiry_date <= today:
				task.remark = "expired"
				task.save()
				
			print(task.title)
		context ={
		   'tasks':tasks
		}
		return render(request,'print.html',context)
	else:
		return redirect("login")

def search(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			key = request.POST.get('search')
			tasks = Task.objects.filter(supplier_name=key)
			print(tasks)
			context={
			'tasks' : tasks
			}
			return render(request,'search.html',context)
		else:
			return redirect('home')
	else:
		return redirect('login')

def addtask(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			title=request.POST['title']
			suppliersname=request.POST['suppliersname']
			cellphone=request.POST['cellphone']
			contractno=request.POST['contractno']
			typeofsecurity=request.POST['typeofsecurity']
			formofsecurity=request.POST['formofsecurity']
			issuingbank=request.POST['issuingbank']
			referenceno=request.POST['referenceno']
			issuingdate=request.POST['issuingdate']
			expirydate=request.POST['expirydate']
			informsupdate=request.POST['informsupdate']
			informbankdate=request.POST['informbankdate']
			amount=request.POST['amount']
			remark="safe"
			
			if expirydate <= issuingdate:
				messages.info(request,'The issuing date can not be after or on expiry date')
				print("wrong")
				return render(request,'addtask.html')
			elif expirydate <= informsupdate:
				messages.info(request,'The date of communication to suppliers can not be after or on expiry date')
				print("wrong")
				return render(request,'addtask.html')
			elif expirydate <= informbankdate:
				messages.info(request,'The date of communication to The bank can not be after or on expiry date')
				print("wrong")
				return render(request,'addtask.html')
			elif issuingdate >= informbankdate:
				messages.info(request,'The date of communication to The bank can not be before or on issuing date date')
				print("wrong")
				return render(request,'addtask.html')
			elif issuingdate >= informsupdate:
				messages.info(request,'The date of communication to The suppliers can not be before or on issuing date date')
				print("wrong")
				return render(request,'addtask.html')
			elif informbankdate <= informsupdate:
				messages.info(request,'The date of communication to The bank can not be before or on The date of communication to The suppliers')
				print("wrong")
				return render(request,'addtask.html')
			else:
				task= Task(title=title, supplier_name=suppliersname, cell_phone=cellphone, contract_no=contractno, types_of_security=typeofsecurity,
				form_of_Security=formofsecurity, issuing_bank=issuingbank, issuing_date=issuingdate, extend_remindat=informsupdate, last_remindat=informbankdate,
				expiry_date=expirydate, amount=amount, remark=remark)
				task.save()
				print(task.issuing_date)
				print(task.expiry_date)
				task.user.add(request.user)
				return redirect('/home')
		else:
			return render(request,'addtask.html')
	else:
		return redirect('login')



	