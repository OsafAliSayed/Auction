from django.contrib import admin
from .models import *

#User, Item, Categories are base tables.
#Watchlist, ItemCategory, owner are reference tables

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Watchlist)
admin.site.register(Categories)
admin.site.register(Comments)