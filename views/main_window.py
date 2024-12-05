"""
Gerenciador de Playlist - Interface Gráfica
Versão 1.0.0
Data: 04/12/2023

Interface gráfica principal do sistema.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QSlider, QLabel, QFileDialog,
                             QInputDialog, QComboBox, QMessageBox, QMenuBar, QMenu,
                             QDialog, QDialogButtonBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from typing import List, Dict
from models.playlist import Track
import os
import pygame.mixer


class SavePlaylistDialog(QDialog):
    """Diálogo personalizado para salvar playlist"""
    def __init__(self, parent=None, existing_names=None):
        super().__init__(parent)
        self.existing_names = existing_names or []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Salvar Playlist")
        layout = QVBoxLayout(self)

        # Combo para nome da playlist
        self.name_combo = QComboBox()
        self.name_combo.setEditable(True)
        self.name_combo.addItems(self.existing_names)

        # Label explicativo
        label = QLabel("Selecione uma playlist existente ou digite um novo nome:")
        layout.addWidget(label)
        layout.addWidget(self.name_combo)

        # Botões padrão
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_playlist_name(self):
        return self.name_combo.currentText()


class MainWindow(QMainWindow):
    """Interface principal do aplicativo"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.track_widgets: List[Dict] = []
        self.current_playing_button = None
        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        """Configura a barra de menu"""
        menubar = self.menuBar()

        # Menu Arquivo
        file_menu = menubar.addMenu('Arquivo')

        # Ação Carregar Playlist
        load_action = file_menu.addAction('Carregar Playlist')
        load_action.triggered.connect(self.update_playlist_list)

        # Ação Salvar Playlist
        save_action = file_menu.addAction('Salvar Playlist')
        save_action.triggered.connect(self.save_playlist)

        # Separador
        file_menu.addSeparator()

        # Ação Sair
        exit_action = file_menu.addAction('Sair')
        exit_action.triggered.connect(self.close)

        # Menu Ajuda
        help_menu = menubar.addMenu('Ajuda')
        about_action = help_menu.addAction('Sobre')
        about_action.triggered.connect(self.show_about)

    def show_about(self):
        """Exibe a janela Sobre"""
        QMessageBox.about(self, 'Sobre',
                          'Gerenciador de Playlist v1.0.0\n\n'
                          'Desenvolvido para gerenciar suas músicas locais.\n'
                          '© 2023 Todos os direitos reservados.')

    def setup_ui(self):
        """Configura a interface do usuário"""
        self.setWindowTitle("Gerenciador de Playlist")
        self.setMinimumWidth(900)

        # Estilo moderno com cores personalizadas
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFD700;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border: 1px solid #FFD700;
                padding: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: #1E1E1E;
                border: none;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
            QSlider::groove:horizontal {
                background: #FFD700;
                height: 6px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                border: 1px solid #FFD700;
                width: 12px;
                margin: -5px 0;
                border-radius: 6px;
            }
            QComboBox {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border: 1px solid #FFD700;
                padding: 5px;
            }
            QMenuBar {
                background-color: #1E1E1E;
                color: #FFD700;
            }
            QMenuBar::item:selected {
                background-color: #FFD700;
                color: #1E1E1E;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Adicionar logo no topo
        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = "logo.png"  # Substitua pelo caminho correto do logo
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logo_label.setText("Logo não encontrado")
            logo_label.setStyleSheet("color: #FF0000; font-size: 16px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        main_layout.addLayout(logo_layout)

        # Combo de seleção de playlist
        playlist_layout = QHBoxLayout()
        self.playlist_combo = QComboBox()
        self.playlist_combo.setFixedWidth(500)
        self.playlist_combo.currentTextChanged.connect(self.load_playlist)
        playlist_layout.addWidget(QLabel("Playlist:"))
        playlist_layout.addWidget(self.playlist_combo)
        playlist_layout.addStretch()
        main_layout.addLayout(playlist_layout)

        # Lista de faixas
        tracks_group = QWidget()
        tracks_layout = QVBoxLayout(tracks_group)

        for i in range(10):
            track_layout = QHBoxLayout()

            sequence_label = QLabel(str(i + 1))
            sequence_label.setFixedWidth(30)

            event_edit = QLineEdit()
            event_edit.setFixedWidth(200)
            event_edit.setPlaceholderText("Evento da sessão")

            name_edit = QLineEdit()
            name_edit.setFixedWidth(500)
            name_edit.setPlaceholderText("Caminho da música")

            file_btn = QPushButton("...")
            file_btn.setFixedWidth(30)

            play_btn = QPushButton("▶")
            play_btn.setFixedWidth(30)

            volume_slider = QSlider(Qt.Orientation.Horizontal)
            volume_slider.setRange(0, 100)
            volume_slider.setValue(100)
            volume_slider.setFixedWidth(150)

            track_layout.addWidget(sequence_label)
            track_layout.addWidget(event_edit, 1)
            track_layout.addWidget(name_edit, 1)
            track_layout.addWidget(file_btn)
            track_layout.addWidget(play_btn)
            track_layout.addWidget(volume_slider)

            tracks_layout.addLayout(track_layout)

            self.track_widgets.append({
                "sequence": i + 1,
                "event_edit": event_edit,
                "name_edit": name_edit,
                "file_btn": file_btn,
                "play_btn": play_btn,
                "volume_slider": volume_slider,
                "file_path": ""
            })

            file_btn.clicked.connect(lambda checked, i=i: self.select_file(i))
            play_btn.clicked.connect(lambda checked, i=i: self.play_audio(i))
            volume_slider.valueChanged.connect(lambda value, i=i: self.volume_changed(i))

        main_layout.addWidget(tracks_group)

    def select_file(self, index: int):
        """Seleciona arquivo de música"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Música",
            "",
            "Arquivos de Áudio (*.mp3 *.wav *.ogg)"
        )

        if file_path:
            self.track_widgets[index]["file_path"] = file_path
            # self.track_widgets[index]["file_btn"].setText("..." + file_path[-20:])
            self.track_widgets[index]["file_btn"].setText("...")
            # if not self.track_widgets[index]["name_edit"].text():
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            # self.track_widgets[index]["name_edit"].setText(file_name)
            self.track_widgets[index]["name_edit"].setText(file_path)

    def play_audio(self, index: int):
        """Reproduz ou para o áudio"""
        widget = self.track_widgets[index]

        if not widget["file_path"]:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo de música primeiro.")
            return

        try:
            if self.current_playing_button == widget["play_btn"] and \
               self.controller.audio_utils.is_playing:
                self.controller.stop_audio()
                widget["play_btn"].setText("▶")
                self.current_playing_button = None
            else:
                if self.current_playing_button:
                    self.current_playing_button.setText("▶")

                volume = widget["volume_slider"].value() / 100
                self.controller.play_audio(widget["file_path"], volume)
                widget["play_btn"].setText("⏹")
                self.current_playing_button = widget["play_btn"]

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao reproduzir áudio: {str(e)}")

    def volume_changed(self, index: int):
        """Atualiza o volume"""
        widget = self.track_widgets[index]
        if self.current_playing_button == widget["play_btn"] and \
           self.controller.audio_utils.is_playing:
            volume = widget["volume_slider"].value() / 100
            pygame.mixer.music.set_volume(volume)

    def get_tracks(self) -> List[Track]:
        """Obtém lista de faixas"""
        tracks = []
        for widget in self.track_widgets:
            if widget["file_path"]:
                track = Track(
                    sequence=widget["sequence"],
                    event=widget["event_edit"].text(),
                    name=widget["name_edit"].text() or os.path.splitext(
                        os.path.basename(widget["file_path"]))[0],
                    file_path=widget["file_path"],
                    volume=widget["volume_slider"].value() / 100
                )
                tracks.append(track)
        return tracks

    def save_playlist(self):
        """Salva playlist atual"""
        tracks = self.get_tracks()

        if not tracks:
            QMessageBox.warning(
                self,
                "Aviso",
                "Adicione pelo menos uma música à playlist antes de salvar."
            )
            return

        # Obtém lista de playlists existentes
        existing_names = self.controller.get_playlist_names()

        # Cria e exibe o diálogo de salvamento
        dialog = SavePlaylistDialog(self, existing_names)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_playlist_name()

            if name:
                try:
                    self.controller.save_playlist(name, tracks)
                    self.update_playlist_list()
                    self.playlist_combo.setCurrentText(name)
                    QMessageBox.information(
                        self,
                        "Sucesso",
                        f"Playlist '{name}' salva com sucesso!"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Erro",
                        f"Erro ao salvar playlist: {str(e)}"
                    )

    def load_playlist(self, name: str):
        """Carrega playlist selecionada"""
        if not name:
            return

        try:
            # Carrega as faixas da playlist
            tracks = self.controller.load_playlist(name)

            # Para qualquer áudio em reprodução
            if self.current_playing_button:
                self.controller.stop_audio()
                self.current_playing_button.setText("▶")
                self.current_playing_button = None

            # Atualiza os widgets com os dados da playlist carregada
            for widget in self.track_widgets:
                widget["event_edit"].clear()
                widget["name_edit"].clear()
                widget["file_btn"].setText("...")
                widget["volume_slider"].setValue(100)
                widget["file_path"] = ""
                widget["play_btn"].setText("▶")

            for track in tracks:
                index = track.sequence - 1
                if index < len(self.track_widgets):
                    widget = self.track_widgets[index]
                    widget["event_edit"].setText(track.event)
                    widget["name_edit"].setText(track.name)
                    widget["file_btn"].setText("...")
                    widget["volume_slider"].setValue(int(track.volume * 100))
                    widget["file_path"] = track.file_path

            # Atualiza o layout para garantir que os widgets sejam exibidos
            self.centralWidget().update()

            QMessageBox.information(
                self,
                "Sucesso",
                f"Playlist '{name}' carregada com sucesso!"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar playlist: {str(e)}"
            )                    

    def load_playlist(self, name: str):
        """Carrega playlist selecionada"""
        if not name:
            return

        try:
            # Carrega as faixas da playlist
            tracks = self.controller.load_playlist(name)

            # Para qualquer áudio em reprodução
            if self.current_playing_button:
                self.controller.stop_audio()
                self.current_playing_button.setText("▶")
                self.current_playing_button = None

            # Limpa os widgets existentes
            for widget in self.track_widgets:
                widget["event_edit"].setText("")  # Limpa o campo de evento
                widget["name_edit"].setText("")  # Limpa o campo de nome
                widget["file_btn"].setText("...")  # Reseta o botão de arquivo
                widget["volume_slider"].setValue(100)  # Reseta o volume
                widget["file_path"] = ""  # Limpa o caminho do arquivo
                widget["play_btn"].setText("▶")  # Reseta o botão de play

            # Atualiza os widgets com os dados da playlist carregada
            for track in tracks:
                index = track.sequence - 1
                if index < len(self.track_widgets):
                    widget = self.track_widgets[index]
                    widget["event_edit"].setText(track.event)
                    widget["name_edit"].setText(track.name)
                    widget["file_btn"].setText("...")
                    widget["volume_slider"].setValue(int(track.volume * 100))
                    widget["file_path"] = track.file_path

            # Atualiza o layout para garantir que os widgets sejam exibidos
            self.centralWidget().update()

            QMessageBox.information(
                self,
                "Sucesso",
                f"Playlist '{name}' carregada com sucesso!"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar playlist: {str(e)}"
            )

    def update_playlist_list(self):
        """Atualiza lista de playlists"""
        current = self.playlist_combo.currentText()
        self.playlist_combo.clear()
        names = self.controller.get_playlist_names()
        self.playlist_combo.addItems(names)
        if current in names:
            self.playlist_combo.setCurrentText(current)

    def closeEvent(self, event):
        """Manipula o evento de fechamento"""
        if self.current_playing_button:
            self.controller.stop_audio()
        event.accept()