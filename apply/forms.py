from django import forms

from services.models import Services
from trainings.models import Training


class BusinessApplicationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Emri i kompanisë")
    delegate = forms.CharField(max_length=100, required=True, label="Përfaqësuesi")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=50, required=True, label="Nr. Telefonit")
    service = forms.ModelChoiceField(
        queryset=Services.objects.none(), required=True, label="Shërbimi"
    )
    message = forms.CharField(max_length=300, required=True, label="Mesazhi")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Services.objects.all().order_by("services_name")


class CareerApplicationForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label="Emri")
    surname = forms.CharField(max_length=50, required=True, label="Mbiemri")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=50, required=True, label="Nr. Telefonit")
    job = forms.CharField(required=True, label="Pozicioni i punës")
    cv = forms.FileField(required=True, label="CV")
    message = forms.CharField(max_length=300, required=True, label="Mesazhi")


class StudentApplicationForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label="Emri")
    surname = forms.CharField(max_length=50, required=True, label="Mbiemri")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=50, required=True, label="Nr. Telefonit")
    training = forms.ModelChoiceField(
        queryset=Training.objects.none(), required=True, label="Trajnimi"
    )
    message = forms.CharField(max_length=300, required=True, label="Mesazhi")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["training"].queryset = Training.objects.all().order_by("training_name")
