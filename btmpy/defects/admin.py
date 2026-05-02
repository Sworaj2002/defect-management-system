from django.contrib import admin
from defects.models import Defects_details,Developers,Testers,Defect_Screen_Shots
# Register your models here.
admin.site.register(Defects_details)
admin.site.register(Developers)
admin.site.register(Testers)
admin.site.register(Defect_Screen_Shots)