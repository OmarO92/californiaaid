from django.conf.urls import url
from django.http import HttpResponseRedirect, Http404
from .views import *
from . import views

app_name = 'cadb'
urlpatterns = [
#ex: /cadb/
	url(r'^$', views.DistributionList, name='index'),
	#url(r'^distribute', views.DistributeView, name='distribute'),
	url(r'^new_distribute_package', views.NewDistribution, name='distribute'),
	url(r'^student',views.AddStudentView, name='student'),
	url(r'^report',views.ReportView.as_view(),name='report'),#history link on menu
	url(r'^file_report',views.PdfSummary, name='file_report'),#report link on menu
	url(r'^distribution_receipt/(?P<studentid>[0-9]+)$',DistributionReceipt, name='distribution_receipt'),
	url(r'^distribution_list',views.DistributionList, name='distribution_list'),
	url(r'^history/',generate_history, name='history_distribution'),
	url(r'^budget_report/',remainingBudgetReport, name='budget_report'),
	url(r'^newdistribution',NewDistribution,name='newdistribution'),
	url(r'^pdf_distribution_receipt/(?P<studentid>[0-9]+)$',pdf_distribution_receipt, name='pdf_distribution_receipt'),
]
