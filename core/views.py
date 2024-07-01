from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
import requests
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Carrito, Pagos
from django.shortcuts import get_object_or_404
import random
import string
from .forms import PagoForm
import uuid
from django.utils.crypto import get_random_string




# Create your views here.
def home(request):
    id_es = ['0003', '0007', '0004', '0010']
    cam = Camiseta.objects.filter(codigo__in=id_es)
    context = {'cam': cam, 'user': request.user}
    return render(request, 'index.html', context)


def tickets (request):
    tkt = Ticket.objects.all()
    return render(request, 'entradas.html',{'tkt':tkt})

def camisetas (request):
    cam = Camiseta.objects.all()
    return render(request, 'camiseta.html', {'cam': cam})

def accesorios (request):
    acc = Accesorio.objects.all()
    return render(request,'accesorio.html', {'acc': acc} )

def tours (request):
    tou = Tour.objects.all()
    return render(request,'tour.html', {'tou': tou})

def zapato (request):
    zapa = Zapatos.objects.all()
    return render(request,'zapatos.html', {'zapa': zapa})

def addToCar(request, codigo):
    carrito = request.session.get("carrito", [])
    producto = None

    try:
        producto = Accesorio.objects.get(codigo=codigo)
    except Accesorio.DoesNotExist:
        try:
            producto = Camiseta.objects.get(codigo=codigo)
        except Camiseta.DoesNotExist:
            try:
                producto = Tour.objects.get(codigo=codigo)
            except Tour.DoesNotExist:
                try:
                    producto = Ticket.objects.get(codigo=codigo)
                except Ticket.DoesNotExist:
                    try:
                        producto = Zapatos.objects.get(codigo=codigo)
                    except Zapatos.DoesNotExist:
                        raise Http404("Producto no encontrado")

    for item in carrito:
        if item["codigo"] == codigo:
            item["cantidad"] += 1
            item["subtotal"] = item["cantidad"] * item["precio"]
            break
    else:
        carrito.append({
            "codigo": codigo,
            "nombre": producto.detalle,
            "imagen": producto.imagen,
            "precio": producto.precio,
            "cantidad": 1,
            "subtotal": producto.precio
        })

    request.session["carrito"] = carrito
    print("Carrito actualizado:", carrito)  
    return redirect('carrito')  
def delToCar(request, codigo):
    carrito = request.session.get("carrito", [])
    producto = None

    try:
        producto = Accesorio.objects.get(codigo=codigo)
    except Accesorio.DoesNotExist:
        try:
            producto = Camiseta.objects.get(codigo=codigo)
        except Camiseta.DoesNotExist:
            try:
                producto = Tour.objects.get(codigo=codigo)
            except Tour.DoesNotExist:
                try:
                    producto = Ticket.objects.get(codigo=codigo)
                except Ticket.DoesNotExist:
                    try:
                        producto = Zapatos.objects.get(codigo=codigo)
                    except Zapatos.DoesNotExist:
                        raise Http404("Producto no encontrado")

    item_to_remove = None

    for item in carrito:
        if item["codigo"] == codigo:
            if item["cantidad"] > 1:
                item["cantidad"] -= 1
                item["subtotal"] = item["cantidad"] * item["precio"]
            else:
                item_to_remove = item
            break

    if item_to_remove:
        carrito.remove(item_to_remove)

    request.session["carrito"] = carrito
    print("Carrito actualizado:", carrito)  
    return redirect('carrito')  

def carrito(request):
    carrito = request.session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,
    })
    
def registro(request):
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')  # Redirige a la página de éxito
    else:
        form = Registro()
    return render(request, 'registro.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Pasar request y data=request.POST
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige a la página principal después del inicio de sesión
            else:
                # Manejar el caso de credenciales inválidas
                return render(request, 'iniciar_sesion.html', {'form': form, 'error_message': 'Credenciales inválidas'})
    else:
        form = LoginForm()

    return render(request, 'iniciar_sesion.html', {'form': form})
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
        
@login_required
def procesar_pago(request):
    if request.method == 'POST':
        total = request.POST.get('total')
        
        pago = Pagos(
            codigo=str(uuid.uuid4())[:5],
            nombre_usuario=request.user.username,
            id_productos=obtener_productos_del_carrito(request.user),
            precio_total=total
        )
        pago.save()
        
        return redirect('confirmacion_pago')
    
    return redirect('carrito')

@login_required
def pagos(request):
    if request.method == 'POST':
        total = request.POST.get('total')
        pago = Pagos(
            codigo=str(uuid.uuid4())[:5],
            nombre_usuario=request.user.username,
            id_productos=obtener_productos_del_carrito(request),
            precio_total=total
        )
        pago.save()
        return redirect('confirmacion_pago')
    
    carrito = request.session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    return render(request, 'pagos.html', {
        'total': total,
    })

def obtener_productos_del_carrito(request):
    carrito = request.session.get('carrito', [])
    ids_productos = ",".join([item['codigo'] for item in carrito])
    return ids_productos

@login_required
def confirmacion_pago(request):
    return render(request, 'confirmacion_pago.html')
    
def generar_codigo_unico():
    return str(uuid.uuid4())[:5]
