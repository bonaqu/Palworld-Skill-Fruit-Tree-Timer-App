import pygame
from tkinter import Tk, Label, Button, Frame, PhotoImage, Canvas, Toplevel, messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import os
import webbrowser
import keyboard

class AboutMeWindow:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Обо мне")
        self.window.geometry("256x256")
        self.window.resizable(False, False)

        # Черный фон
        self.canvas = Canvas(self.window, bg="black", width=256, height=256)
        self.canvas.pack()

        # Кнопка для поддержки автора
        support_button = Button(self.window, text="Поддержка автора (QIWI)", bg="black", fg="yellow", command=self.open_support_link)
        support_button.place(relx=0.5, y=20, anchor="center")
        
        # Логотип
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((256, 256), Image.NEAREST)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.canvas.create_image(128, 128, image=self.logo_photo)

        # Надпись
        self.canvas.create_text(128, 45, text="github.com/bonaqu", fill="white")

        # Версия приложения
        self.canvas.create_text(128, 240, text="Версия 1.0.0.3", fill="white")

    def open_support_link(self):
        webbrowser.open("https://qiwi.com/n/BONAQU")

class PalworldSkillFruitTreeTimerApp:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)  # Убираем рамку окна и заголовок
        self.root.geometry("318x159")
        self.root.resizable(False, False)

        # Добавляем возможность перемещения окна по экрану
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_motion)

        self.timer_running = False
        self.sound_played = False  # Флаг для отслеживания воспроизведения звука окончания таймера

        self.create_start_button()  # Создаем только одну кнопку

        self.background_label = Label(self.root)
        self.background_label.pack(fill="both", expand=True)

        self.tree_image_path = os.path.join(os.getcwd(), "tree.png")
        if os.path.exists(self.tree_image_path):
            self.tree_image = PhotoImage(file=self.tree_image_path)
            self.background_label.configure(image=self.tree_image)

        self.timer_delay = timedelta(hours=3, minutes=12)
        self.last_collection_time = None

        pygame.init()
        self.start_sound = pygame.mixer.Sound("start_sound.wav")
        self.end_sound = pygame.mixer.Sound("end_sound.wav")

        self.update_timer()

        keyboard.add_hotkey("ctrl+shift+x", self.fast_forward_timer)

        self.create_close_button()  # Создаем кнопку закрытия окна
        self.create_about_button()  # Создаем кнопку "Обо мне"

        self.root.mainloop()

    def create_close_button(self):
        close_button_image = PhotoImage(file="close_button.png")
        close_button = Button(self.root, image=close_button_image, bg="black", bd=0, command=self.close_app, highlightthickness=0)
        close_button.image = close_button_image
        close_button.place(x=300, y=0)

    def create_start_button(self):
        self.start_button_text = "Ожидание нового урожая!"
        self.start_button = Button(self.root, text=self.start_button_text, bg="black", fg="yellow", command=self.toggle_timer)
        self.start_button.pack(fill="x", side="bottom")

    def update_button_text(self):
        if self.timer_running:
            self.start_button_text = self.calculate_time_left()
        else:
            self.start_button_text = "Ожидание нового урожая!"
        self.start_button.config(text=self.start_button_text)

    def calculate_time_left(self):
        if self.last_collection_time:
            current_time = datetime.now()
            next_collection_time = self.last_collection_time + self.timer_delay
            time_until_collection = next_collection_time - current_time

            if time_until_collection <= timedelta(0):
                if not self.sound_played:
                    self.end_sound.play()
                    self.sound_played = True
                return "Плоды скиллов вырастут через: 00:00:00"
            else:
                self.sound_played = False  # Сброс флага, чтобы в следующий раз звук снова воспроизводился
                formatted_time = "{:02}:{:02}:{:02}".format(
                    time_until_collection.seconds // 3600,
                    (time_until_collection.seconds // 60) % 60,
                    time_until_collection.seconds % 60
                )
                return f"Плоды скиллов вырастут через: {formatted_time}"
        return ""

    def start_timer(self):
        self.last_collection_time = datetime.now()
        self.timer_running = True
        self.update_timer()
        self.update_button_text()
        self.start_sound.play()

    def stop_timer(self):
        self.timer_running = False
        self.update_button_text()

    def toggle_timer(self):
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def fast_forward_timer(self):
        if self.timer_running:
            self.last_collection_time -= timedelta(hours=3, minutes=11, seconds=55)
            self.update_button_text()

    def update_timer(self):
        if self.last_collection_time and self.timer_running:
            self.update_button_text()

        self.root.after(1000, self.update_timer)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def close_app(self):
        self.root.destroy()

    def create_about_button(self):
        about_button_image = PhotoImage(file="question_button.png")
        about_button = Button(self.root, image=about_button_image, bg="black", bd=0, command=self.show_about_window, highlightthickness=0)
        about_button.image = about_button_image
        about_button.place(x=0, y=0)

    def show_about_window(self):
        if not hasattr(self, 'about_me_window') or not self.about_me_window.window.winfo_exists():
            self.about_me_window = AboutMeWindow()
            self.about_me_window.window.lift(self.root)



if __name__ == "__main__":
    app = PalworldSkillFruitTreeTimerApp()
