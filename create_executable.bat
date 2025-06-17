@echo off
echo ===================================================
echo Criando executavel do YouTube MP3 Downloader
echo Sistema: Windows
echo ===================================================
echo.

echo Verificando se o Python esta instalado...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao foi encontrado. Por favor, instale o Python e tente novamente.
    echo Voce pode baixar o Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado! Verificando versao...
python --version

echo.
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install pyinstaller yt-dlp

echo.
echo Verificando FFmpeg (recomendado para conversao de audio)...
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo AVISO: FFmpeg nao encontrado. Recomendamos instalar para melhor funcionamento.
    echo Para instalar com Chocolatey: choco install ffmpeg -y
    echo Para instalar manualmente: https://ffmpeg.org/download.html
    echo.
    choice /C YN /M "Deseja continuar mesmo assim? (Y/N)"
    if errorlevel 2 exit /b 1
)

echo.
echo Criando o executavel...
pyinstaller --onefile --windowed --name "YouTube MP3 Downloader" --clean youtube_mp3_downloader_gui.py

echo.
echo Verificando se o executavel foi criado...
if exist "dist\YouTube MP3 Downloader.exe" (
    echo ===================================================
    echo Executavel criado com sucesso!
    echo.
    echo O executavel foi salvo em: dist\YouTube MP3 Downloader.exe
    echo.
    echo Voce pode mover este arquivo para o Desktop 
    echo ou qualquer outro local de sua preferencia.
    echo ===================================================
) else (
    echo ERRO: Falha ao criar o executavel.
    echo Verifique os logs acima para mais detalhes.
)

echo.
pause