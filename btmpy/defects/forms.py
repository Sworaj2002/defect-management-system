from django import forms
from defects.models import Defects_details


class defdetails(forms.ModelForm):
    defect_id = forms.CharField(max_length=100,disabled=True)
    defect_name = forms.CharField(max_length=100,disabled=True)
    class Meta:
        model = Defects_details
        fields = ['defect_id','defect_name','assigned_by','assigned_to','description','defect_status','priority']


class add_defectdetails(forms.ModelForm):
    class Meta:
        model = Defects_details
        fields = '__all__'