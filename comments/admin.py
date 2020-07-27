from django.contrib import admin
from .models import RootComment, DerivedComment

admin.site.register(RootComment)
admin.site.register(DerivedComment)
