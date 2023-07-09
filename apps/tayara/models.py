from django.db import models
import uuid
from ..users.models import Account
# Create your models here.

class Annonce(models.Model):
    hex_code                = models.TextField(null=False)  # No limit length
    main_id                 = models.CharField(max_length=24, null=True, blank=True)   # Example 6459dd50a4cb3b2e7a3fff63 (24 Caracters)
    title                   = models.CharField(max_length=128, null=True, blank=True)
    description             = models.TextField(max_length=512, null=True, blank=True)
    price                   = models.IntegerField(null=True, blank=True)
    images                  = models.ManyToManyField('AnnonceImage', blank=True)
    is_actif                = models.BooleanField(default=True)
    creation_date           = models.DateTimeField(auto_now_add = True, auto_now = False, editable=False)
    user                    = models.ForeignKey(Account, related_name='Annonce_user', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-creation_date']
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            if len(self.hex_code) > 8:
                return self.hex_code[:4] + '...' + self.hex_code[-4:]
            else:
                return self.hex_code
    """
    def getObject(self):
        return {
                'categorie'            : self.categorie ,
                'sousCategorie'        : self.sousCategorie ,
                'titre'                : self.titre ,
                'description'          : self.description ,
                'prix'                 : self.prix ,
                'livraison'            : self.livraison ,
                'imagesUrls'           : [(str(i.image.url)+".jpg") for i in self.images.all()] ,
                'ville'                : self.ville ,
                'delegation'           : self.delegation ,
                'principalPhoneNumber' : self.principalPhoneNumber ,
                'phoneNumber'          : self.secondaryPhoneNumber
                }
    """
    def getURL(self):
        return f"https://www.tayara.tn/item/{self.main_id}/"
    
    def save(self, *args,  ** kwargs):
        # Removing useless spaces
        while ' ' in self.hex_code:
            self.hex_code = self.hex_code.replace(' ','')
        #
        # Saving
        super(Annonce, self).save(*args, **kwargs)

class AnnonceImage(models.Model):
    main_id = models.TextField(max_length=40, null=True) # Example c36df87b-886b-4147-9151-ccb4ae3f59e2  (35-40 Caracters)
    
    def __str__(self):
        return self.main_id
    
    def getURL(self):
        return f"https://storage.googleapis.com/tayara-migration-yams-pro/{self.main_id[:2]}/{self.main_id}"


EventNatureChoices = [
    ('LOGIN', 'LOGIN'),
    ('CREATE', 'CREATE'),
    ('DELETE', 'DELETE'),
]

class Event(models.Model):
    nature  = models.CharField(max_length=10,choices=EventNatureChoices)
    related_annonce_id = models.CharField(max_length=24, null=True, blank=True)
    jwt                = models.CharField(max_length=1024, null=True, blank=True)
    success            = models.BooleanField(default=False)
    was_manual         = models.BooleanField(default=True)
    creation_date      = models.DateTimeField(auto_now_add = True, auto_now = False, editable=False)
    user               = models.ForeignKey(Account, related_name='Event_user', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nature