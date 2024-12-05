# models/playlist.py
from dataclasses import dataclass
from typing import List
import json
from utils.config_manager import ConfigManager

@dataclass
class Track:
    sequence: int
    event: str
    name: str
    file_path: str
    volume: float

class PlaylistModel:
    """Modelo para gerenciamento de playlists"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.playlists_file = self.config_manager.get_playlist_path()

    def save_playlist(self, name: str, tracks: List[Track]) -> None:
        """
        Salva uma playlist no arquivo JSON

        Args:
            name (str): Nome da playlist
            tracks (List[Track]): Lista de faixas
        """
        try:
            try:
                with open(self.playlists_file, 'r', encoding='utf-8') as f:
                    playlists = json.load(f)
            except FileNotFoundError:
                playlists = {}

            playlists[name] = [
                {
                    "sequence": t.sequence,
                    "event": t.event,
                    "name": t.name,
                    "file_path": t.file_path,
                    "volume": t.volume
                } for t in tracks
            ]

            with open(self.playlists_file, 'w', encoding='utf-8') as f:
                json.dump(playlists, f, indent=4)

        except Exception as e:
            raise Exception(f"Erro ao salvar playlist: {str(e)}")

    def load_playlist(self, name: str) -> List[Track]:
        """
        Carrega uma playlist do arquivo JSON

        Args:
            name (str): Nome da playlist

        Returns:
            List[Track]: Lista de faixas
        """
        try:
            with open(self.playlists_file, 'r', encoding='utf-8') as f:
                playlists = json.load(f)

            if name not in playlists:
                raise Exception("Playlist não encontrada")

            return [
                Track(
                    sequence=t["sequence"],
                    event=t["event"],
                    name=t["name"],
                    file_path=t["file_path"],
                    volume=t["volume"]
                ) for t in playlists[name]
            ]
        except Exception as e:
            raise Exception(f"Erro ao carregar playlist: {str(e)}")

    def get_playlist_names(self) -> List[str]:
        """
        Retorna lista de nomes das playlists salvas

        Returns:
            List[str]: Lista de nomes
        """
        try:
            with open(self.playlists_file, 'r', encoding='utf-8') as f:
                playlists = json.load(f)
            return list(playlists.keys())
        except FileNotFoundError:
            return []