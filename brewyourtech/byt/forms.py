### START ### 

from django import forms

class PhoneFilterForm(forms.Form):
    price = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)
    launch_year = forms.IntegerField(required=False, min_value=2000, max_value=2050)
    ram = forms.IntegerField(required=False, min_value=0)
    main_camera = forms.IntegerField(required=False, min_value=0)
    selfie_camera = forms.IntegerField(required=False, min_value=0)
    sound_jack = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], required=False)
    bluetooth = forms.IntegerField(required=False, min_value=0, max_value=5)  
    battery_capacity = forms.IntegerField(required=False, min_value=0)

class LaptopFilterForm(forms.Form):
    price = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)
    ram = forms.IntegerField(required=False, min_value=0)
    inches = forms.DecimalField(required=False, min_value=0, max_digits=5, decimal_places=2)
    cpu_company = forms.CharField(required=False)

class CameraFilterForm(forms.Form):
    price = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=1,label="Price in USD")
    max_resolution = forms.IntegerField(required=False, min_value=1, label="Max Resolution (MP)") 
    release_date = forms.IntegerField(required=False, min_value=1980, max_value=2024)

class TabletFilterForm(forms.Form):
    price = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)
    display_size_inches = forms.DecimalField(required=False, min_value=0, max_digits=5, decimal_places=2)
    battery_capacity = forms.IntegerField(required=False, min_value=0)

### END ### 