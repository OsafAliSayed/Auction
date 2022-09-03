from django.contrib.auth.models import AbstractUser
from django.db import models

# Table that holds user data
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}, {self.username}, {self.email}"

# Categories table
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.category}"


# Table that holds data of items
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    bid = models.IntegerField()
    description = models.CharField(max_length=4000)
    image = models.CharField(max_length=4000)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    # isActive - to track bidding status
    isActive = models.BooleanField(default=True)

    # To keep track of last bidder
    def default_Bidder():
        return User.objects.get(username="admin").id

    lastBidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="last_Bidder", default=default_Bidder)

    def __str__(self):
        return f"{self.id}, {self.title}, {self.bid}, {self.isActive}"

# watchlist table


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    item = models.OneToOneField(Item, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.user.username} is watching {self.item.title}"

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=2000)
    
    def __str__(self):
        return f"{self.user.username}: {self.comment}"