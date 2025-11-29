from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Product, Order
from .utils import get_cnb_rates
from decimal import Decimal, ROUND_HALF_UP



# Create your views here.
def index(request):
    form = OrderForm()
    produkty = Product.objects.all()
    
    kurzy = get_cnb_rates()  # {'EUR': 24.12, 'USD': 22.45}
    
    context = {
        'form': form,
        'data': produkty,
        'kurzy': kurzy
    }
    return render(request, 'index.html', context)


def order_submit(request):
    produkty = Product.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            produkt = form.cleaned_data['produkt']
            pocet = form.cleaned_data['pocet']
            celkem = produkt.cena_z_dph * pocet

            # >>> uložit objednávku a zachytit ji <<<
            objednavka = Order.objects.create(
                jmeno=form.cleaned_data['jmeno'],
                email=form.cleaned_data['email'],
                telefon=form.cleaned_data['telefon'],
                produkt=produkt,
                pocet=pocet,
                addresa=form.cleaned_data['addresa'],
                celkem_cena=celkem
            )

            # >>> předat ID objednávky do success page <<<
            return redirect('order_success', objednavka_id=objednavka.id)

    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form, 'data': produkty})




def order_success(request, objednavka_id):
    objednavka = Order.objects.get(id=objednavka_id)
    kurzy = get_cnb_rates()  # {'EUR': 24.12, 'USD': 22.45}

    kurz_eur = Decimal(str(kurzy['EUR']))
    kurz_usd = Decimal(str(kurzy['USD']))

    cena_eur = (objednavka.celkem_cena / kurz_eur).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if kurz_eur > 0 else Decimal('0.00')
    cena_usd = (objednavka.celkem_cena / kurz_usd).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if kurz_usd > 0 else Decimal('0.00')

    return render(request, 'order_success.html', {'order': objednavka, 'kurzy': kurzy, 'cena_eur': cena_eur, 'cena_usd': cena_usd})
