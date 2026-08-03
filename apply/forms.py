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
    father_name = forms.CharField(max_length=100, required=True, label="Emri i Babait")
    birthday = forms.DateField(required=True, label="Ditëlindja")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=50, required=True, label="Nr. Telefonit")
    card_id_number = forms.CharField(
        max_length=20, required=True, label="Numri i Kartës së Identitetit"
    )
    university_degree = forms.ChoiceField(
        choices=(
            ("bachelor", "Bachelor"),
            ("master", "Master"),
            ("doctorate", "Doktoraturë"),
            ("other", "Tjetër"),
        ),
        required=True,
        label="Diploma Universitare",
    )
    training = forms.ModelChoiceField(
        queryset=Training.objects.none(), required=True, label="Trajnimi"
    )
    timetable = forms.ChoiceField(
        choices=(
            ("morning", "11:00 - 13:00"),
            ("afternoon", "17:00 - 19:00"),
            ("evening", "19:00 - 21:00"),
        ),
        required=True,
        label="Orari i Preferuar",
    )
    message = forms.CharField(max_length=300, required=True, label="Mesazhi")
    terms_conditions = forms.BooleanField(required=True, label="Termat dhe Kushtet")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["training"].queryset = Training.objects.all().order_by("training_name")
