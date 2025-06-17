#!/bin/bash

echo "=================================================="
echo "Criando executável do YouTube MP3 Downloader"
echo "Sistema: macOS"
echo "=================================================="
echo

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não foi encontrado."
    echo "Para instalar:"
    echo "1. Via Homebrew: brew install python"
    echo "2. Via site oficial: https://www.python.org/downloads/"
    exit 1
fi

echo "Python encontrado! Verificando versão..."
python3 --version

echo
echo "Instalando dependências..."
python3 -m pip install --upgrade pip
python3 -m pip install pyinstaller yt-dlp

echo
echo "Verificando FFmpeg (necessário para conversão de áudio)..."
if ! command -v ffmpeg &> /dev/null; then
    echo "AVISO: FFmpeg não encontrado."
    echo "Para instalar:"
    echo "1. Via Homebrew: brew install ffmpeg"
    echo "2. Via MacPorts: sudo port install ffmpeg"
    echo
    read -p "Deseja continuar mesmo assim? (y/N): " choice
    case "$choice" in 
        y|Y ) echo "Continuando...";;
        * ) echo "Saindo..."; exit 1;;
    esac
else
    echo "✓ FFmpeg encontrado!"
    ffmpeg -version | head -1
fi

echo
echo "Criando o executável..."
python3 -m PyInstaller --onefile --windowed --name "YouTube MP3 Downloader" --clean youtube_mp3_downloader_gui.py

echo
echo "Verificando se o executável foi criado..."
if [ -f "dist/YouTube MP3 Downloader" ]; then
    echo "=================================================="
    echo "Executável criado com sucesso!"
    echo
    echo "O executável foi salvo em: dist/YouTube MP3 Downloader"
    echo
    echo "Para usar:"
    echo "1. Abra o Finder"
    echo "2. Navegue até a pasta 'dist'"
    echo "3. Clique duas vezes no arquivo 'YouTube MP3 Downloader'"
    echo
    echo "Ou via terminal: ./dist/YouTube\\ MP3\\ Downloader"
    echo "=================================================="
    
    # Tornar o arquivo executável
    chmod +x "dist/YouTube MP3 Downloader"
    echo "✓ Permissões de execução configuradas"
else
    echo "ERRO: Falha ao criar o executável."
    echo "Verifique os logs acima para mais detalhes."
    exit 1
fi

echo
echo "Pressione Enter para continuar..."
read