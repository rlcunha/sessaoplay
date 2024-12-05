# utils/config_manager.py
"""
Gerenciador de Configurações
Versão 1.0.0
"""
import json
import os
from pathlib import Path

class ConfigManager:
    """Gerencia as configurações do sistema"""

    def __init__(self):
        self.config_file = "setup.json"
        self.default_config = {
            "playlist_directory": str(Path.home() / "Documents" / "PlaylistManager"),
            "playlist_file": "playlists.json"
        }
        self.config = self.load_config()

    def load_config(self):
        """Carrega as configurações do arquivo setup.json"""
        try:
            if not os.path.exists(self.config_file):
                self.save_config(self.default_config)
                return self.default_config

            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configurações: {str(e)}")
            return self.default_config

    def save_config(self, config):
        """Salva as configurações no arquivo setup.json"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {str(e)}")

    def get_playlist_path(self):
        """Retorna o caminho completo do arquivo de playlists"""
        directory = self.config.get("playlist_directory", self.default_config["playlist_directory"])
        filename = self.config.get("playlist_file", self.default_config["playlist_file"])

        # Cria o diretório se não existir
        os.makedirs(directory, exist_ok=True)

        return os.path.join(directory, filename)