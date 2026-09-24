class Inventario:
    def verificar(self, producto):
        print(f'Verificando el stock de {producto}')
        return True

class Pago:
    def procesar(self, monto):
        print(f'Procesando {monto}')
        return True

class Envio:
    def crear_envio(self, producto):
        print(f'Preparando el envío del: {producto}')

class Notificacion:
    def enviar(self):
        print("Se creó el envío correctamente")
#sistema de notificación con una dunción eniar y que tenga un mensaje y que se haga luego de que se envíe
#fachada:
class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()
        self.notificacion = Notificacion()
    def comprar(self, producto, precio):
        if not self.inventario.verificar(producto):
            print('No hay stock')
            return 
        if not self.pago.procesar(precio):
            print('Falló el pago')
            return
        
        self.envio.crear_envio(producto)
        print('Compra completada')
        self.notificacion.enviar()
    
def main():
    tienda = TiendaFacade()
    tienda.comprar('Laptop', 1500)

main()
