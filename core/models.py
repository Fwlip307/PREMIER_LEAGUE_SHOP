from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Camiseta(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    detalle = models.CharField(max_length=200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    oferta = models.BooleanField()
    imagen = models.CharField(max_length=200)

    def descuento15(self):
        if self.oferta:
            print("$"+str(round(self.precio * 1.15)))
            return "$"+str(round(self.precio * 1.15))
        return ""
    def descuento10(self):
        if self.oferta:
            return "$"+str(round(self.precio * 1.1))
        return ""

class Pagos(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    id_productos = models.CharField(max_length=200)
    precio_total = models.IntegerField()
    
    def __str__(self):
        return f'Pago {self.codigo} - {self.nombre_usuario}'

class Accesorio(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    detalle = models.CharField(max_length=200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    oferta = models.BooleanField()
    imagen = models.CharField(max_length=200)
    imagen2 = models.CharField(max_length=200)
    
    def descuento15(self):
        if self.oferta:
            print("$"+str(round(self.precio * 1.15)))
            return "$"+str(round(self.precio * 1.15))
        return ""
    def descuento10(self):
        if self.oferta:
            return "$"+str(round(self.precio * 1.1))
        return ""
    

class Tour(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    detalle = models.CharField(max_length=200)
    precio = models.IntegerField()
    imagen = models.CharField(max_length=200)
    hora = models.CharField(max_length=50)

class Ticket (models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    detalle = models.CharField(max_length=200)
    precio = models.IntegerField()
    imagen = models.CharField(max_length=200)
    fecha = models.CharField(max_length=50)
        

class Zapatos(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    detalle = models.CharField(max_length=200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    oferta = models.BooleanField()
    imagen = models.CharField(max_length=200)
    
    def descuento15(self):
        if self.oferta:
            print("$"+str(round(self.precio * 1.15)))
            return "$"+str(round(self.precio * 1.15))
        return ""
    def descuento10(self):
        if self.oferta:
            return "$"+str(round(self.precio * 1.1))
        return ""
    def __str__(self):
        return self.detalle+"("+self.codigo+")"


class Producto(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    detalle = models.CharField(max_length=200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    oferta = models.BooleanField()
    imagen = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.detalle} ({self.codigo})"

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

class Pago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return f"Pago de {self.usuario.username} - Total: {self.total}"