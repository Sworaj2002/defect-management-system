from django.urls import path
from . import views

urlpatterns = [
    path('/',views.defect_detail,name='defectdetal'),
    path('/<int:id>',views.description,name='description'),
    path('/edit/<int:id>',views.edit_defect,name='edit'),
    path('/adddefect',views.add_defects,name="adddefect"),
    path('/pending',views.pending_defects,name='pending'),
    path('/completed',views.completed_defects,name='completed'),
    path('/filterdefect',views.filter_defect,name='filterdefect'),
    path('/delete/<int:id>',views.delete_defect,name='delete'),
]

