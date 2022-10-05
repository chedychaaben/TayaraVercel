from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.tayara.models import Annonce
from .serializers import AnnonceSerializer

@api_view(['GET'])
def getAnnonces(request):
    annonces = Annonce.objects.all()
    serializer = AnnonceSerializer(annonces, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addAnnonce(request):
    serializer = AnnonceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()