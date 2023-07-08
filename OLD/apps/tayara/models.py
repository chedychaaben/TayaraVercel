from django.db import models
import uuid

# Create your models here.

CategorieChoices = [
    ('1', 'Véhicules'),
    ('2', 'Immobilier'),
    ('3', 'Informatique et Multimedia'),
    ('4', 'Pour la Maison et Jardin'),
    ('5', 'Loisirs et Divertissement'),
    ('6', 'Habillement et Bien Etre'),
    ('7', 'Emploi et Services'),
    ('8', 'Entreprises'),
    ('9', 'Autres')
]

InformatiqueChoices = [
    ('1', 'Téléphones'),
    ('2', 'Image & Son'),
    ('3', 'Ordinateurs portables'),
    ('4', 'Accessoires informatique et Gadgets'),
    ('5', 'Jeux vidéo et Consoles'),
    ('6', 'Appareils photo et Caméras'),
    ('7', 'Tablettes'),
    ('8', 'Télévisions')
]

GouvernementChoices = [
    ('1', 'Ariana'),
    ('2', 'Béja'),
    ('3', 'Ben Arous'),
    ('4', 'Bizerte'),
    ('5', 'Gabès'),
    ('6', 'Gafsa'),
    ('7', 'Jendouba'),
    ('8', 'Kairouan'),
    ('9', 'Kasserine'),
    ('10', 'Kébili'),
    ('11', 'La Manouba'),
    ('12', 'Le Kef'),
    ('13', 'Mahdia'),
    ('14', 'Médenine'),
    ('15', 'Monastir'),
    ('16', 'Nabeul'),
    ('17', 'Sfax'),
    ('18', 'Sidi Bouzid'),
    ('19', 'Siliana'),
    ('20', 'Sousse'),
    ('21', 'Tataouine'),
    ('22', 'Tozeur'),
    ('23', 'Tunis'),
    ('24', 'Zaghouan')
]

DelegationChoices = [
    ('1', 'Agareb'),
    ('2', 'Autres Villes'),
    ('3', 'Bir Ali Ben Khalifa'),
    ('4', 'El Amra'),
    ('5', 'El Hencha'),
    ('6', 'Ghraiba'),
    ('7', 'Jebiniana'),
    ('8', 'Kerkennah'),
    ('9', 'Mahrès'),
    ('10', 'Menzel Chaker'),
    ('11', 'Route de GABES'),
    ('12', 'Route de l/aéroport'),
    ('13', 'Route El Afrane'),
    ('14', 'Route El AFRANE'),
    ('15', 'Route El Ain'),
    ('16', 'Route El Ain'),
    ('17', 'Route GREMDA'),
    ('18', 'Route MANZEL CHAKER'),
    ('19', 'Route Mehdia'),
    ('20', 'Route MEHDIA'),
    ('21', 'Route Menzel Chaker'),
    ('22', 'Route MHARZA'),
    ('23', 'ROUTE SALTANIA'),
    ('24', 'Route SOKRA'),
    ('25', 'Route Soukra'),
    ('26', 'Route TANIOUR'),
    ('27', 'Route Tunis'),
    ('28', 'Route TUNIS'),
    ('29', 'Sakiet Eddaïer'),
    ('30', 'Sakiet Ezzit'),
    ('31', 'Sfax Médina'),
    ('32', 'Sfax Ville'),
    ('33', 'Skhira'),
    ('34', 'Thyna'),
]

class Annonce(models.Model):
    categorie               = models.IntegerField(null=False)
    sousCategorie           = models.IntegerField(null=False)
    titre                   = models.CharField(max_length=128, null=False)
    description             = models.TextField(max_length=512, null=False)
    prix                    = models.IntegerField(null=False)
    livraison               = models.BooleanField(default=False)
    ville                   = models.IntegerField(null=False)
    delegation              = models.IntegerField(null=False)
    
    images                  = models.ManyToManyField('AnnonceImage')
    principalPhoneNumber    = models.BooleanField(default=True)
    secondaryPhoneNumber    = models.IntegerField(default=0)
    is_actif                = models.BooleanField(default=True)
    times_posted            = models.IntegerField(default=0)
    times_deleted           = models.IntegerField(default=0)

    creation_date           = models.DateTimeField(auto_now_add = True, auto_now = False, editable=False)
    last_created_token      = models.CharField(max_length=128, null=False)

    class Meta:
        ordering = ['-creation_date']
    
    def __str__(self):
        return self.titre

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

    def get_old_token(self):
        return self.last_created_token

    def is_online(self):
        if self.times_posted > self.times_deleted:
            return True
        return False


class AnnonceImage(models.Model):
    image = models.ImageField(default=None, upload_to='ad_images')

    def __str__(self):
        return self.image.name


class AnnonceCreateProcess(models.Model):
    token                           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annonce                         = models.ForeignKey('Annonce', 
                                                    related_name='AnnonceOfTheCreateProcess',
                                                    on_delete=models.SET_NULL,
                                                    null=True
                                                    )
    # Login
    loggedIn                        = models.BooleanField(null=True)
    loginPageOnePassed              = models.BooleanField(null=True)
    loginPageTwoPassed              = models.BooleanField(null=True)
    loginTimeInSeconds              = models.FloatField(null=True, blank=True)

    # Creation
    newCreatedArticleToken          = models.CharField(max_length=128, null=False)
    annonceCreated                  = models.BooleanField(null=True)
    createAnnoncePageOnePassed      = models.BooleanField(null=True)
    createAnnoncePageTwoPassed      = models.BooleanField(null=True)
    createAnnoncePageThreePassed    = models.BooleanField(null=True)
    createAnnoncePageFourPassed     = models.BooleanField(null=True)
    createAnnonceTimeInSeconds      = models.FloatField(null=True, blank=True)
    #
    processCompleted                = models.BooleanField(default=False)
    started                         = models.DateTimeField(auto_now_add = True, auto_now = False, editable=False)

    class Meta:
        ordering = ['-started']
    
    def __str__(self):
        return self.started.strftime("%A, %d %B %Y %H:%M")

class AnnonceDeleteProcess(models.Model):
    token                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annonceToken            = models.CharField(max_length=128, null=False)

    # Login
    loggedIn                        = models.BooleanField(null=True)
    loginPageOnePassed              = models.BooleanField(null=True)
    loginPageTwoPassed              = models.BooleanField(null=True)
    loginTimeInSeconds              = models.FloatField(null=True, blank=True)

    # Deletion
    annonceDeleted                  = models.BooleanField(null=True)
    deleteAnnonceTimeInSeconds      = models.FloatField(null=True, blank=True)

    processCompleted        = models.BooleanField(default=False)
    started                 = models.DateTimeField(auto_now_add = True, auto_now = False, editable=False)

    class Meta:
        ordering = ['-started']
    
    def __str__(self):
        return self.started.strftime("%A, %d %B %Y %H:%M")


class Task(models.Model):
    createAnnonce           = models.BooleanField(null=True)
    annonceToCreate         = models.ForeignKey('Annonce', 
                                                related_name='annonceOfTask',
                                                on_delete=models.SET_NULL,
                                                null=True,
                                                blank=True
                                                )
    deleteAnnonce           = models.BooleanField(null=True)
    annonceToDeleteToken    = models.CharField(max_length=128, null=True, blank=True)

    #
    creation_date           = models.DateTimeField(auto_now_add = True, auto_now = False, editable=False)

    class Meta:
        ordering = ['-creation_date']
    
    def __str__(self):
        return self.creation_date.strftime("%A, %d %B %Y %H:%M")