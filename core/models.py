from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('user should have username')
        
        if email is None:
            raise TypeError('user should have an email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        user.save()
        return user
    
    
class Owner(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Store(models.Model):
    storeId = models.IntegerField(db_column='StoreId', primary_key=True)
    storeRefId = models.CharField(max_length=20, db_column='StoreRefId')
    ownerId = models.ForeignKey(Owner, db_column='OwnerId', on_delete=models.CASCADE)
    storeName = models.CharField(db_column='Name',max_length=100)
    storeCode = models.IntegerField(db_column='StoreCode')
    streetName = models.CharField(db_column='StreetName',max_length=100)
    postalcode = models.CharField(db_column='Postalcode',max_length=7)
    city  = models.CharField(db_column='City',max_length=30)
    province  = models.CharField(db_column='Province',max_length=30)
    primaryContact = models.CharField(max_length=12, db_column='PrimaryContact',blank=True)
    secondaryContact = models.CharField(max_length=12, db_column='SecondaryContact',null=True)
    fromDate = models.DateField(db_column='FromDate',null=True)
    thruDate  = models.DateField(db_column='ThruDate',null=True)
    creator  = models.CharField(db_column='Creator',max_length=30,null=True)
    created  = models.DateField(db_column='Created',null=True)
    modifier  = models.CharField(db_column='Modifier',max_length=30,null=True)
    modified  = models.DateField(db_column='Modified',null=True)


class Category(models.Model):
    storeId = models.ForeignKey(Store, db_column='StoreId', on_delete=models.CASCADE)
    categoryId = models.IntegerField(db_column='CategoryId', primary_key=True)
    category_name = models.CharField(db_column='Name',max_length=100)
    description = models.CharField(db_column='Description',max_length=100,null=True)
    rackNumber = models.IntegerField(db_column='RackNumber',null=True)
    fromDate  = models.DateField(db_column='FromDate',null=True)
    thruDate =  models.DateField(db_column='ThruDate',null=True)
    creator = models.CharField(db_column='Creator',max_length=30,null=True)
    created  = models.DateField(db_column='Created',null=True)
    modifier = models.CharField(db_column='Modifier',max_length=30,null=True)
    modified  = models.DateField(db_column='Modified',null=True)

class Product(models.Model):
    storeId = models.ForeignKey(Store, db_column='StoreId', on_delete=models.CASCADE)
    productId = models.IntegerField(db_column='ProductId', primary_key=True)
    CategoryId = models.ForeignKey(Category, db_column='CategoryId', on_delete=models.CASCADE)
    product_name = models.CharField(db_column='Name',max_length=100)
    description = models.CharField(db_column='Description',max_length=500,null=True)
    quantity = models.IntegerField(db_column='Quantity',null=True)
    price = models.DecimalField(db_column='Price',max_digits=5, decimal_places=2,null=True)
    discount =  models.DecimalField(db_column='Discount',max_digits=3, decimal_places=2,null=True)
    #images = models.ImageField(db_column='Images',null=True)
    company = models.CharField(db_column='Company',max_length=100,null=True)
    ingredients = models.CharField(db_column='Ingredients',max_length=500,null=True)
    fromDate  = models.DateField(db_column='FromDate',null=True)
    thruDate =  models.DateField(db_column='ThruDate',null=True)
    creator = models.CharField(db_column='Creator',max_length=30,null=True)
    created  = models.DateField(db_column='Created',null=True)
    modifier = models.CharField(db_column='Modifier',max_length=30,null=True)
    modified  = models.DateField(db_column='Modified',null=True)