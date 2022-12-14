from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
#
import time, requests, json

from .models import Annonce, AnnonceCreateProcess, AnnonceDeleteProcess, Task
from apps.users.models import Account as User

@login_required
def createAnnonce(request,annonceId):
    try:
        annonce = Annonce.objects.get(pk=int(annonceId))
    except Annonce.DoesNotExist:
        raise Http404("Given annonce not found....")
    AWS_CREATE_URL = "https://axp2b47ur6jkrfdipy7pk7djne0mmncg.lambda-url.eu-west-1.on.aws/"
    p = AnnonceCreateProcess.objects.create()
    p.annonce = annonce
    p.save()
    r = requests.get(AWS_CREATE_URL, headers={"data": json.dumps(annonce.getObject())})
    if r.status_code == 200:
        this_lifeCycle = json.loads(r.text)
        # Login
        p.loggedIn                      = this_lifeCycle['loggedIn']
        p.loginPageOnePassed            = this_lifeCycle['loginPageOnePassed']
        p.loginPageTwoPassed            = this_lifeCycle['loginPageTwoPassed']
        p.loginTimeInSeconds            = this_lifeCycle['loginTimeInSeconds']
        # Creation
        p.annonceCreated                = this_lifeCycle['annonceCreated']
        p.newCreatedArticleToken        = this_lifeCycle['newCreatedArticleToken']
        p.createAnnoncePageOnePassed    = this_lifeCycle['createAnnoncePageOnePassed']
        p.createAnnoncePageTwoPassed    = this_lifeCycle['createAnnoncePageTwoPassed']
        p.createAnnoncePageThreePassed  = this_lifeCycle['createAnnoncePageThreePassed']
        p.createAnnoncePageFourPassed   = this_lifeCycle['createAnnoncePageFourPassed']
        p.createAnnonceTimeInSeconds    = this_lifeCycle['createAnnonceTimeInSeconds']
        # Saving
        p.processCompleted = True
        p.save()
        # save this article token to the annonce last one
        annonce.last_created_token = this_lifeCycle['newCreatedArticleToken']
        annonce.times_posted = annonce.times_posted + 1
        annonce.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("NOT OK")

@login_required
def deleteAnnonce(request,annonceToken):
    AWS_DELETE_URL = "https://ehwaetp5cnelm2nsti4d5d4zty0zedit.lambda-url.eu-west-1.on.aws/"
    p = AnnonceDeleteProcess.objects.create()
    p.annonceToken = annonceToken
    p.save()

    r = requests.get(AWS_DELETE_URL, headers={"annonceToken": str(annonceToken)})
    if r.status_code == 200:
        this_lifeCycle = json.loads(r.text)
        # Login
        p.loggedIn                      = this_lifeCycle['loggedIn']
        p.loginPageOnePassed            = this_lifeCycle['loginPageOnePassed']
        p.loginPageTwoPassed            = this_lifeCycle['loginPageTwoPassed']
        p.loginTimeInSeconds            = this_lifeCycle['loginTimeInSeconds']
        # Deletion
        p.annonceDeleted                = this_lifeCycle['annonceDeleted']
        p.deleteAnnonceTimeInSeconds    = this_lifeCycle['deleteAnnonceTimeInSeconds']
        p.processCompleted = True
        p.save()

        # Find the Annonce that has annonceToken exactly like this one and append one to it
        Annonces_with_this_token = Annonce.objects.filter(last_created_token=annonceToken)
        for A in Annonces_with_this_token:
            A.times_deleted = A.times_deleted + 1
            A.save()

        return HttpResponse("OK")
    else:
        return HttpResponse("NOT OK")













@login_required
def triggerAllTasks(request):
    return HttpResponse('Finished')
    

@login_required
def homepage(request):
    
    context = {
                "Annonces":Annonce.objects.all(),
                
            }
    return render(request, 'index.html', context=context)