# Importa as classes necessárias do Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

# Define a classe para a tela inicial
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Cria um layout vertical para organizar os elementos
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título da tela
        main_layout.add_widget(Label(text='Início da Inspeção', font_size='24sp', size_hint_y=None, height=50))

        # Cria os campos de entrada de texto
        self.fabrica_input = TextInput(hint_text='Nome da Fábrica', size_hint_y=None, height=40)
        self.pedido_input = TextInput(hint_text='Nº do Pedido', size_hint_y=None, height=40)
        self.inspetor_input = TextInput(hint_text='Nome do Inspetor', size_hint_y=None, height=40)
        self.data_input = TextInput(hint_text='Data da Inspeção', size_hint_y=None, height=40) # Vamos simplificar e pedir a data como texto por enquanto

        # Adiciona os campos ao layout
        main_layout.add_widget(self.fabrica_input)
        main_layout.add_widget(self.pedido_input)
        main_layout.add_widget(self.inspetor_input)
        main_layout.add_widget(self.data_input)

        # Cria o botão para iniciar a inspeção
        iniciar_button = Button(text='Iniciar Inspeção', size_hint_y=None, height=50)
        iniciar_button.bind(on_press=self.start_inspection)
        main_layout.add_widget(iniciar_button)

        # Adiciona o layout à tela
        self.add_widget(main_layout)

    def start_inspection(self, instance):
        # Esta função será chamada quando o botão for pressionado
        # Por enquanto, vamos apenas imprimir os dados no terminal
        # Futuramente, ela vai nos levar para a próxima tela
        print("Iniciando inspeção com os dados:")
        print(f"Fábrica: {self.fabrica_input.text}")
        print(f"Pedido: {self.pedido_input.text}")
        print(f"Inspetor: {self.inspetor_input.text}")
        print(f"Data: {self.data_input.text}")

# Define a classe principal do aplicativo
class InspectionApp(App):
    def build(self):
        # Gerenciador de telas do Kivy
        sm = ScreenManager()

        # Adiciona a tela inicial ao gerenciador
        sm.add_widget(MainScreen(name='main_screen'))

        return sm

# Executa o aplicativo
if __name__ == '__main__':
    InspectionApp().run()