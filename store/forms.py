from django import forms
from .models import Product
from django.core.validators import RegexValidator

validace_cisla_telefonu = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Telefonní číslo musí mít 9–15 číslic a může začínat +."
)


class OrderForm(forms.Form):
    jmeno = forms.CharField(max_length=100, label='Jméno')
    email = forms.EmailField(label='Email')
    telefon = forms.CharField(max_length=15, label='Číslo telefonu', validators=[validace_cisla_telefonu])
    produkt = forms.ModelChoiceField(queryset=Product.objects.all(), label='Vyberte produkt')
    pocet = forms.IntegerField(min_value=1, label='Množství')
    addresa = forms.CharField(widget=forms.Textarea, label='Adresa dodání')

    @property
    def celkem_cena(self):
        produkt = self.cleaned_data.get('produkt')
        pocet = self.cleaned_data.get('pocet', 1)
        if produkt:
            return produkt.cena_z_dph * pocet
        return 0
