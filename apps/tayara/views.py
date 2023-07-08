from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#
import time, requests, json, httpx, re
from .utils import base64_to_bytes, base64_to_hex, hex_to_base64, hex_to_bytes, extract_jwt, clean_spaces_from_hex_code
from .utils import get_www_headers, get_auth_headers

from .models import Annonce
from apps.users.models import Account as User


@csrf_exempt
def createAnnonce(request):#,hex_code, jwt
    if request.method == 'POST':
        jwt = request.POST['jwt']
        hexInput = request.POST['hex_code']
        
        creation_url = "https://www.tayara.tn/core/marketplace.MarketPlace/CreateAd"
        
        hexInput = clean_spaces_from_hex_code(hexInput)

        dataInBytes = hex_to_bytes(hexInput)

        # Creating
        r = httpx.post(creation_url, headers=get_www_headers(jwt), data=dataInBytes) # This Accept only bytes as data

        # Checking if okay
        response_text = r.text
        creation_success = not response_text == ""
        if creation_success:
            tokens = re.findall(r'\b64\w+', response_text)
            # The article id is always the first in that weird gzip return text
            article_id = tokens[0]
            print('Article was posted')
            #return True, article_id
            return HttpResponse(f"OK {article_id}")
        else:
            print('Article was not posted')
            #return False, ''
            return HttpResponse("NOT OK")
    else:
        return HttpResponse('Only POST requsts are allowed')


@csrf_exempt
def deleteAnnonce(request): #main_id, jwt
    if request.method == 'POST':
        jwt = request.POST['jwt']
        main_id = request.POST['main_id']

        
        deletion_url = "https://www.tayara.tn/core/marketplace.MarketPlace/DeleteAd"

        hex_data = f"\u0000\u0000\u0000\u0000\u001a\n\u0018{main_id}"
        r = httpx.post(deletion_url, headers=get_www_headers(jwt), data = hex_data)

        response_text = r.text
        
        deletion_success = not response_text == ""

        if deletion_success:
            print('Article was deleted')
            return HttpResponse("OK")
            #return True, article_id
        else:
            print('Article was not deleted')
            return HttpResponse("NOT OK")
            #return False, ''
    else:
        return HttpResponse('Only POST requsts are allowed')



@csrf_exempt
def login_and_getJWT(request):
    if request.method == 'POST':
        kifech naaref el user mel api call ? bel authorization token!!!!!!
        # Exemple f"\u0000\u0000\u0000\u0000\u0014\n\b{phonenumber}\u0012\b{phonenumber}"
        dataInBytesForLogin = request.POST['dataInBytesForLogin']
        url = "https://authentication.tayara.tn/Auth.auth/login"
        r = httpx.post(url, headers=get_auth_headers(), data=dataInBytesForLogin)

        jwt = extract_jwt(r.text)

        if len(jwt) == 773:
            print('login was ok')
            #return True, jwt
            return HttpResponse(f"OK {jwt}")
        else:
            print('login was not ok')
            #return False, ''
            return HttpResponse("NOT OK")
    else:
        return HttpResponse('Only POST requsts are allowed')

@login_required
def homepage(request):
    
    context = {
                "Annonces":Annonce.objects.all(),
                
            }
    return render(request, 'index.html', context=context)