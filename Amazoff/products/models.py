from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

# Creating a table for product categories, which can be used to create product groups for recommendations.


class subcategories(models.Model):
    name = models.CharField("Sub-Category Name", max_length=50)

    def __str__(self):
        return self.name


class Product_Categories (models.Model):
    name = models.CharField("Category Name", max_length=50)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField("Name", max_length=120)

    def __str__(self):
        return self.name


# creating model for products


class Product(models.Model):

    # will include a name field, title field, price, description field, inventory value
    # tags for searching (not displayed), popularity for filtering purposes and a maximum of 6 images
    # using JSONs as we can easily parse through them in javascript files

    name = models.CharField("Name", max_length=120)
    price = models.DecimalField(
        "Price", default=0.00, max_digits=10, decimal_places=2)
    description = models.TextField("Description", blank=True)
    inventory = models.IntegerField("Inventory")
    popularity = models.IntegerField("Popularity")

    # pictures - maximum 6 pictures to be uploaded, 1 is required

    picture1 = models.ImageField(
        "Image 1", upload_to='images/', height_field=None, width_field=None, max_length=100
    )
    picture2 = models.ImageField(
        "Image 2",
        blank=True,
        upload_to='images/',
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture3 = models.ImageField(
        "Image 3",
        blank=True,
        upload_to='images/',
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture4 = models.ImageField(
        "Image 4",
        blank=True,
        upload_to='images/',
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture5 = models.ImageField(
        "Image 5",
        blank=True,
        upload_to='images/',
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture6 = models.ImageField(
        "Image 6",
        blank=True,
        upload_to='images/',
        height_field=None,
        width_field=None,
        max_length=100,
    )

    category = models.ManyToManyField(Product_Categories)
    tags = models.ManyToManyField(Tags)
    sub_categories = models.ManyToManyField(subcategories)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)

    # wishlist is diff model
    # cart is diff model
    # addresses is diff model
    # order history is a database query
    # preferences done after category model is done

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    orderExecuted = models.BooleanField(default=False, null=True, blank=True)
    cartValue = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)
    orderDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def calcCartTotal(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.calcTotal for item in cartitems])
        return total

    @property
    def calcCartQuant(self):
        cartitems = self.cartitem_set.all()
        quantity = sum([item.quant for item in cartitems])
        return quantity


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    quant = models.IntegerField(default=0, null=True, blank=True)
    changeDate = models.DateTimeField(auto_now_add=True)

    @property
    def calcTotal(self):
        total = self.product.price * self.quant
        return total


class Wishlist(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    orderExecuted = models.BooleanField(default=False, null=True, blank=True)
    orderDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.SET_NULL, null=True)
    changeDate = models.DateTimeField(auto_now_add=True)


class Addresses(models.Model):
    name = models.CharField(max_length=100, null=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    addressLine1 = models.CharField(max_length=100, null=False)
    addressLine2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    zipCode = models.IntegerField(default=00000, null=False)
    addedDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# reviews and ratings database


class ReviewsRatings(models.Model):

    # includes a user foreign key and project foreign key, not null, to link who has reviewed which product
    # has a rating which cannot be null, validated for a range of 1 to 5 (will be stars)
    # has a review field which can be blank, as some people may just rate and not review

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    rating = models.IntegerField("Rating", default=1, validators=[
        MaxValueValidator(5), MinValueValidator(1)],
        null=False, blank=False)
    review = models.CharField("Review", max_length=250, blank=True, null=True)


class completedOrders(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(
        Addresses, on_delete=models.SET_NULL, null=True)
    orderTime = models.DateTimeField(auto_now_add=True)


'''
class User(models.Model):

    # includes phone number, email, username, saved addresses, password, wishlist

    phone_number = models.CharField(
        "Number", max_length=10, null=False)
    email = models.EmailField("Email", max_length=254,
                              null=False)
    username = models.CharField(
        "Username", max_length=50, null=False)

    # Have to figure out password validator, google said we should use forms to store passwords

    # password = models.CharField(
    #     "Password", max_length=20, null=False)

    # Wishlist will link to multiple products in the Product database instead of having the names.
    # I THINK this is how we do it, please correct if I am wrong.

    wishlist = models.ManyToManyField(
        Product)
'''
