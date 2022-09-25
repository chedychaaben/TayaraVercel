from django.shortcuts import render
from django.http import HttpResponse, Http404
#
import time, requests, json

from .models import Annonce, AnnonceCreateProcess, AnnonceDeleteProcess, Task


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
        annonce.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("NOT OK")


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
        return HttpResponse("OK")
    else:
        return HttpResponse("NOT OK")














def triggerAllTasks(request):
    return HttpResponse('Finished')
    


def homepage(request):
    context = {}
    return render(request, 'index.html', context=context)