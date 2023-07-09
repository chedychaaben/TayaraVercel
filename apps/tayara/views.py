from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import time, requests, json, httpx, re
from .utils import base64_to_bytes, base64_to_hex, hex_to_base64, hex_to_bytes, extract_jwt, clean_spaces_from_hex_code
from .utils import get_www_headers, get_auth_headers

from .models import Annonce, Event
from apps.users.models import Account as User


from rest_framework import status

#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createAnnonce(request):#,annonce_id
    try:
        event = Event.objects.create(nature="CREATE")

        annonce_id = request.POST['annonce_id']
        hexInput = Annonce.objects.get(id=annonce_id).hex_code

        user = User.objects.first() #DELETEEEEEEEEEEEEEEEEEEEEEEEE
        #user = request.user
        event.user = user
        jwt = user.jwt

        creation_url = "https://www.tayara.tn/core/marketplace.MarketPlace/CreateAd"
        
        hexInput = clean_spaces_from_hex_code(hexInput)

        dataInBytes = hex_to_bytes(hexInput)

        # Creating
        r = httpx.post(creation_url, headers=get_www_headers(jwt), data=dataInBytes) # This Accept only bytes as data

        # Checking if okay
        if not r.text == "":
            tokens = re.findall(r'\b64\w+', r.text)
            # The article id is always the first in that weird gzip return text
            article_id = tokens[0]
            event.related_annonce_id = article_id
            event.success = True
        
        event.save()
        return HttpResponse(f"Event ID : {event.id}")
    except:
        return HttpResponse("ERROR",status=status.HTTP_400_BAD_REQUEST)

#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def deleteAnnonce(request): #main_id
    try:
        # Creating Event
        event = Event.objects.create(nature="DELETE")
        main_id = request.POST['main_id']
        
        user = User.objects.first() #DELETEEEEEEEEEEEEEEEEEEEEEEEE
        #user = request.user
        event.user = user
        jwt = user.jwt
        event.related_annonce_id = main_id

        deletion_url = "https://www.tayara.tn/core/marketplace.MarketPlace/DeleteAd"

        hex_data = f"\u0000\u0000\u0000\u0000\u001a\n\u0018{main_id}"

        r = httpx.post(deletion_url, headers=get_www_headers(jwt), data = hex_data)

        if not r.text == "":
            event.success = True
        
        event.save()
        return HttpResponse(f"Event ID : {event.id}")
    except:
        return HttpResponse("ERROR",status=status.HTTP_400_BAD_REQUEST)



#@permission_classes([IsAuthenticated])
#@api_view(['GET'])
def loginOnTayara(request):
    try:
        # Creating Event
        event = Event.objects.create(nature="LOGIN")
        # Example "\u0000\u0000\u0000\u0000\u0014\n\b92268675\u0012\b92268675"
        user = User.objects.first() #DELETEEEEEEEEEEEEEEEEEEEEEEEE
        #user = request.user
        event.user = user
        if user.login_bytes_code:
            dataInBytesForLogin = user.login_bytes_code# IDK WHY DOSENT WORKKKKK
            dataInBytesForLogin = "\u0000\u0000\u0000\u0000\u0014\n\b92268675\u0012\b92268675"
            url = "https://authentication.tayara.tn/Auth.auth/login"
            r = httpx.post(url, headers=get_auth_headers(), data=dataInBytesForLogin)
            print(dataInBytesForLogin)
            if r.text:
                jwt = extract_jwt(r.text)
                if len(jwt) == 773:
                    event.jwt = jwt
                    event.success = True
        event.save()
        return HttpResponse(f"Event ID : {event.id}")
    except:
        return HttpResponse("ERROR",status=status.HTTP_400_BAD_REQUEST)




@login_required
def homepage(request):
    
    context = {
                "Annonces":Annonce.objects.all(),
                
            }
    return render(request, 'index.html', context=context)