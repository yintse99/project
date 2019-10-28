from django.shortcuts import render
from django.views.generic import TemplateView,View
from BackTrack.models import *
from BackTrack.forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum,F,Window,Func
# Create your views here.

class LoginPage(View):
    def get(self, request):
        if 'position' in request.session:
            if request.session['position']=="Developer":
                if Developer.objects.get(pk=request.session['id']).project is None:
                    return HttpResponseRedirect('CreateProject')
                else:
                    return HttpResponseRedirect('Productbacklog/')
            else:
                return HttpResponseRedirect('Overview')
        else:
            return render(request,'LoginPage.html')

class Signin(View):
    def post(self, request):
        if request.POST.get("username")=="" or request.POST.get("password")=="":
            messages.info(request,'Please fill in username and password.')
            return render(request,'LoginPage.html')
        else:
            if request.POST.get("position")=="Developer":
                dataset = Developer.objects.filter(username=request.POST.get("username"))
                if dataset.exists() and dataset[0].password==request.POST.get("password"):
                    request.session['id']=dataset[0].pk
                    request.session['position']=request.POST.get("position")
                    if dataset[0].project is None:
                        return HttpResponseRedirect('CreateProject')
                    else:
                        return HttpResponseRedirect('Productbacklog/')
                else:
                    messages.info(request,'Wrong username or password.')
                    return render(request,'LoginPage.html')
            else:
                dataset = Manager.objects.filter(username=request.POST.get("username"))
                if dataset.exists() and dataset[0].password==request.POST.get("password"):
                    request.session['id']=dataset[0].pk
                    request.session['position']=request.POST.get("position")
                    return HttpResponseRedirect('Overview')
                else:
                    messages.info(request,'Wrong username or password')
                    return render(request,'LoginPage.html')

class Productbacklog(TemplateView):
    template_name = "ProductBacklog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session['position']=="Developer":
            context['user']= Developer.objects.filter(pk=self.request.session['id'])[0]
            projectID=context['user'].project.pk
        else:
            projectID=self.request.GET.get("id")
            self.request.session['project']=projectID
            context['user'] = Manager.objects.filter(pk=self.request.session['id'])[0]
        context['Project'] = Project.objects.filter(pk=projectID)[0]
        context['ProductBacklog'] = context['Project'].productbacklog_set.all().order_by('order')
        cumulative =0
        for item in context['ProductBacklog']:
            cumulative +=item.size
            item.cumulative = cumulative
        context['NumberOfPBIs'] = context['ProductBacklog'].count()
        context['Storypoints'] = context['ProductBacklog'].aggregate(total=Sum("size"))
        context['Position'] = self.request.session['position']
        return context

class Logout(View):
    def get(self, request):
        del request.session['id']
        del request.session['position']
        if 'project' in request.session:
            del request.session['project']
        return HttpResponseRedirect('/BackTrack')

class CreateProject(TemplateView):
    template_name = "CreateProject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Developer.objects.filter(pk=self.request.session['id'])[0]
        context['Manager'] = Manager.objects.all()
        context['Developer'] = Developer.objects.exclude(pk=self.request.session['id']).filter(project=None)
        return context

class AddPBI(View):
    def post(self, request):
        projectID = Developer.objects.get(pk=request.session['id']).project.pk
        p = Project.objects.filter(pk=projectID)[0]
        numberOfPBIs = p.productbacklog_set.all().count()
        q = ProductBacklog(project=p,name=request.POST.get("name"),description=request.POST.get("description"),size=request.POST.get("size"),sprintbacklog=None,status="1",order=numberOfPBIs+1)
        q.save()
        return HttpResponseRedirect('/BackTrack/Productbacklog/')

class DeletePBI(View):
    def get(self,request):
        project = Developer.objects.get(pk=request.session['id']).project
        if project.product_owner.pk!=request.session['id']:
            return HttpResponseRedirect('/BackTrack/Productbacklog/')
        projectID = project.pk
        d = ProductBacklog.objects.get(pk=request.GET.get("id"),project=projectID)
        temp = d.order
        d.delete()
        u = ProductBacklog.objects.filter(order__gt=d.order).update(order=F('order') - 1)
        return HttpResponseRedirect('/BackTrack/Productbacklog/')

class Filter(TemplateView):
    template_name = "ProductBacklog.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        ctx = super(Filter, self).get_context_data(**kwargs)
        if self.request.session['position']=="Developer":
            ctx['user']= Developer.objects.filter(pk=self.request.session['id'])[0]
        else:
            ctx['user'] = Manager.objects.filter(pk=self.request.session['id'])[0]
        if 'project' in self.request.session:
            projectID = self.request.session['project']
        else:
            projectID = Developer.objects.get(pk=self.request.session['id']).project.pk
        ctx['Project'] = Project.objects.filter(pk=projectID)[0]
        larger=self.request.POST.get("larger",'')
        if larger=='':
            larger=0
        ctx['ProductBacklog'] = ctx['Project'].productbacklog_set.filter(size__gte=larger).order_by('order')
        smaller=self.request.POST.get("smaller",'')
        if smaller!='':
            ctx['ProductBacklog'] = ctx['ProductBacklog'].filter(size__lte=smaller)
        notinsprint=self.request.POST.get("notinsprint",'')
        if notinsprint!='':
            ctx['ProductBacklog'] = ctx['ProductBacklog'].exclude(status=notinsprint)
        insprint=self.request.POST.get("insprint",'')
        if insprint!='':
            ctx['ProductBacklog'] = ctx['ProductBacklog'].exclude(status=insprint)
        finished=self.request.POST.get("finished",'')
        if finished!='':
            ctx['ProductBacklog'] = ctx['ProductBacklog'].exclude(status=finished)
        ctx['NumberOfPBIs'] = ctx['ProductBacklog'].count()
        ctx['Storypoints'] = ctx['ProductBacklog'].aggregate(total=Sum("size"))
        ctx['Position'] = self.request.session['position']
        return ctx

class Overview(TemplateView):
    template_name = "Overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Manager.objects.filter(pk=self.request.session['id'])[0]
        context['Project'] = context['user'].project_set.filter(scrum_master=self.request.session['id'])
        context['NumberOfProjects'] = context['Project'].count()
        return context
