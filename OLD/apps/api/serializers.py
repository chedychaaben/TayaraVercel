from dataclasses import field
from rest_framework import serializers
from apps.tayara.models import Annonce

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'
