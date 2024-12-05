# main.py
"""
Gerenciador de Playlist - Sistema de Reprodução de Áudio
Versão 1.0.0
Data: 04/12/2023

Arquivo principal do sistema que inicializa a aplicação.

### Funcionalidades
- Gerenciamento de múltiplas playlists
- Reprodução de áudio com controle individual
- Ajuste de volume por faixa
- Salvamento automático em JSON
- Interface gráfica intuitiva

### Estrutura do Projeto
- `main.py`: Arquivo principal
- `controllers/`: Controladores do sistema
- `models/`: Modelos de dados
- `views/`: Interface gráfica
- `utils/`: Utilitários e helpers

### Licença
[Sua licença aqui]

### Contato
[Suas informações de contato]

"""
# main.py
import sys
from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController
from views.main_window import MainWindow

def main():
    """Função principal do aplicativo"""
    try:
        app = QApplication(sys.argv)

        controller = MainController()
        window = MainWindow(controller)
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        print(f"Erro ao iniciar aplicativo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()