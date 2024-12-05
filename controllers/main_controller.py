   
# controllers/main_controller.py
"""
Gerenciador de Playlist - Controller Principal
Versão 1.0.0
Data: 04/12/2023

Controlador principal que gerencia a lógica de negócio do sistema.
"""
# controllers/main_controller.py
from models.playlist import PlaylistModel, Track
from utils.audio_handler import AudioUtils
from typing import List

class MainController:
    """Controlador principal do aplicativo"""

    def __init__(self):
        self.playlist_model = PlaylistModel()
        self.audio_utils = AudioUtils()

    def play_audio(self, file_path: str, volume: float) -> None:
        """
        Reproduz um arquivo de áudio

        Args:
            file_path (str): Caminho do arquivo
            volume (float): Volume da reprodução
        """
        self.audio_utils.play_audio(file_path, volume)

    def stop_audio(self) -> None:
        """Para a reprodução do áudio atual"""
        self.audio_utils.stop_audio()

    def save_playlist(self, name: str, tracks: List[Track]) -> None:
        """
        Salva uma playlist

        Args:
            name (str): Nome da playlist
            tracks (List[Track]): Lista de faixas
        """
        try:
            # Valida arquivos de áudio
            for track in tracks:
                if not self.audio_utils.validate_audio_file(track.file_path):
                    raise Exception(f"Arquivo inválido: {track.file_path}")

            self.playlist_model.save_playlist(name, tracks)

        except Exception as e:
            raise Exception(f"Erro ao salvar playlist: {str(e)}")

    def load_playlist(self, name: str) -> List[Track]:
        """
        Carrega uma playlist

        Args:
            name (str): Nome da playlist

        Returns:
            List[Track]: Lista de faixas
        """
        return self.playlist_model.load_playlist(name)

    def get_playlist_names(self) -> List[str]:
        """
        Obtém nomes das playlists

        Returns:
            List[str]: Lista de nomes
        """
        return self.playlist_model.get_playlist_names()
