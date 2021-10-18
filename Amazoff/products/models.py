from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField("Name", max_length=120)
    site_title = models.CharField("Title", max_length=60)
    price = models.IntegerField("Price")
    description = models.TextField("Description", blank=True)
    inventory = models.IntegerField("Inventory")
    tags = models.JSONField("Tags", encoder=None, decoder=None)
    popularity = models.IntegerField("Popularity")

    # pictures - maximum 6 pictures to be uploaded, 1 is required

    picture1 = models.ImageField(
        "Image 1", upload_to=None, height_field=None, width_field=None, max_length=100
    )
    picture2 = models.ImageField(
        "Image 2",
        blank=True,
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture3 = models.ImageField(
        "Image 3",
        blank=True,
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture4 = models.ImageField(
        "Image 4",
        blank=True,
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture5 = models.ImageField(
        "Image 5",
        blank=True,
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    picture6 = models.ImageField(
        "Image 6",
        blank=True,
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    review_count = models.IntegerField("Review Count")
    rating_count = models.IntegerField("Rating Count")
    average_rating = models.IntegerField("Average Rating")
    reviews_ratings = models.JSONField("Reviews and Ratings")
