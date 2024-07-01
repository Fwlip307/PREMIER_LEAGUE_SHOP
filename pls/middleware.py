# middleware.py

class CarritoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Calcula la cantidad de productos en el carrito
        carrito = request.session.get("carrito", [])
        carrito_count = sum(item["cantidad"] for item in carrito)
        
        # Añade la cantidad al objeto request
        request.carrito_count = carrito_count
        
        response = self.get_response(request)
        return response
