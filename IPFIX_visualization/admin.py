from django.contrib import admin
from .models import *

admin.site.register(Visualization)
admin.site.register(Type)
admin.site.register(TypeToVisualization)