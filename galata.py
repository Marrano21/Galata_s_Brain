#!/usr/bin/env python3
import ollama
import time
import json
import random
import os
from pathlib import Path
from typing import Optional, List
import platform
import subprocess

class JARVIS:
    def __init__(self):
        self.user = self.detect_user()
        self.system = platform.system()
        self.setup_directories()
        self.boot_sequence()

    # === Configurazione ===
    def detect_user(self) -> str:
        """Rileva il nome dell'utente"""
        try:
            return os.getlogin() or "Sir"
        except:
            return "Sir"

    def setup_directories(self) -> None:
        """Crea strutture dati"""
        Path("jarvis_logs").mkdir(exist_ok=True)
        Path("jarvis_output").mkdir(exist_ok=True)

    # === Effetti ===
    def play_sound(self, sound_type: str) -> None:
        """Riproduci effetti sonori (cross-platform)"""
        sounds = {
            "boot": "https://soundbible.com/mp3/Jarvis-SoundBible.com-238868247.mp3",
            "success": "https://soundbible.com/mp3/Blip-SoundBible.com-1927126940.mp3",
            "error": "https://soundbible.com/mp3/Windows-Error-SoundBible.com-1655839472.mp3"
        }
        
        if self.system == "Darwin":
            subprocess.run(["afplay", sounds[sound_type]], stderr=subprocess.DEVNULL)
        elif self.system == "Linux":
            subprocess.run(["mpg123", sounds[sound_type]], stderr=subprocess.DEVNULL)
        elif self.system == "Windows":
            subprocess.run(["start", sounds[sound_type]], shell=True)

    def typewriter_effect(self, text: str, speed: float = 0.03) -> None:
        """Effetto macchina da scrivere"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed if char not in " \n" else 0.01)
        print()

    # === Sequenze ===
    def boot_sequence(self) -> None:
        """Sequenza di avvio cinematografica"""
        self.clear_screen()
        self.play_sound("boot")
        
        boot_messages = [
            f"Inizializzazione sistema J.A.R.V.I.S. per {self.user}...",
            "Caricamento moduli IA...",
            "Connessione a Stark Industries Network...",
            "Verifica strumenti di sviluppo...",
            "Sistema operativo pronto"
        ]

        for msg in boot_messages:
            self.typewriter_effect(f"\n\033[1;36m• {msg}\033[0m")
            time.sleep(1.5 if "Stark" in msg else 0.7)
        
        print(f"\n\033[1;32m✔ Sistema pronto\033[0m")
        time.sleep(1)
        self.clear_screen()
        self.show_banner()

    def show_banner(self) -> None:
        """Mostra banner ASCII"""
        print(r"""
        \033[1;34m
          ██╗ █████╗ ██████╗ ██╗   ██╗ █████╗ ███████╗
          ██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔════╝
          ██║███████║██████╔╝██║   ██║███████║███████╗
          ██║██╔══██║██╔══██╗██║   ██║██╔══██║╚════██║
          ██║  ██║██║  ██║██║  ██║██║  ██║███████║
          ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
        \033[0m""")
        self.typewriter_effect(f"\n\033[1;36mBuongiorno {self.user}, come posso assisterla oggi?\033[0m\n")

    # === Core Functions ===
    def generate_response(self, prompt: str) -> str:
        """Genera risposta con personalità JARVIS"""
        try:
            response = ollama.generate(
                model="starcoder2:3b",
                options={'temperature': 0.4},
                prompt=f"""
                [CONTESTO]
                Sei JARVIS, l'assistente AI di Tony Stark. 
                Risposte devono essere:
                - In italiano impeccabile
                - Con tono formale ma ironico
                - Massimo 3 frasi per spiegazioni
                - Codice perfettamente formattato

                [ESEMPI]
                Input: "Crea un bottone"
                Output: "Come desidera, {self.user}. Ecco un bottone degno di Stark Industries:\n```html\n<button class='stark-btn'>Click</button>\n```"

                Input: {prompt}
                """
            )
            return self.validate_output(response['response'])
        except Exception as e:
            self.play_sound("error")
            return f"\033[31m✖ Errore: {str(e)}\nProvi a riformulare la richiesta, {self.user}.\033[0m"

    def validate_output(self, output: str) -> str:
        """Aggiunge stile JARVIS all'output"""
        phrases = [
            f"Ecco quanto richiesto, {self.user}:",
            "Operazione completata:",
            "Risultati analizzati:",
            "Codice pronto per l'implementazione:"
        ]
        
        if "```" not in output:
            return f"\033[1;36m{random.choice(phrases)}\033[0m\n{output}"
        return f"\033[1;36m{random.choice(phrases)}\033[0m\n{output}"

    # === UI ===
    def clear_screen(self) -> None:
        """Pulisci lo schermo"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self) -> None:
        """Loop principale"""
        while True:
            try:
                user_input = input("\n\033[1;34mJARVIS ▸ \033[0m").strip()
                
                if user_input.lower() in ('exit', 'quit', 'spegniti'):
                    self.typewriter_effect(f"\n\033[1;36mCome desidera {self.user}. JARVIS in modalità standby.\033[0m")
                    break
                
                if not user_input:
                    continue
                
                print()
                response = self.generate_response(user_input)
                self.typewriter_effect(response)
                self.play_sound("success")
                
            except KeyboardInterrupt:
                self.typewriter_effect("\n\033[1;36mIn attesa dei suoi ordini, {self.user}.\033[0m")
                break
            except Exception as e:
                self.play_sound("error")
                self.typewriter_effect(f"\033[31m✖ Errore critico: {str(e)}\033[0m")

if __name__ == "__main__":
    try:
        assistant = JARVIS()
        assistant.run()
    except Exception as e:
        print(f"\n\033[1;31m⚠ Sistema JARVIS non operativo: {str(e)}\033[0m")