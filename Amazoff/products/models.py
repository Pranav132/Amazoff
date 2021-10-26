from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


# creating model for products

class Product(models.Model):

    # will include a name field, title field, price, description field, inventory value
    # tags for searching (not displayed), popularity for filtering purposes and a maximum of 6 images
    # using JSONs as we can easily parse through them in javascript files

    name = models.CharField("Name", max_length=120)
    site_title = models.CharField("Title", max_length=60)
    price = models.IntegerField("Price")
    description = models.TextField("Description", blank=True)
    inventory = models.IntegerField("Inventory")
    tags = models.JSONField("Tags", encoder=None, decoder=None)
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
