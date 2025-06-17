#!/usr/bin/env python3
"""
Instalador Automático do YouTube MP3 Downloader
Verifica requisitos, instala dependências e cria o executável
Compatível com Windows e macOS
"""

import os
import sys
import platform
import subprocess
import urllib.request
import json
from pathlib import Path

class YouTubeDownloaderInstaller:
    def __init__(self):
        self.os_name = platform.system()
        self.is_windows = self.os_name == "Windows"
        self.is_macos = self.os_name == "Darwin"
        self.is_linux = self.os_name == "Linux"
        
    def print_header(self):
        print("=" * 70)
        print("🎵 YouTube MP3 Downloader - Instalador Automático")
        print(f"Sistema detectado: {self.os_name}")
        print("=" * 70)
        print()

    def check_python_version(self):
        """Verifica se a versão do Python é compatível"""
        print("🐍 Verificando Python...")
        
        version = sys.version_info
        print(f"   Versão encontrada: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3:
            print("   ❌ Python 2 não é suportado. Por favor, instale Python 3.7+")
            return False
        
        if version.major == 3 and version.minor < 7:
            print("   ⚠️  Versão antiga detectada. Recomendamos Python 3.9+")
            response = input("   Deseja continuar mesmo assim? (y/N): ")
            if response.lower() not in ['y', 'yes', 's', 'sim']:
                return False
        
        print("   ✅ Python OK!")
        return True

    def check_internet_connection(self):
        """Verifica conexão com a internet"""
        print("\n🌐 Verificando conexão com a internet...")
        
        try:
            urllib.request.urlopen('https://www.google.com', timeout=5)
            print("   ✅ Conexão OK!")
            return True
        except:
            print("   ❌ Sem conexão com a internet")
            print("   Necessário para baixar dependências")
            return False

    def update_pip(self):
        """Atualiza o pip"""
        print("\n📦 Atualizando pip...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True, capture_output=True)
            print("   ✅ pip atualizado!")
            return True
        except subprocess.CalledProcessError:
            print("   ⚠️  Falha ao atualizar pip, continuando...")
            return True

    def install_dependencies(self):
        """Instala as dependências Python necessárias"""
        print("\n📚 Instalando dependências Python...")
        
        dependencies = [
            ("pyinstaller", "Criação de executáveis"),
            ("yt-dlp", "Download de vídeos do YouTube")
        ]
        
        for package, description in dependencies:
            print(f"   Instalando {package} ({description})...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True)
                print(f"   ✅ {package} instalado!")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Falha ao instalar {package}: {e}")
                return False
        
        return True

    def check_ffmpeg(self):
        """Verifica se o FFmpeg está instalado"""
        print("\n🎬 Verificando FFmpeg...")
        
        try:
            result = subprocess.run([
                "ffmpeg", "-version"
            ], check=True, capture_output=True, text=True)
            
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {version_line}")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ❌ FFmpeg não encontrado!")
            self.show_ffmpeg_instructions()
            return False

    def show_ffmpeg_instructions(self):
        """Mostra instruções para instalar FFmpeg"""
        print("\n📋 Instruções para instalar FFmpeg:")
        
        if self.is_windows:
            print("   Windows:")
            print("   1. Via Chocolatey: choco install ffmpeg -y")
            print("   2. Via Scoop: scoop install ffmpeg")
            print("   3. Download manual: https://ffmpeg.org/download.html")
            print("      - Baixe, extraia e adicione ao PATH")
            
        elif self.is_macos:
            print("   macOS:")
            print("   1. Via Homebrew: brew install ffmpeg")
            print("   2. Via MacPorts: sudo port install ffmpeg")
            print("   3. Se não tem Homebrew: https://brew.sh/")
            
        elif self.is_linux:
            print("   Linux:")
            print("   1. Ubuntu/Debian: sudo apt install ffmpeg")
            print("   2. CentOS/RHEL: sudo yum install ffmpeg")
            print("   3. Arch: sudo pacman -S ffmpeg")

    def get_latest_ytdlp_version(self):
        """Obtém a versão mais recente do yt-dlp"""
        try:
            with urllib.request.urlopen('https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest') as response:
                data = json.loads(response.read().decode())
                return data['tag_name']
        except:
            return "unknown"

    def create_executable(self):
        """Cria o executável"""
        print("\n🏗️  Criando executável...")
        
        if not os.path.exists("youtube_mp3_downloader_gui.py"):
            print("   ❌ Arquivo 'youtube_mp3_downloader_gui.py' não encontrado!")
            print("   Certifique-se de que está na pasta correta.")
            return False
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "YouTube MP3 Downloader",
            "--clean"
        ]
        
        # Opções específicas por plataforma
        if self.is_macos:
            cmd.extend([
                "--osx-bundle-identifier", "com.youtubedownloader.app"
            ])
        
        cmd.append("youtube_mp3_downloader_gui.py")
        
        try:
            print("   Executando PyInstaller...")
            subprocess.run(cmd, check=True)
            print("   ✅ Executável criado!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Falha ao criar executável: {e}")
            return False

    def verify_executable(self):
        """Verifica se o executável foi criado corretamente"""
        print("\n🔍 Verificando executável...")
        
        if self.is_windows:
            exe_path = Path("dist") / "YouTube MP3 Downloader.exe"
        else:
            exe_path = Path("dist") / "YouTube MP3 Downloader"
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Executável encontrado!")
            print(f"   📁 Local: {exe_path}")
            print(f"   📊 Tamanho: {size_mb:.1f} MB")
            
            # Configurar permissões no macOS/Linux
            if not self.is_windows:
                os.chmod(exe_path, 0o755)
                print("   🔐 Permissões configuradas")
            
            return True
        else:
            print("   ❌ Executável não encontrado!")
            return False

    def show_usage_instructions(self):
        """Mostra instruções de uso"""
        print("\n🎉 Instalação concluída com sucesso!")
        print("\n📖 Como usar:")
        
        if self.is_windows:
            print("   • Navegue até a pasta 'dist'")
            print("   • Clique duas vezes em 'YouTube MP3 Downloader.exe'")
            print("   • Ou mova o arquivo para onde desejar")
            
        elif self.is_macos:
            print("   • Abra o Finder e navegue até a pasta 'dist'")
            print("   • Clique duas vezes em 'YouTube MP3 Downloader'")
            print("   • Ou via Terminal: ./dist/YouTube\\ MP3\\ Downloader")
            
        print("\n💡 Dicas:")
        print("   • Cole URLs do YouTube na interface")
        print("   • Suporta vídeos individuais e playlists")
        print("   • Escolha a qualidade de áudio desejada")
        print("   • Os arquivos são salvos na pasta Downloads por padrão")

    def show_troubleshooting(self):
        """Mostra dicas de solução de problemas"""
        print("\n🔧 Solução de problemas:")
        print("   • Se downloads falham: verifique a URL e conexão")
        print("   • Para atualizar: pip install --upgrade yt-dlp")
        print("   • Logs detalhados aparecem na interface do app")

    def run_installation(self):
        """Executa o processo completo de instalação"""
        self.print_header()
        
        # Verificações iniciais
        if not self.check_python_version():
            print("\n❌ Instalação cancelada - Python incompatível")
            return False
        
        if not self.check_internet_connection():
            print("\n❌ Instalação cancelada - Sem internet")
            return False
        
        # Instalação
        if not self.update_pip():
            print("\n❌ Falha ao atualizar pip")
            return False
        
        if not self.install_dependencies():
            print("\n❌ Falha ao instalar dependências")
            return False
        
        # Verificar FFmpeg
        ffmpeg_ok = self.check_ffmpeg()
        if not ffmpeg_ok:
            print("\n⚠️  FFmpeg não encontrado!")
            response = input("   Deseja continuar mesmo assim? (y/N): ")
            if response.lower() not in ['y', 'yes', 's', 'sim']:
                print("\n❌ Instalação cancelada")
                return False
        
        # Criar executável
        if not self.create_executable():
            print("\n❌ Falha ao criar executável")
            return False
        
        if not self.verify_executable():
            print("\n❌ Verificação do executável falhou")
            return False
        
        # Mostrar instruções finais
        self.show_usage_instructions()
        
        if not ffmpeg_ok:
            print("\n⚠️  IMPORTANTE: Instale o FFmpeg para melhor funcionamento!")
            self.show_ffmpeg_instructions()
        
        self.show_troubleshooting()
        
        print("\n✨ Instalação completa!")
        return True

def main():
    installer = YouTubeDownloaderInstaller()
    
    try:
        success = installer.run_installation()
        if success:
            input("\nPressione Enter para sair...")
        else:
            input("\nInstalação falhou. Pressione Enter para sair...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()