from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

# Importa as classes necessárias para a próxima tela
from kivy.uix.image import Image
# A biblioteca kivy.uix.camera ainda não é necessária neste código,
# mas será no futuro para a funcionalidade de foto.

# Classe da tela inicial para a entrada de dados
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Layout principal da tela
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título
        main_layout.add_widget(Label(text='Início da Inspeção', font_size='24sp', size_hint_y=None, height=50))

        # Campos de entrada de texto
        self.fabrica_input = TextInput(hint_text='Nome da Fábrica', size_hint_y=None, height=40)
        self.pedido_input = TextInput(hint_text='Nº do Pedido', size_hint_y=None, height=40)
        self.inspetor_input = TextInput(hint_text='Nome do Inspetor', size_hint_y=None, height=40)
        self.data_input = TextInput(hint_text='Data da Inspeção', size_hint_y=None, height=40)

        main_layout.add_widget(self.fabrica_input)
        main_layout.add_widget(self.pedido_input)
        main_layout.add_widget(self.inspetor_input)
        main_layout.add_widget(self.data_input)

        # Botão para iniciar a inspeção
        iniciar_button = Button(text='Iniciar Inspeção', size_hint_y=None, height=50)
        iniciar_button.bind(on_press=self.start_inspection)
        main_layout.add_widget(iniciar_button)

        self.add_widget(main_layout)

    def start_inspection(self, instance):
        # Coleta os dados básicos
        inspection_info = {
            'fabrica': self.fabrica_input.text,
            'pedido': self.pedido_input.text,
            'inspetor': self.inspetor_input.text,
            'data': self.data_input.text
        }
        
        # Mudar para a tela de inspeção, passando os dados coletados
        self.manager.add_widget(InspectionScreen(name='inspection_screen', inspection_data=inspection_info))
        self.manager.current = 'inspection_screen'

# Classe da tela de inspeção passo a passo
class InspectionScreen(Screen):
    def __init__(self, inspection_data, **kwargs):
        super(InspectionScreen, self).__init__(**kwargs)
        self.inspection_data = inspection_data
        # Lista de passos da inspeção. Você pode personalizar isso facilmente.
        self.inspection_steps = ['Foto do Produto', 'Cor do Produto', 'Caixa/Frente e Verso', 'Caixa/Laterais', 'Outros Detalhes']
        self.current_step_index = 0

        # Layout da tela de inspeção
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título do passo da inspeção
        self.step_label = Label(text=self.inspection_steps[self.current_step_index], font_size='20sp', size_hint_y=None, height=40)
        main_layout.add_widget(self.step_label)

        # Botão para tirar a foto
        self.photo_button = Button(text='Tirar Foto', size_hint_y=None, height=50)
        self.photo_button.bind(on_press=self.take_photo)
                               