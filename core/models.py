from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, username, email, firstname, lastname, password=None):
        if username is None:
            raise TypeError('user should have username')

        if email is None:
            raise TypeError('user should have an email')

        user = self.model(username=username, email=self.normalize_email(email), firstname=firstname, lastname=lastname)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, username, email, firstname, lastname, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password, firstname, lastname)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
    
class Owner(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    # firstname = models.CharField(max_length=25, null=True)
    # lastname = models.CharField(max_length=25, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=False)
    allergicIngredients = models.CharField(db_column='AllergicIngredients',max_length=500,null=True)
    contact = models.CharField(max_length=12, db_column='CustomerContact',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']

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
    storeId = models.AutoField(db_column='StoreId',auto_created=True, primary_key=True)
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
    categoryId = models.AutoField(db_column='CategoryId' ,auto_created=True , primary_key=True)
    category_name = models.CharField(db_column='Name', max_length=100)
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
    productId = models.AutoField(db_column='ProductId',auto_created=True , primary_key=True)
    categoryId = models.ForeignKey(Category, db_column='CategoryId', on_delete=models.CASCADE)
    product_name = models.CharField(db_column='Name',max_length=100)
    description = models.CharField(db_column='Description',max_length=500,null=True)
    quantity = models.IntegerField(db_column='Quantity',null=True)
    price = models.DecimalField(db_column='Price',max_digits=7, decimal_places=2,null=True)
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


class ProductImage(models.Model):
    imageId = models.AutoField(db_column="ImageId", auto_created=True, primary_key=True)
    imagePath = models.ImageField(upload_to='images')

    # def __str__(self):
    #     return self.imagePath


class Order(models.Model):
    CHOICES = (
        ('M', 'Multiple'),
        ('S', 'Single'),
    )

    CHOICES_STATUS = (
        ('A', 'Approved'),
        ('R', 'Ready'),
        ('P', 'Preparing'),
        ('C', 'Cancelled'),
        ('D', 'Disapproved')
    )

    orderId = models.AutoField(db_column='OrderId', primary_key=True)
    customerId = models.ForeignKey(Owner, db_column='CustomerId', on_delete=models.CASCADE)
    orderDate = models.DateTimeField(db_column="OrderDate")
    orderType = models.CharField(db_column="OrderType", choices=CHOICES, null=True, max_length=15)
    OrderAmount = models.DecimalField(db_column="OrderAmount", max_digits=7, decimal_places=2)
    status = models.CharField(db_column="OrderStatus", choices=CHOICES_STATUS, null=True, max_length=15)
    paid = models.BooleanField(db_column="IsPaid", default=False)
    fromDate  = models.DateField(db_column='FromDate',null=True)
    thruDate =  models.DateField(db_column='ThruDate',null=True)
    creator = models.CharField(db_column='Creator',max_length=30,null=True)
    created  = models.DateField(db_column='Created',null=True)
    modifier = models.CharField(db_column='Modifier',max_length=30,null=True)
    modified  = models.DateField(db_column='Modified',null=True)


class OrderProduct(models.Model):
    productId = models.IntegerField(db_column="ProductId")
    storeId = models.IntegerField(db_column="StoreId")
    orderId = models.IntegerField(db_column="OrderId")
    quantity = models.IntegerField(db_column="Quantity")
    amount = models.DecimalField(db_column="Amount", max_digits=7, decimal_places=2)
