from django.shortcuts import render
from django.views.generic import TemplateView,View
from BackTrack.models import *
from BackTrack.forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum
# Create your views here.

class LoginPage(TemplateView):
    template_name = "LoginPage.html"

class Signin(View):
    def post(self, request):
        if request.POST.get("username")=="" or request.POST.get("password")=="":
            messages.info(request,'Please fill in username and password.')
            return render(request,'LoginPage.html')
        else:
            if request.POST.get("position")=="Developer":
                dataset = Developer.objects.filter(username=request.POST.get("username"))
                if dataset[0].password==request.POST.get("password"):
                    request.session['id']=dataset[0].pk
                    request.session['position']=request.POST.get("position")
                    if dataset[0].project is None:
                        return HttpResponseRedirect('CreateProject')
                    else:
                        return HttpResponseRedirect('ProductBacklog')
                else:
                    messages.info(request,'Wrong username or password.')
                    return render(request,'LoginPage.html')
            else:
                dataset = Manager.objects.filter(username=request.POST.get("username"))
                if dataset[0].password==request.POST.get("password"):
                    request.session['id']=dataset[0].pk
                    request.session['position']=request.POST.get("position")
                    return HttpResponseRedirect('Overview')
                else:
                    messages.info(request,'Wrong username or password')
                    return render(request,'LoginPage.html')

class ProductBacklog(TemplateView):
    template_name = "ProductBacklog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session['position']=="Developer":
            context['user']= Developer.objects.filter(pk=self.request.session['id'])[0]
            projectID=context['user'].project.pk
        else:
            projectID=self.kwargs['project']
            context['user'] = Manager.objects.filter(pk=self.request.session['id'])[0]
        context['Project'] = Project.objects.filter(pk=projectID)[0]
        context['ProductBacklog'] = context['Project'].productbacklog_set.all().order_by('order')
        context['NumberOfPBIs'] = context['ProductBacklog'].count()
        context['Storypoints'] = context['ProductBacklog'].aggregate(total=Sum("size"))
        context['Position'] = self.request.session['position']
        return context

class Logout(View):
    def get(self, request):
        del self.request.session['id']
        del self.request.session['position']
        return HttpResponseRedirect('/BackTrack')

class CreateProject(TemplateView):
    template_name = "CreateProject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Developer.objects.filter(pk=self.request.session['id'])[0]
        context['Manager'] = Manager.objects.all()
        context['Developer'] = Developer.objects.exclude(pk=self.request.session['id']).filter(project=None)
        return context
