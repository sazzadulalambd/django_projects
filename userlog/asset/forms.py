from django import forms
from .models import *

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'image', 'brand_name', 'model', 'sn_number', 'description', 'purchase_date', 'expire_Date', 'price', 'invoice_img', 'status', 'report']
