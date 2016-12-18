from django.conf import settings
from io import BytesIO, StringIO
import StringIO
import cgi
import os
from django.db import connection
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import Context
from django.views import generic
from django import forms
from reportlab.pdfgen import canvas
from django.db.models import Avg, Min, Max, Sum, Count
from xhtml2pdf import pisa
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf_response
from .models import EoooData, EoooParent, EoooStudent, EoooDistributedto, EoooFapackage, EoooEmployee, EoooDepartment, EoooBudget
from .forms import NameForm, DistributePackageForm, AddStudentForm

#MAY NOT NEED RESULTS VIEW......
# Create your views here.
class HelloPDFView(PDFTemplateView):
    template_name = "report_file.html"
    def get_context_data(self, **kwargs):
        return super(HelloPDFView, self).get_context_data(pagesize="A4",title="Hi There!",**kwargs)

class IndexView(generic.ListView):
    template_name = 'cadb/list_of_employees.html'
    context_object_name = 'latest_employee_list'
    def get_queryset(self):
        return EoooEmployee.objects.order_by('employee_id')[:5]

class ReportView(generic.ListView):#THIS LINK IS ACTUALLY "HISTORY"
    template_name = 'cadb/report.html'
    context_object_name = 'report_list'
    def get_queryset(self):
        return EoooFapackage.objects.order_by('packageid')[:]

def DistributionList(request):
    distribution_list = EoooDistributedto.objects.order_by('-ddate')[:10]
    return render(request, 'cadb/distribution_list.html',{'distribution_list':distribution_list})

def DistributeView(request):
    if request.method == 'POST':
        distribute = DistributePackageForm(request.POST)
        print("CHECKING IF FORM IS VALID")
        if distribute.is_valid():
            studentid = request.POST.get('studentid')
            distribute.save(commit=True)
            #print(studentid)
            ##consider making a financial aid package
            #object to have the same id number as the studentid
            return HttpResponseRedirect('distribution_list')
        else:
            print distribute.errors
            return HttpResponseRedirect('distribute.html')
    else:
        form_class = DistributePackageForm()
        return render(request, 'cadb/distribute.html', {'form':form_class,})

def DistributionReceipt(request, studentid):
    distribution = EoooDistributedto.objects.get(studentid=studentid)
    #try:
    #student = EoooStudent.objects.get(student_id=d_student_id)
    #end try
    return render(request, 'cadb/distribution_receipt.html', {'distribution':distribution})

def generate_history(request):
    print("def: Generate History")
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']
    dates = dict()
    dates['from'] = date_from
    dates['to'] = date_to
    print(date_from)
    print(date_to)
    try:
        distribution = EoooDistributedto.objects.filter(ddate__gt=date_from, ddate__lt=date_to)
    except EoooDistributedto.DoesNotExist:
        return HttpResponse('No distributions')
    return render(request, 'cadb/distribution_history.html', {'dates':dates, 'distribution':distribution})

def remainingBudgetReport(request):

    print("def: remainingBudgetReport")
    budget_year = request.GET['budget_date']
    years = dict()
    years['budget'] = budget_year
    print(budget_year)
    try:
        #first get budget
        budget = EoooBudget.objects.get(budate=budget_year)
        print(budget.amount)
        distribution = EoooDistributedto.objects.filter(ddate__gt=budget_year).order_by('fapackageid__ptype')#was order_by('-ddate')
        package = EoooFapackage.objects.filter(fabudgetid=budget.pk)
        largest_package = package.all().aggregate(Max('amount'))
        print(largest_package)
        average_package = package.all().aggregate(Avg('amount'))
        print(average_package)
        #GROUP BY
        package_types = package.values('ptype').annotate(Count('packageid')).order_by()
        #package_types = distribution.values('fapackageid__ptype').annotate(Count('fapackageid')).order_by()
        print(package_types)
    except EoooBudget.DoesNotExist:
        return HttpResponse('No budget exists')

    return render(request, 'cadb/budget_report.html', {'largest_package':largest_package, 'average_package':average_package, 'package_types':package_types,'budget':budget, 'distribution':distribution})

def NewDistribution(request):
    print("def: New Distribution Fn")
    print("getting current budget")
    budget = EoooBudget.objects.get(pk=40)#2016 budget
    print("budget's primary key is", budget.pk)
    print("current budget is",budget.amount)
    print("budget year is", budget.budate)
    if request.method=='POST':
        student_ssn = request.POST.get('student_ssn')
        print(student_ssn)
        f_name = request.POST.get('f_name', 'john')
        print(f_name)
        l_name = request.POST.get('l_name','doe')
        print(l_name)
        student_city = request.POST.get('student_city')
        print(student_city)
        student_state = request.POST.get('student_state')
        print(student_state)
        aid_amount = float(request.POST.get('aid_amount',500.00))
        print(aid_amount)
        aid_type = request.POST.get('aid_type')
        print(aid_type)
        distribution_date = request.POST.get('distribution_date')
        print(distribution_date)
        try:
            #STUDENT UPDATING
            student_insert = EoooStudent.objects.create(ssn=student_ssn,fname=f_name, lname=l_name, city=student_city, state=student_state)
            student_insert.refresh_from_db()
            student_primaryKey = student_insert.student_id
            print("Student primary key is: ",student_primaryKey)
            #PACKAGE UPDATING
            package_insert = EoooFapackage.objects.create(ptype=aid_type, amount=aid_amount, fabudgetid=budget)
            package_insert.refresh_from_db()
            package_primaryKey = package_insert.packageid #for this to work had to use AUTOFIELD in MODEL for PK
            print("Financial aid package primary key is",package_primaryKey)
            #BUDGET UPDATING
            budget = EoooBudget.objects.get(pk=40)#2016 budget
            budget.amount -= aid_amount
            budget.save()
            #DISTRIBUTION UPDATING
            distribution_insert = EoooDistributedto.objects.create(studentid=student_insert, fapackageid=package_insert,ddate=distribution_date)
            distribution_insert.refresh_from_db()
            print("distribution made with:", distribution_insert.studentid, distribution_insert.fapackageid)
        except EoooStudent.DoesNotExist:
            return HttpResponse('No Students')
        return render(request, 'cadb/new_distribute_package.html', {'budget':budget})
    else:
        print('GET')
        return render(request, 'cadb/new_distribute_package.html', {'budget':budget})

def pdf_distribution_receipt(request, studentid):
    distribution = EoooDistributedto.objects.get(studentid=studentid)
    return render_to_pdf('cadb/pdf_distribution_receipt.html', {'distribution':distribution})

def AddStudentView(request):
    if request.method == 'POST':
        student_form = AddStudentForm(request.POST)
        print("CHECKING IF FORM IS VALID")
        if student_form.is_valid():
            student_form.save(commit=True)
            return HttpResponseRedirect('.')
        else:
             print student_form.errors
             return HttpResponseRedirect('.')
    else:
        form = AddStudentForm()
        return render(request, 'cadb/student.html',{'form':form,})

def PdfSummary(request):
    distributions = EoooDistributedto.objects.get(studentid=19)
    return render_to_pdf('cadb/file_report.html', {'distributions':distributions})

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='')
    return HttpResponse('We had errors<pre>%s</pre>' % escape(html))

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL,''))
    return path
#list of latest distributed packages before
class DistributeList(generic.ListView):
    template_name = 'cadb/distribute.html'
    context_object_name = 'latest_distro_list'
    def get_queryset(self):
        #returns all distribution package
        return EoooDistributedto.objects.order_by('-studentid')[:]

#get_name for form
def get_name(request):
        #if this is a POST request we need to proces the form data
        if request.method == 'POST':
            #create a form instance and populate it with the data from request:
            form = NameForm(request.POST)
            #check whether it's valid:
            if form.is_valid():
                #process the data in form.cleaned_data as required
                #...
                #redirect to a new URL:
                return HttpResponseRedirect('/thanks/')
        #if a GET (or any other method) we'll create a blank form
            else:
                form = NameForm()
            return render(request, 'name.html',{'form':form})
