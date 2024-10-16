from .models import Pedidos, DetallePedidos, Empleados, TipoPedidos, Productos
from django.utils import timezone
from django.db.models import Max
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        id = str(producto.iidproducto)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id" : producto.iidproducto,
                "nombre" : producto.snombreproducto,
                "acumulado" : producto.dprecio,
                "cantidad" : 1
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.dprecio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.iidproducto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.iidproducto)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.dprecio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def crear_pedido(self, user):
        # Obtenemos al empleado a partir del usuario (user) logueado
        empleado = Empleados.objects.get(user=user)

        # Obtener el objeto TipoPedidos con id igual a 2
        tipo_pedido = TipoPedidos.objects.get(iidtipopedido=2)
       

        # Obtener el número de pedido más alto actualmente en la base de datos
        ultimo_pedido = Pedidos.objects.aggregate(Max('inropedido'))
        nuevo_numero_pedido = ultimo_pedido['inropedido__max'] + 1 if ultimo_pedido['inropedido__max'] else 1

        pedido = Pedidos(iidempleado=empleado,inropedido=nuevo_numero_pedido,iidtipopedido=tipo_pedido,dfechapedido= timezone.now().date(),iidestado=1, itotal=0)  # Crea un nuevo pedido relacionado con el empleado
        pedido.save()
        print('primero')
        print(pedido)

        total_pedido = 0

        for item in self.carrito.values():
            producto = Productos.objects.get(iidproducto=item["producto_id"])

            detalle_pedido = DetallePedidos(iidpedido=pedido, iidproducto=producto, icantidad=item["cantidad"], precio_unitario=item["acumulado"])
            detalle_pedido.save()
            total_pedido += item["acumulado"]

        pedido.itotal = total_pedido
        pedido.save()
        print('segundo')
        print(pedido)

        # Limpia el carrito después de crear el pedido
        self.limpiar()
        return pedido  # Añade esta línea para retornar el pedido creado
        

   