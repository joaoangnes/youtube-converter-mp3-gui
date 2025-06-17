# YouTube MP3 Downloader - Versão Multiplataforma

Um aplicativo com interface gráfica para baixar vídeos do YouTube e convertê-los para MP3, compatível com **Windows** e **macOS**.

## 🚀 Características

- ✅ Interface gráfica amigável
- ✅ Suporte a vídeos individuais
- ✅ Suporte a playlists completas
- ✅ Download em lote de múltiplas URLs
- ✅ Múltiplas qualidades de áudio (128k, 192k, 256k, 320k)
- ✅ Compatível com Windows e macOS
- ✅ Log detalhado do processo
- ✅ Seleção personalizada da pasta de destino

## 📋 Pré-requisitos

### Para ambos os sistemas:
- **Python 3.7+** (recomendado Python 3.9+)
- **FFmpeg** (necessário para conversão de áudio)

### Windows
- Python: [python.org/downloads](https://www.python.org/downloads/)
- FFmpeg: 
  - Via Chocolatey: `choco install ffmpeg -y`
  - Download manual: [ffmpeg.org](https://ffmpeg.org/download.html)

### macOS
- Python: `brew install python` ou [python.org/downloads](https://www.python.org/downloads/)
- FFmpeg: `brew install ffmpeg`
- Homebrew (se não tiver): [brew.sh](https://brew.sh/)

## 🛠️ Instalação

### Método 1: Script Automático (Recomendado)

#### Windows:
1. Baixe todos os arquivos para uma pasta
2. Execute `create_executable.bat`
3. O executável será criado em `dist/YouTube MP3 Downloader.exe`

#### macOS:
1. Baixe todos os arquivos para uma pasta
2. Abra o Terminal na pasta
3. Execute: `chmod +x create_executable.sh && ./create_executable.sh`
4. O executável será criado em `dist/YouTube MP3 Downloader`

### Método 2: Script Python Universal

```bash
# Para qualquer sistema
python3 build.py
```

### Método 3: Instalação Manual

```bash
# 1. Instalar dependências
pip install pyinstaller yt-dlp

# 2. Criar executável
pyinstaller --onefile --windowed --name "YouTube MP3 Downloader" --clean youtube_mp3_downloader_gui.py
```

## 🎯 Como Usar

### Executando o Aplicativo

#### Windows:
- Clique duas vezes em `YouTube MP3 Downloader.exe`

#### macOS:
- Clique duas vezes em `YouTube MP3 Downloader` no Finder
- Ou via terminal: `./dist/YouTube\ MP3\ Downloader`

### Funcionalidades

1. **Vídeo Único**: Cole a URL de um vídeo do YouTube
2. **Playlist Completa**: Cole a URL de uma playlist
3. **Download em Lote**: Selecione um arquivo .txt com URLs (uma por linha)
4. **Qualidades Disponíveis**:
   - Baixa (128k)
   - Média (192k) 
   - Alta (256k)
   - Muito Alta (320k)
5. **Pasta de Destino**: Clique em "Alterar" para escolher onde salvar

## 📁 Estrutura de Arquivos

```
YouTube-MP3-Downloader/
├── youtube_mp3_downloader_gui.py    # Código principal
├── create_executable.bat            # Script de build para Windows
├── create_executable.sh             # Script de build para macOS
├── build.py                         # Script universal Python
├── README.md                        # Este arquivo
└── dist/                           # Pasta com executável (após build)
    └── YouTube MP3 Downloader      # Executável
```

## 🔧 Solução de Problemas

### Problema: "FFmpeg não encontrado"

#### Windows:
```bash
# Via Chocolatey
choco install ffmpeg -y

# Ou baixar manualmente de ffmpeg.org
# Extrair e adicionar ao PATH do Windows
```

#### macOS:
```bash
# Via Homebrew
brew install ffmpeg

# Se não tiver Homebrew, instale primeiro:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Problema: "Python não encontrado"

#### Windows:
1. Baixe Python de [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação

#### macOS:
```bash
# Via Homebrew (recomendado)
brew install python

# Ou usar o instalador oficial
# Baixar de python.org/downloads
```

### Problema: "Permissão negada" (macOS)

```bash
# Dar permissão de execução
chmod +x "dist/YouTube MP3 Downloader"

# Se ainda não funcionar, tentar:
sudo xattr -rd com.apple.quarantine "dist/YouTube MP3 Downloader"
```

### Problema: Downloads falham

1. Verifique sua conexão com a internet
2. Confirme se a URL está correta
3. Alguns vídeos podem ter restrições regionais
4. Atualize o yt-dlp: `pip install --upgrade yt-dlp`

## 🆕 Diferenças da Versão Multiplataforma

### Melhorias Implementadas:

1. **Detecção Automática do Sistema**: O app se adapta automaticamente ao Windows ou macOS
2. **Caminhos de Download Inteligentes**: 
   - Windows: `C:\Users\[Usuario]\Downloads`
   - macOS: `/Users/[Usuario]/Downloads`
3. **Fontes Específicas por Sistema**:
   - Windows: Consolas
   - macOS: Monaco
4. **Comandos de Instalação Contextuais**: Mostra comandos específicos para cada sistema
5. **Tratamento de Caracteres Especiais**: Melhor compatibilidade com nomes de arquivo
6. **Mensagens de Sistema**: Instruções específicas para cada plataforma

## 🔄 Atualizações

Para manter o aplicativo atualizado:

```bash
# Atualizar yt-dlp (recomendado mensalmente)
pip install --upgrade yt-dlp

# Recriar o executável após atualizações importantes
python3 build.py
```

## ⚠️ Aviso Legal

Este aplicativo é destinado apenas para uso pessoal e educacional. Respeite os direitos autorais e os termos de serviço do YouTube. O usuário é responsável pelo uso adequado da ferramenta.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todos os pré-requisitos estão instalados
2. Consulte a seção "Solução de Problemas"
3. Verifique os logs no aplicativo para mensagens de erro detalhadas
4. Certifique-se de que está usando a versão mais recente do yt-dlp

## 📊 Informações Técnicas

- **Linguagem**: Python 3.7+
- **Interface**: Tkinter (incluído no Python)
- **Download Engine**: yt-dlp
- **Conversão de Áudio**: FFmpeg
- **Empacotamento**: PyInstaller

---

**Criado para uso pessoal - Compatível com Windows e macOS** 🎵