from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.tayara.models import Annonce
from .serializers import AnnonceSerializer

# Customizing Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
#


@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Protected with bearer token ;)
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