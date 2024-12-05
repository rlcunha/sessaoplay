# utils/audio_handler.py
"""
Gerenciador de Playlist - Manipulador de Áudio
Versão 1.0.0
Data: 04/12/2023

Utilitário para manipulação de arquivos de áudio.
"""
# utils/audio_handler.py
import ffmpeg
import json
from pathlib import Path
from typing import Dict, Any
import pygame.mixer
import threading
import time

class AudioUtils:
    """Classe utilitária para manipulação de áudio"""

    def __init__(self):
        pygame.mixer.init()
        self.current_playing = None
        self.is_playing = False

    def play_audio(self, file_path: str, volume: float) -> None:
        """
        Reproduz um arquivo de áudio

        Args:
            file_path (str): Caminho do arquivo
            volume (float): Volume da reprodução
        """
        try:
            if self.current_playing:
                pygame.mixer.music.stop()
                self.is_playing = False

            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
            self.current_playing = file_path
            self.is_playing = True

        except Exception as e:
            raise Exception(f"Erro ao reproduzir áudio: {str(e)}")

    def stop_audio(self) -> None:
        """Para a reprodução do áudio atual"""
        try:
            if self.is_playing:
                pygame.mixer.music.stop()
                self.is_playing = False
                self.current_playing = None
        except Exception as e:
            raise Exception(f"Erro ao parar áudio: {str(e)}")

    @staticmethod
    def validate_audio_file(file_path: str) -> bool:
        """
        Valida se o arquivo é um arquivo de áudio válido

        Args:
            file_path (str): Caminho do arquivo

        Returns:
            bool: True se válido, False caso contrário
        """
        try:
            probe = ffmpeg.probe(file_path)
            return 'audio' in probe['streams'][0]['codec_type']
        except Exception:
            return False

    @staticmethod
    def adjust_volume(file_path: str, volume: float) -> None:
        """
        Ajusta o volume do arquivo de áudio

        Args:
            file_path (str): Caminho do arquivo
            volume (float): Valor do volume (0.0 a 2.0)
        """
        try:
            stream = ffmpeg.input(file_path)
            stream = ffmpeg.filter(stream, 'volume', volume=volume)
            stream = ffmpeg.output(stream, f"temp_{Path(file_path).name}")
            ffmpeg.run(stream, overwrite_output=True)
        except Exception as e:
            raise Exception(f"Erro ao ajustar volume: {str(e)}")

