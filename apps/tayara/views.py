from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import time, requests, json, httpx, re, datetime, random
from .utils import base64_to_bytes, base64_to_hex, hex_to_base64, hex_to_bytes, extract_jwt, clean_spaces_from_hex_code
from .utils import get_www_headers, get_auth_headers

from .models import Annonce, AnnonceOnTayaraNow, Event
from apps.users.models import Account as User


from rest_framework import status


@login_required
def homepage(request):
    return HttpResponse('Hey')

def createAnnonceFN(user, annonce_id):
    try:
        event = Event.objects.create(nature="CREATE")
        
        A = Annonce.objects.get(id=annonce_id)

        hexInput = A.hex_code

        event.user = user
        jwt = user.jwt

        creation_url = "https://www.tayara.tn/core/marketplace.MarketPlace/CreateAd"
        
        hexInput = clean_spaces_from_hex_code(hexInput)

        dataInBytes = hex_to_bytes(hexInput)

        # Creating
        r = httpx.post(creation_url, headers=get_www_headers(jwt), data=dataInBytes) # This Accept only bytes as data

        # Checking if okay
        if not r.text == "":
            tokens = re.findall(r'[a-f0-9]{24}', r.text)
            # The article id is always the first in that weird gzip return text
            article_id = tokens[0]

            event.related_annonce_id = article_id
            event.success = True
            A.main_id = article_id
            A.is_onTayaraNow = True
            AOTN = AnnonceOnTayaraNow.objects.create(annonce=A, user=user, tayara_annonce_id=article_id)
        
        AOTN.save()
        A.save()
        event.save()
        return True
    except:
        return False


#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createAnnonce(request):
    if createAnnonceFN(request.user, request.POST['annonce_id']):
        return HttpResponse(f"OK")
    else:
        return HttpResponse("ERROR",status=status.HTTP_400_BAD_REQUEST)

def deleteAnnonceFN(user, main_id):
    # Deleting annonce then creating related event
    
    # Getting User because it's needed for the request
    if not user or user.is_anonymous : 
        print('Request is from anonymous ')
        user = User.objects.first()
    jwt = user.jwt
    # Delete Annonce

    deletion_url = "https://www.tayara.tn/core/marketplace.MarketPlace/DeleteAd"

    hex_data = f"\u0000\u0000\u0000\u0000\u001a\n\u0018{main_id}"

    r = httpx.post(deletion_url, headers=get_www_headers(jwt), data = hex_data)
    
    # Event Creation
    event = Event.objects.create(nature="DELETE")
    event.user = user
    event.related_annonce_id = main_id

    if not r.text == "":
        event.success = True
        AOTN = AnnonceOnTayaraNow.objects.get(tayara_annonce_id=main_id)
        AOTN.delete()
    
    A = Annonce.objects.get(main_id=main_id)
    A.is_onTayaraNow = False
    A.save()

    
    event.save()
    return True

"""
    try :
        # Creating Event
        event = Event.objects.create(nature="DELETE")
        event.user = user
        jwt = user.jwt
        event.related_annonce_id = main_id

        deletion_url = "https://www.tayara.tn/core/marketplace.MarketPlace/DeleteAd"

        hex_data = f"\u0000\u0000\u0000\u0000\u001a\n\u0018{main_id}"

        r = httpx.post(deletion_url, headers=get_www_headers(jwt), data = hex_data)
        if not r.text == "":
            event.success = True
            AOTN = AnnonceOnTayaraNow.objects.get(tayara_annonce_id=main_id)
            AOTN.delete()
        
        A = Annonce.objects.get(main_id=main_id)
        A.is_onTayaraNow = False

        
        A.save()
        event.save()
        return True
    except:
        return False"""


#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def deleteAnnonce(request):
    if deleteAnnonceFN(request.user, request.POST['main_id']):
        return HttpResponse(f"OK")
    else:
        return HttpResponse("ERROR",status=status.HTTP_400_BAD_REQUEST)


def loginOnTayaraFN(user):
    try:
        # Creating Event
        event = Event.objects.create(nature="LOGIN")
        event.user = user
        if user.login_hex_code:
            url = "https://authentication.tayara.tn/Auth.auth/login"
            r = httpx.post(url, headers=get_auth_headers(), data=hex_to_bytes(user.login_hex_code))#data=dataInBytesForLogin)
            user.jwt = extract_jwt(r.text)
            event.jwt = extract_jwt(r.text)
            event.success = True
        user.save()
        event.save()
        return True
    except:
        return False



#@permission_classes([IsAuthenticated])
#@api_view(['GET'])
def loginOnTayara(request):
    if loginOnTayaraFN(request.user):
        return HttpResponse(f"OK")
    else:
        return HttpResponse("ERROR",status=status.HTTP_400_BAD_REQUEST)

def jobFN():
    print('job triggered')
    for user in User.objects.all():
        Annonces = Annonce.objects.filter(user=user, is_actif=True)
        time_nowUTC = datetime.datetime.utcnow()
        preffered_time = user.time_in_minutes
        last_time_triggeredUTC = user.last_time_triggered.replace(tzinfo=None)
        diff_in_minutes = (time_nowUTC-last_time_triggeredUTC).total_seconds() / 60

        new_Annonces_that_should_be_reposted = []

        #if diff_in_minutes > preffered_time:
        for A in Annonces:
            new_Annonces_that_should_be_reposted.append(A)
        
        print(f"Found {len(new_Annonces_that_should_be_reposted)} targets...")
        if len(new_Annonces_that_should_be_reposted) > 0:
            # Delete all Annonces on tayara now
            for AOTN in AnnonceOnTayaraNow.objects.filter(user=user):
                # Delete ALL
                deleteAnnonceFN(user, AOTN.tayara_annonce_id)
            '''
            # Create as you wish
            for i in range(user.number_of_ads):
                A = random.choice(new_Annonces_that_should_be_reposted)
                createAnnonceFN(user, A.id)
            '''
            # 1 ad post per Annonce
            for A in new_Annonces_that_should_be_reposted:
                createAnnonceFN(user, A.id)
            
        user.last_time_triggered = datetime.datetime.now()
        user.save()

    return True


def job(request):
    if jobFN():
        return HttpResponse('kk')
