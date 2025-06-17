#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import shutil

def check_python():
    """Verifica se o Python está instalado e é uma versão compatível"""
    try:
        version = sys.version_info
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} encontrado!")
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("⚠️ Aviso: Recomendamos Python 3.7 ou superior")
        return True
    except Exception as e:
        print(f"✗ Erro ao verificar Python: {e}")
        return False

def install_dependencies():
    """Instala as dependências necessárias"""
    print("\nInstalando dependências...")
    dependencies = ["pyinstaller", "yt-dlp"]
    
    for dep in dependencies:
        try:
            print(f"Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✓ {dep} instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao instalar {dep}: {e}")
            return False
    return True

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✓ FFmpeg encontrado: {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_install_instructions():
    """Retorna instruções de instalação específicas por plataforma"""
    current_os = platform.system()
    
    if current_os == "Darwin":  # macOS
        return {
            "python": "brew install python ou https://www.python.org/downloads/",
            "ffmpeg": "brew install ffmpeg",
            "package_manager": "Recomendamos instalar o Homebrew: https://brew.sh/"
        }
    elif current_os == "Windows":
        return {
            "python": "https://www.python.org/downloads/",
            "ffmpeg": "choco install ffmpeg -y ou https://ffmpeg.org/download.html",
            "package_manager": "Recomendamos instalar o Chocolatey: https://chocolatey.org/"
        }
    else:  # Linux
        return {
            "python": "sudo apt install python3 python3-pip",
            "ffmpeg": "sudo apt install ffmpeg",
            "package_manager": "Use o gerenciador de pacotes da sua distribuição"
        }

def create_executable():
    """Cria o executável usando PyInstaller"""
    current_os = platform.system()
    
    print(f"\nCriando executável para {current_os}...")
    
    # Comando base do PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "YouTube MP3 Downloader",
        "--clean",
        "youtube_mp3_downloader_gui.py"
    ]
    
    # Adicionar opções específicas por plataforma
    if current_os == "Darwin":
        # Para macOS, adicionar opções específicas
        cmd.extend(["--osx-bundle-identifier", "com.youtubedownloader.app"])
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao criar executável: {e}")
        return False

def main():
    current_os = platform.system()
    instructions = get_install_instructions()
    
    print("=" * 60)
    print("YouTube MP3 Downloader - Build Script")
    print(f"Sistema: {current_os}")
    print("=" * 60)
    
    # Verificar Python
    if not check_python():
        print(f"Para instalar Python: {instructions['python']}")
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        print("Falha ao instalar dependências.")
        sys.exit(1)
    
    # Verificar FFmpeg
    if not check_ffmpeg():
        print("\n⚠️ FFmpeg não encontrado!")
        print(f"Para instalar: {instructions['ffmpeg']}")
        print(f"Info: {instructions['package_manager']}")
        
        response = input("\nDeseja continuar mesmo assim? (y/N): ")
        if response.lower() not in ['y', 'yes', 's', 'sim']:
            print("Build cancelado.")
            sys.exit(1)
    
    # Verificar se o arquivo principal existe
    if not os.path.exists("youtube_mp3_downloader_gui.py"):
        print("✗ Arquivo 'youtube_mp3_downloader_gui.py' não encontrado!")
        print("Certifique-se de que o arquivo está no mesmo diretório.")
        sys.exit(1)
    
    # Criar executável
    if create_executable():
        # Verificar se foi criado
        if current_os == "Windows":
            exe_path = os.path.join("dist", "YouTube MP3 Downloader.exe")
        else:
            exe_path = os.path.join("dist", "YouTube MP3 Downloader")
        
        if os.path.exists(exe_path):
            print("\n" + "=" * 60)
            print("✓ Executável criado com sucesso!")
            print(f"\nLocalização: {exe_path}")
            
            if current_os == "Darwin":
                print("\nPara usar:")
                print("1. Abra o Finder")
                print("2. Navegue até a pasta 'dist'")
                print("3. Clique duas vezes no arquivo")
                print(f"4. Ou via terminal: ./{exe_path.replace(' ', '\\ ')}")
                
                # Tornar executável no macOS/Linux
                os.chmod(exe_path, 0o755)
                print("✓ Permissões de execução configuradas")
                
            elif current_os == "Windows":
                print("\nVocê pode mover este arquivo para o Desktop")
                print("ou qualquer outro local de sua preferência.")
            
            print("=" * 60)
        else:
            print("✗ Executável não foi encontrado após a criação.")
            sys.exit(1)
    else:
        print("✗ Falha ao criar o executável.")
        sys.exit(1)

if __name__ == "__main__":
    main()