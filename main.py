import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
from tqdm import tqdm
from threading import Thread

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Downloader")
        self.master.geometry("350x520")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TLabel", background="#ffffff", foreground="#000000")
        self.style.configure("TButton", background="#2ecc71", foreground="#000000")

        self.frame = ttk.Frame(master)
        self.frame.pack(pady=10)

        self.url_label = ttk.Label(self.frame, text="YT Downloder", font=("Arial", 25) )
        self.url_label.grid(row=0, column=0, pady=15, padx=15)

        self.url_label = ttk.Label(self.frame, text="Enter YouTube URL:")
        self.url_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        self.url_entry = ttk.Entry(self.frame, width=50)
        self.url_entry.grid(row=2, column=0, pady=5, padx=10)

        self.quality_label = ttk.Label(self.frame, text="Select Video Quality:")
        self.quality_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        self.quality_combobox = ttk.Combobox(self.frame, values=["144p", "240p", "360p", "480p", "720p", "1080p"])
        self.quality_combobox.set("720p")
        self.quality_combobox.grid(row=4, column=0, pady=5, padx=10)

        self.location_button = ttk.Button(self.frame, text="Select Download Location", command=self.select_location)
        self.location_button.grid(row=5, column=0, pady=10, padx=10)

        self.download_button = ttk.Button(self.frame, text="Download", command=self.download_video)
        self.download_button.grid(row=6, column=0, pady=20, padx=10)

        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=7, column=0, pady=10, padx=10)

        self.pause_button = ttk.Button(self.frame, text="Pause", state="disabled", command=self.pause_download)
        self.pause_button.grid(row=8, column=0, pady=5, padx=10, sticky="w")

        self.play_button = ttk.Button(self.frame, text="Play", state="disabled", command=self.resume_download)
        self.play_button.grid(row=8, column=0, pady=5, padx=10)

        self.cancel_button = ttk.Button(self.frame, text="Cancel", state="disabled", command=self.cancel_download)
        self.cancel_button.grid(row=9, column=0, pady=5, padx=10, sticky="w")

        self.regenerate_button = ttk.Button(self.frame, text="Regenerate Download", command=self.regenerate_download)
        self.regenerate_button.grid(row=10, column=0, pady=5, padx=10, sticky="w")

        self.status_label = ttk.Label(self.frame, text="")
        self.status_label.grid(row=11, column=0, pady=10, padx=10)

        self.download_thread = None
        self.download_location = ""

    def select_location(self):
        self.download_location = filedialog.askdirectory()
        if self.download_location:
            self.status_label.config(text=f"Download location: {self.download_location}")

    def download_video(self):
        try:
            url = self.url_entry.get()
            quality = self.quality_combobox.get()
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension='mp4', res=quality).first()

            self.download_thread = Thread(target=self.download_thread_worker, args=(stream,))
            self.download_thread.start()

        except Exception as e:
            self.status_label.config(text="Error: " + str(e))

    def reset_ui(self):
        self.url_entry.delete(0, tk.END)
        self.quality_combobox.set("720p")
        self.progress_bar["value"] = 0
        self.status_label.config(text="")
        self.pause_button["state"] = "disabled"
        self.play_button["state"] = "disabled"
        self.cancel_button["state"] = "disabled"

    def regenerate_download(self):
        self.reset_ui()
        self.download_thread = None
        self.download_location = ""

        # ... (existing code)

    def cancel_download(self):
        if self.download_thread:
            self.download_thread.terminate()
            self.reset_ui()
            self.status_label.config(text="Download Canceled")

    def download_thread_worker(self, stream):
        self.progress_bar["value"] = 0
        self.pause_button["state"] = "normal"
        self.cancel_button["state"] = "normal"

        with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading", ncols=80) as progress_bar:
            try:
                stream.download(output_path=self.download_location)
            except Exception as e:
                self.status_label.config(text="Error: " + str(e))
            finally:
                self.progress_bar["value"] = 100
                self.pause_button["state"] = "disabled"
                self.play_button["state"] = "disabled"
                self.cancel_button["state"] = "disabled"
                self.status_label.config(text="Download Complete!")

    def pause_download(self):
        self.download_thread.suspend()
        self.pause_button["state"] = "disabled"
        self.play_button["state"] = "normal"

    def resume_download(self):
        self.download_thread.resume()
        self.pause_button["state"] = "normal"
        self.play_button["state"] = "disabled"

    def cancel_download(self):
        self.download_thread.terminate()
        self.pause_button["state"] = "disabled"
        self.play_button["state"] = "disabled"
        self.cancel_button["state"] = "disabled"
        self.status_label.config(text="Download Canceled")

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
