from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(self.cleaned_data["password"])
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name 				= models.CharField(max_length=30)
    last_name 				= models.CharField(max_length=30)
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    login_hex_code          = models.CharField(max_length=750, null=True, blank=True)
    jwt                     = models.CharField(max_length=1024, null=True, blank=True)
    number_of_ads           = models.IntegerField(default=0, null=True, blank=True)
    time_in_minutes         = models.IntegerField(default=0, null=True, blank=True)
    last_time_triggered		= models.DateTimeField(verbose_name='last time triggered')
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email' #login field

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def get_fullname(self):
        if self.first_name !="" and self.last_name !="":
            return self.last_name + " " + self.first_name 
        return self.email

    def get_jwt(self):
        return self.jwt
    
    def save(self, *args,  ** kwargs):
        # Removing useless spaces
        while ' ' in self.login_hex_code:
            self.login_hex_code = self.login_hex_code.replace(' ','')
        #
        # Saving
        super(Account, self).save(*args, **kwargs)
'''
    #Save The image at 400 px
    def save(self, ** kwargs): # the save method is already exist we r just modifing it
        super().save() # save the the user gave in large size
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
    #Save The image at 400 px
    '''
