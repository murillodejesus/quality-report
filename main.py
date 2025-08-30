from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.uix.camera import Camera
import os
import time

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

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
        self.inspection_report_data = []  # Lista para armazenar os dados do relatório

        # Layout da tela de inspeção
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título do passo da inspeção
        self.step_label = Label(text=self.inspection_steps[self.current_step_index], font_size='20sp', size_hint_y=None, height=40)
        main_layout.add_widget(self.step_label)

        # Widget da câmera
        self.camera_widget = Camera(resolution=(640, 480), play=True)
        main_layout.add_widget(self.camera_widget)

        # Botão para tirar a foto
        self.photo_button = Button(text='Tirar Foto', size_hint_y=None, height=50)
        self.photo_button.bind(on_press=self.take_photo)
        main_layout.add_widget(self.photo_button)

        # Campo para anotações extras
        self.notes_input = TextInput(hint_text='Anotações (opcional)', multiline=True)
        main_layout.add_widget(self.notes_input)

        # Botão para o próximo passo
        self.next_button = Button(text='Próximo', size_hint_y=None, height=50)
        self.next_button.bind(on_press=self.next_step)
        main_layout.add_widget(self.next_button)

        self.add_widget(main_layout)

    def take_photo(self, instance):
        # Sanitize o nome da fábrica para evitar caracteres inválidos
        sanitized_fabrica = ''.join(c for c in self.inspection_data['fabrica'] if c.isalnum() or c in (' ', '_'))
        sanitized_fabrica = sanitized_fabrica.strip().replace(' ', '_')

        # Sanitize o número do pedido
        sanitized_pedido = ''.join(c for c in self.inspection_data['pedido'] if c.isalnum() or c in (' ', '_'))
        sanitized_pedido = sanitized_pedido.strip().replace(' ', '_')

        # Cria o nome da pasta com os nomes sanitizados
        folder_name = f"relatorio_{sanitized_fabrica}_{sanitized_pedido}"
        
        # Se o nome da pasta estiver vazio, usa um nome padrão
        if not folder_name.strip():
            folder_name = "relatorio_sem_nome"

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Cria um nome de arquivo único para a foto
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        photo_name = f"{self.inspection_steps[self.current_step_index].replace(' ', '_')}_{timestamp}.png"
        photo_path = os.path.join(folder_name, photo_name)

        # Salva a imagem da câmera
        self.camera_widget.export_to_png(photo_path)
        print(f"Foto salva em: {photo_path}")

        # Salva o caminho da foto e as anotações
        step_data = {
            'step_name': self.step_label.text,
            'notes': self.notes_input.text,
            'photo_path': photo_path
        }
        self.inspection_report_data.append(step_data)

        # Limpa o campo de anotações
        self.notes_input.text = ''
        
        # Avança para o próximo passo (opcional, mas torna o fluxo mais ágil)
        self.next_step(instance)

    def next_step(self, instance):
        # Avança para o próximo passo, se houver
        if self.current_step_index < len(self.inspection_steps) - 1:
            self.current_step_index += 1
            self.step_label.text = self.inspection_steps[self.current_step_index]
        # Se for o último passo, gera o relatório
        else:
            print("Inspeção concluída! Gerando relatório Excel...")
            # Dados completos para o relatório
            full_report_data = {
                'inspection_data': self.inspection_data,
                'report_data': self.inspection_report_data
            }
            create_excel_report(full_report_data)
            self.manager.current = 'main_screen' # Retorna para a tela inicial

# Função para criar o relatório em Excel
def create_excel_report(data):
    # Cria uma nova planilha do Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório de Inspeção"

    # Define o cabeçalho da tabela
    headers = ["Nome da Fábrica", "Nº do Pedido", "Nome do Inspetor", "Data da Inspeção", "Passo", "Anotações", "Caminho da Foto"]
    ws.append(headers)

    # Aplica formatação ao cabeçalho (negrito e alinhado)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Preenche a planilha com os dados coletados
    # As informações gerais da inspeção serão repetidas em cada linha
    general_info = [data['inspection_data']['fabrica'], data['inspection_data']['pedido'], data['inspection_data']['inspetor'], data['inspection_data']['data']]
    
    for row_data in data['report_data']:
        row = general_info + [row_data['step_name'], row_data['notes'], row_data['photo_path']]
        ws.append(row)

    # Ajusta a largura das colunas
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Sanitize o nome da fábrica e o número do pedido para o nome do arquivo
    sanitized_fabrica = ''.join(c for c in data['inspection_data']['fabrica'] if c.isalnum())
    sanitized_pedido = ''.join(c for c in data['inspection_data']['pedido'] if c.isalnum())
    
    # Cria o nome do arquivo com os nomes sanitizados
    file_name = f"relatorio_{sanitized_fabrica}_{sanitized_pedido}.xlsx"
    
    wb.save(file_name)
    print(f"Relatório Excel salvo em: {file_name}")

# Classe principal do aplicativo
class InspectionApp(App):
    def build(self):
        # O ScreenManager gerencia todas as telas do app
        sm = ScreenManager()
        # Adiciona a tela inicial ao gerenciador
        sm.add_widget(MainScreen(name='main_screen'))
        return sm

# Executa o aplicativo
if __name__ == '__main__':
    InspectionApp().run()