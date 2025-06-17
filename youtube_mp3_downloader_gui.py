#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import threading
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "tk"], check=True)
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        self.root.resizable(False, False)
        self.root.geometry("600x500")
        
        # Configurar ícone caso esteja empacotado como executável
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            # self.root.iconbitmap(os.path.join(application_path, 'icon.ico'))
        except:
            pass
        
        # Variáveis
        self.download_dir = os.path.join(str(Path.home()), "Downloads")
        self.download_in_progress = False
        self.quality_var = tk.StringVar(value="320k")
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto para download")
        self.progress_var = tk.DoubleVar(value=0)
        self.download_type = tk.StringVar(value="single")
        self.file_path = tk.StringVar()
        
        # Configuração da interface
        self.setup_ui()
        
        # Verificar requisitos de início
        self.root.after(500, self.check_requirements_async)

    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo e título
        title_label = ttk.Label(self.main_frame, text="YouTube MP3 Downloader", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Frame para seleção do tipo de download
        self.type_frame = ttk.LabelFrame(self.main_frame, text="Tipo de Download", padding="10")
        self.type_frame.pack(fill=tk.X, pady=(0, 10))
        
        single_radio = ttk.Radiobutton(self.type_frame, text="Vídeo único", variable=self.download_type, value="single")
        single_radio.grid(row=0, column=0, padx=10, sticky=tk.W)
        
        playlist_radio = ttk.Radiobutton(self.type_frame, text="Playlist completa", variable=self.download_type, value="playlist")
        playlist_radio.grid(row=0, column=1, padx=10, sticky=tk.W)
        
        batch_radio = ttk.Radiobutton(self.type_frame, text="Lista de URLs de um arquivo", variable=self.download_type, value="batch")
        batch_radio.grid(row=0, column=2, padx=10, sticky=tk.W)
        
        # Criar os dois frames (para url e batch) mas inicialmente não empacotar nenhum
        # URL input frame
        self.url_frame = ttk.Frame(self.main_frame)
        url_label = ttk.Label(self.url_frame, text="URL do YouTube:")
        url_label.pack(anchor=tk.W)
        url_entry = ttk.Entry(self.url_frame, textvariable=self.url_var, width=70)
        url_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Frame para arquivo de lote (batch mode)
        self.batch_frame = ttk.Frame(self.main_frame)
        file_label = ttk.Label(self.batch_frame, text="Arquivo com URLs (uma por linha):")
        file_label.pack(anchor=tk.W)
        file_entry_frame = ttk.Frame(self.batch_frame)
        file_entry_frame.pack(fill=tk.X, pady=(5, 0))
        file_entry = ttk.Entry(file_entry_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        browse_button = ttk.Button(file_entry_frame, text="Procurar", command=self.browse_file)
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Qualidade de áudio frame - será usado como referência de posicionamento
        self.quality_frame = ttk.LabelFrame(self.main_frame, text="Qualidade do Áudio", padding="10")
        self.quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        quality_128 = ttk.Radiobutton(self.quality_frame, text="Baixa (128k)", variable=self.quality_var, value="128k")
        quality_128.grid(row=0, column=0, padx=10, sticky=tk.W)
        
        quality_192 = ttk.Radiobutton(self.quality_frame, text="Média (192k)", variable=self.quality_var, value="192k")
        quality_192.grid(row=0, column=1, padx=10, sticky=tk.W)
        
        quality_256 = ttk.Radiobutton(self.quality_frame, text="Alta (256k)", variable=self.quality_var, value="256k")
        quality_256.grid(row=0, column=2, padx=10, sticky=tk.W)
        
        quality_320 = ttk.Radiobutton(self.quality_frame, text="Muito Alta (320k)", variable=self.quality_var, value="320k")
        quality_320.grid(row=0, column=3, padx=10, sticky=tk.W)
        
        # Pasta de destino
        dest_frame = ttk.Frame(self.main_frame)
        dest_frame.pack(fill=tk.X, pady=(0, 10))
        
        dest_top_frame = ttk.Frame(dest_frame)
        dest_top_frame.pack(fill=tk.X)
        
        dest_label_text = ttk.Label(dest_top_frame, text="Pasta de destino:")
        dest_label_text.pack(side=tk.LEFT, anchor=tk.W)
        
        dest_button = ttk.Button(dest_top_frame, text="Alterar", command=self.choose_download_dir)
        dest_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.dest_path_label = ttk.Label(dest_frame, text=self.download_dir, foreground="blue")
        self.dest_path_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Botão de download
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.download_button = ttk.Button(button_frame, text="Baixar MP3", command=self.start_download)
        self.download_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Barra de progresso
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, mode="indeterminate")
        self.progress_bar.pack(fill=tk.X, expand=True)
        
        # Status
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.pack(anchor=tk.W)
        
        # Log
        log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10, font=("Consolas", 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Rodapé com links
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, pady=(0, 10))
        
        credits_label = ttk.Label(footer_frame, text="Criado para uso pessoal", foreground="gray")
        credits_label.pack(side=tk.RIGHT, padx=20)
        
        # Bind de eventos
        self.download_type.trace_add("write", self.on_download_type_change)
        
        # Inicializar estado dos frames de entrada
        self.on_download_type_change()

    def choose_download_dir(self):
        """Abre diálogo para escolher a pasta de download"""
        new_dir = filedialog.askdirectory(
            title="Selecione a pasta para salvar os arquivos MP3",
            initialdir=self.download_dir
        )
        if new_dir:
            self.download_dir = new_dir
            self.dest_path_label.config(text=self.download_dir)
            self.log(f"Pasta de destino alterada para: {self.download_dir}")

    def on_download_type_change(self, *args):
        # Remover os dois frames se estiverem visíveis
        try:
            self.url_frame.pack_forget()
        except:
            pass
        
        try:
            self.batch_frame.pack_forget()
        except:
            pass
        
        # Mostrar o frame adequado baseado na seleção
        if self.download_type.get() == "batch":
            # Usar o widget quality_frame como referência para posicionamento
            self.batch_frame.pack(fill=tk.X, pady=(0, 10), before=self.quality_frame)
        else:
            # Usar o widget quality_frame como referência para posicionamento
            self.url_frame.pack(fill=tk.X, pady=(0, 10), before=self.quality_frame)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo com URLs",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)

    def log(self, message):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        self.log_text.insert(tk.END, timestamp + message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def check_requirements_async(self):
        thread = threading.Thread(target=self.check_requirements)
        thread.daemon = True
        thread.start()

    def check_requirements(self):
        self.status_var.set("Verificando requisitos...")
        self.progress_bar.start(10)
        self.download_button.config(state=tk.DISABLED)
        
        self.log("Verificando requisitos do sistema...")
        
        # Verificar yt-dlp
        try:
            subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            self.log("✓ yt-dlp encontrado!")
        except (subprocess.SubprocessError, FileNotFoundError):
            self.log("✗ yt-dlp não encontrado. Instalando...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                self.log("✓ yt-dlp instalado com sucesso!")
            except subprocess.SubprocessError as e:
                self.log(f"✗ Falha ao instalar yt-dlp: {e}")
                messagebox.showerror("Erro", "Não foi possível instalar yt-dlp. Tente instalar manualmente com: pip install yt-dlp")
        
        # Verificar FFmpeg
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            self.log("✓ FFmpeg encontrado!")
        except (subprocess.SubprocessError, FileNotFoundError):
            self.log("⚠️ FFmpeg não encontrado! A conversão para MP3 pode falhar.")
            if platform.system() == "Windows":
                self.log("Recomendado: Instale o FFmpeg via Chocolatey com: choco install ffmpeg -y")
            elif platform.system() == "Darwin":
                self.log("Recomendado: Instale o FFmpeg via Homebrew com: brew install ffmpeg")
            else:
                self.log("Recomendado: Instale o FFmpeg via gerenciador de pacotes: sudo apt install ffmpeg")
            
            result = messagebox.askokcancel("Aviso", 
                "FFmpeg não foi encontrado no sistema. Isso pode causar falhas na conversão para MP3.\n\n"
                "Deseja continuar mesmo assim? (Recomendamos instalar o FFmpeg para melhor funcionamento)")
            
            if not result:
                self.root.quit()
                return
        
        self.log("Verificação de requisitos concluída!")
        self.progress_bar.stop()
        self.progress_var.set(0)
        self.status_var.set("Pronto para download")
        self.download_button.config(state=tk.NORMAL)

    def start_download(self):
        # Validar entrada
        download_type = self.download_type.get()
        
        if download_type == "batch":
            file_path = self.file_path.get().strip()
            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("Erro", "Por favor, selecione um arquivo de texto válido com URLs")
                return
        else:
            url = self.url_var.get().strip()
            if not url or not (url.startswith("http://") or url.startswith("https://")):
                messagebox.showerror("Erro", "Por favor, insira uma URL válida do YouTube")
                return
        
        # Validar pasta de destino
        if not os.path.exists(self.download_dir):
            try:
                os.makedirs(self.download_dir)
                self.log(f"✓ Pasta de destino criada: {self.download_dir}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível criar a pasta de destino:\n{e}")
                return
        
        # Evitar downloads múltiplos
        if self.download_in_progress:
            return
        
        # Iniciar thread de download
        self.download_in_progress = True
        self.progress_bar.start(10)
        self.download_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.perform_download)
        thread.daemon = True
        thread.start()

    def perform_download(self):
        try:
            download_type = self.download_type.get()
            quality = self.quality_var.get()
            
            if download_type == "batch":
                self.status_var.set("Baixando vários vídeos do arquivo...")
                self.log(f"Iniciando download em lote do arquivo: {self.file_path.get()}")
                self.download_from_file(self.file_path.get(), self.download_dir, quality)
            else:
                url = self.url_var.get().strip()
                is_playlist = (download_type == "playlist")
                
                if is_playlist:
                    self.status_var.set("Baixando playlist...")
                    self.log(f"Iniciando download da playlist: {url}")
                else:
                    self.status_var.set("Baixando vídeo...")
                    self.log(f"Iniciando download do vídeo: {url}")
                
                self.download_video(url, self.download_dir, quality, is_playlist)
            
            self.status_var.set("Download concluído com sucesso!")
            messagebox.showinfo("Sucesso", f"Download concluído!\nArquivos salvos em: {self.download_dir}")
            
        except Exception as e:
            self.status_var.set(f"Erro: {e}")
            self.log(f"❌ Erro durante o download: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o download:\n{e}")
        
        finally:
            self.progress_bar.stop()
            self.progress_var.set(0)
            self.download_button.config(state=tk.NORMAL)
            self.download_in_progress = False

    def download_video(self, url, output_dir, quality, is_playlist=False):
        temp_dir = tempfile.mkdtemp()
        output_pattern = os.path.join(temp_dir, "%(title)s.%(ext)s")
        
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", quality]
        if is_playlist:
            cmd.append("--yes-playlist")
        cmd.extend(["-o", output_pattern, url])
        
        self.log(f"Qualidade de áudio: {quality}")
        self.log("Iniciando download e conversão...")
        
        try:
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Ler saída linha por linha
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.log(line)
            
            process.wait()
            
            if process.returncode != 0:
                raise Exception(f"yt-dlp saiu com código de erro {process.returncode}")
            
            # Mover arquivos MP3 para o diretório de saída
            found_files = False
            for file in os.listdir(temp_dir):
                if file.endswith(".mp3"):
                    found_files = True
                    src = os.path.join(temp_dir, file)
                    dst = os.path.join(output_dir, file)
                    shutil.move(src, dst)
                    self.log(f"✓ Arquivo salvo: {dst}")
            
            if not found_files:
                self.log("⚠️ Nenhum arquivo MP3 foi gerado. Verifique se o FFmpeg está instalado corretamente.")
            
            # Limpar diretório temporário
            shutil.rmtree(temp_dir)
            return True
            
        except Exception as e:
            self.log(f"✗ Erro ao baixar: {e}")
            # Tentar limpar diretório temporário em caso de erro
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            raise

    def download_from_file(self, file_path, output_dir, quality):
        try:
            with open(file_path, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
            
            if not urls:
                self.log("✗ O arquivo está vazio ou não contém URLs válidas.")
                raise Exception("O arquivo não contém URLs válidas")
            
            self.log(f"Encontradas {len(urls)} URLs para baixar.")
            
            success_count = 0
            for i, url in enumerate(urls, 1):
                self.log(f"\n[{i}/{len(urls)}] Processando URL: {url}")
                self.status_var.set(f"Baixando {i}/{len(urls)}: {url[:30]}...")
                if self.download_video(url, output_dir, quality):
                    success_count += 1
            
            self.log(f"\n✓ Download concluído: {success_count}/{len(urls)} arquivos baixados com sucesso.")
            return True
            
        except Exception as e:
            self.log(f"✗ Erro ao processar arquivo: {e}")
            raise

def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()