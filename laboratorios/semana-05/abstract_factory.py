from abc import ABC, abstractmethod
class Boton(ABC):
    @abstractmethod
    def renderizar(self):
        pass

class Menu(ABC):
    @abstractmethod
    def renderizar(self):
        pass #aunque no hay nada, no me da error
class CheckBox(ABC):
    @abstractmethod
    def renderizar(self):
        pass

class CheckBoxWindows(CheckBox):
    def renderizar(self):
        print('CheckBox estilo Windows')

class CheckBoxMac(CheckBox):
    def renderizar(self):
        print('CheckBox estilo Mac')

class BotonWindows(Boton):
    def renderizar(self):
        print('Boton estilo Windows...')
class BotonMac(Boton):
    def renderizar(self):
        print('Boton estilo Mac...')

class MenuWindows(Menu):
    def renderizar(self):
        print('Menu estilo Windows...')

class MenuMac(Menu):
    def renderizar(self):
        print('Menu estilo Mac...')

class UIFactoryABC(ABC):
    @abstractmethod
    def crear_boton(self):
        pass
    @abstractmethod
    def crear_menu(self):
        pass
    @abstractmethod
    def crear_checkbox(self):
        pass

class WindowsFactory(UIFactoryABC):
    def crear_boton(self):
        return BotonWindows()
    def crear_menu(self):
        return MenuWindows()
    def crear_checkbox(self):
        return CheckBoxWindows()
    

class MacFactory(UIFactoryABC):
    def crear_boton(self):
        return BotonMac()
    def crear_menu(self):
        return MenuMac()  
    def crear_checkbox(self):
        return CheckBoxMac()
    
def crear_UI(factory):
    boton = factory.crear_boton()
    menu = factory.crear_menu()
    checkbox = factory.crear_checkbox()
    boton.renderizar()
    menu.renderizar()
    checkbox.renderizar()

def main():
    sistema = 'Mac'
    if sistema == 'Windows':
        factory = WindowsFactory()
    elif sistema == 'Mac':
        factory = MacFactory()

    crear_UI(factory)

main()