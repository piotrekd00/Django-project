from django.forms import ModelForm
from main.models import Rented


class RentForm(ModelForm):
    class Meta:
        model = Rented
        fields = [
            "date_start",
            "date_end",
        ]