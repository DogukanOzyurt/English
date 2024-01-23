import torch
import tkinter as tk
from tkinter import ttk, scrolledtext
from transformers import AutoModelForCausalLM, AutoTokenizer
from tkinter import messagebox
import random
import csv
from gtts import gTTS
import pygame
from io import BytesIO


class HomePage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.master = master
        master.title("Home")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        label = tk.Label(self, text="Home Page", font=("Arial", 18), bg='black', fg='white')
        label.pack(pady=10)

        # Frame oluştur
        button_frame = tk.Frame(self, bg='black')  # Button frame'in arka plan rengini de siyah yap
        button_frame.pack(pady=300)

        # Butonları ekleyerek yatay olarak ortala
        button_chat = tk.Button(button_frame, text="Chat", command=lambda: switch_frame(ChatPage), width=15, height=3, bg='white', fg='black')
        button_chat.pack(side=tk.LEFT, padx=20)

        button_exercise = tk.Button(button_frame, text="Exercise", command=lambda: switch_frame(ExercisePage), width=15, height=3, bg='white', fg='black')
        button_exercise.pack(side=tk.LEFT, padx=20)

        button_stories = tk.Button(button_frame, text="Stories", command=lambda: switch_frame(StoriesPage), width=15, height=3, bg='white', fg='black')
        button_stories.pack(side=tk.LEFT, padx=20)

        button_listening = tk.Button(button_frame, text="Listening", command=lambda: switch_frame(ListenPage), width=15, height=3, bg='white', fg='black')
        button_listening.pack(side=tk.LEFT, padx=20)

        # Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image1 = self.image1.subsample(1, 1)
        self.label = tk.Label(master, image=self.image1, bg='black')
        self.label.place(anchor="nw", x=10, y=10)


class ListenPage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.master = master
        master.title("Listening")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        # Frame oluştur
        content_frame = tk.Frame(self, bg='black', width=750, height=500)  # Genişliği ve yüksekliği istediğiniz değerlere ayarlayın
        content_frame.pack(expand=True)

        # Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image1 = self.image1.subsample(2, 2)
        self.label = tk.Label(master, image=self.image1, bg='black')
        self.label.place(anchor="nw", x=10, y=10)

        # ListeningApp content here
        self.questions = self.load_questions()
        self.current_question = None

        # Kalın harfli soru cümlesi
        self.question_label = tk.Label(content_frame, text="", wraplength=400, justify="center", font=("Arial", 20, 'bold'), bg='black', fg='white')
        self.question_label.grid(row=1, column=0, pady=20, columnspan=2)  # columnspan ile genişlet

        self.option_labels = []
        for i in range(4):  # 4 seçenek var
            option_label = tk.Label(content_frame, text="", font=("Arial", 15), bg='black', fg='white')
            option_label.grid(row=i + 2, column=0, pady=5, sticky='w', columnspan=2)  # columnspan ile genişlet
            option_label.bind("<Button-1>", lambda event, index=i: self.select_option(index))
            self.option_labels.append(option_label)

        self.submit_button = tk.Button(content_frame, text="Submit", command=self.submit_answer, width=10, height=2, bg='white', fg='black')
        self.submit_button.grid(row=8, column=1, pady=15)

        self.listen_button = tk.Button(content_frame, text="Listen", command=self.listen_question, width=10, height=2, bg='white', fg='black')
        self.listen_button.grid(row=8, column=0, pady=15)

        button_home = tk.Button(content_frame, text="Home", command=lambda: switch_frame(HomePage), width=10, height=2, bg='white', fg='black')
        button_home.grid(row=8, column=2, pady=15)  # columnspan=1 columnspan ile genişlet

        self.load_question()

    def load_question(self):
        self.current_question = random.choice(self.questions)
        self.question_label.config(text=self.current_question['question'])

        # Ayırıcı karakteri "|" olan seçenekleri ayrıştırma
        options = self.current_question['options'].split(', ')

        for i, option in enumerate(options):
            self.option_labels[i].config(text=option, fg="white") #

    def select_option(self, index):
        for i in range(4):
            self.option_labels[i].config(fg="white")
        self.option_labels[index].config(fg="blue")

    def submit_answer(self):
        selected_option = None
        for i in range(4):
            if self.option_labels[i].cget("fg") == "blue":
                selected_option = chr(ord('A') + i)

        if selected_option == self.current_question['answer']:
            messagebox.showinfo("Correct", "Correct answer!")
        else:
            correct_option_text = self.current_question['answer']
            messagebox.showerror("Incorrect", f"Wrong answer. Correct answer is: {correct_option_text}")

        self.load_question()

    def load_questions(self):
        # Soruları bir CSV dosyasından okuma
        with open('listen.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            loaded_questions = list(reader)

        return loaded_questions

    def listen_question(self):
        # Text to speech conversion
        text_to_speak = self.current_question['announcement']
        tts = gTTS(text=text_to_speak, lang='en')

        # Get the speech as an in-memory binary stream
        speech_stream = BytesIO()
        tts.write_to_fp(speech_stream)
        speech_stream.seek(0)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the in-memory binary stream
        pygame.mixer.music.load(speech_stream)

        # Play the audio
        pygame.mixer.music.play()

        
class StoriesPage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.master = master
        master.title("Stories")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        self.stories = self.load_stories()

        for story in self.stories:
            button_story = tk.Button(self, text=story['title'], command=lambda s=story: switch_frame(StoryDetailPage, s),
                                     font=("Arial", 15), fg="black", bg="white")
            button_story.pack(pady=10)

        button_home = tk.Button(self, text="Home", command=lambda: switch_frame(HomePage),
                                font=("Arial", 15), fg="black", bg="white")
        button_home.pack(side=tk.BOTTOM, pady=10)

    def load_stories(self):
        with open('stories.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            loaded_stories = list(reader)
        return loaded_stories
    
    
class StoryDetailPage(tk.Frame):
    def __init__(self, master, switch_frame, story):
        super().__init__(master)
        self.master = master
        master.title(story['title'])

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        #Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image1 = self.image1.subsample(2, 2)
        self.label = tk.Label(master, image=self.image1)
        self.label.place(anchor="nw", x=10, y=10)

        label_title = tk.Label(self, text=story['title'], font=("Arial", 18), fg="white", bg="black")
        label_title.pack(pady=10)

        label_story = tk.Label(self, text=story['story'], wraplength=600, justify="left", font=("Arial", 12),
                               fg="white", bg="black")
        label_story.pack(pady=10)

        button_home = tk.Button(self, text="Home", command=lambda: switch_frame(HomePage),
                                font=("Arial", 15), fg="black", bg="white")
        button_home.pack(side=tk.BOTTOM, pady=10)
      

        
        
class ExercisePage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.master = master
        master.title("Exercise")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        button_grammar = tk.Button(self, text="Grammar", command=lambda: switch_frame(GrammarPage),
                                   font=("Arial", 15), fg="black", bg="white")
        button_grammar.pack(pady=10)

        button_reading = tk.Button(self, text="Reading", command=lambda: switch_frame(ReadingPage),
                                   font=("Arial", 15), fg="black", bg="white")
        button_reading.pack(pady=10)

        button_home = tk.Button(self, text="Home", command=lambda: switch_frame(HomePage),
                                font=("Arial", 15), fg="black", bg="white")
        button_home.pack(pady=10)
        
        
        # Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image2 = self.image1.subsample(2, 2)
        self.label = tk.Label(master, image=self.image2)
        self.label.place(anchor="nw", x=10, y=10)



class ChatPage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.master = master
        master.title("Chat")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        # ChatApp content here
        frame = tk.Frame(self, bg='black')
        frame.pack(expand=True, fill="both", pady=90, padx=105)
        

        # İlk iç çerçeve oluştur
        inner_frame = tk.Frame(frame, bg='black')
        inner_frame.pack(expand=True, fill="both")
        
        #Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image1 = self.image1.subsample(2, 2)
        self.label = tk.Label(master, image=self.image1)
        self.label.place(anchor="nw", x=10, y=10)


        # Mesaj gösterme alanı
        self.chat_display = scrolledtext.ScrolledText(inner_frame, wrap=tk.WORD, width=50, height=20, font=("Arial", 14), bg="black", fg="white")
        self.chat_display.pack(expand=True, fill="both", pady=10)  

        # İkinci iç çerçeve oluştur
        input_frame = tk.Frame(inner_frame,  bg='black')
        input_frame.pack(padx=400, expand=True, fill="both")

        # Giriş kutusu
        self.input_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bg="black", fg="white")
        self.input_entry.pack(pady=10, side=tk.LEFT)  

        # Gönder butonu
        send_button = tk.Button(input_frame, text="Send", command=self.send_message, font=("Arial", 15), fg="black", bg="white")
        send_button.pack(pady=10, side=tk.LEFT)  

        # Enter tuşuna basıldığında da gönderme işlemini yap
        master.bind("<Return>", lambda event: self.send_message())

        # Chatbot modelini yükle
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

        # Chat geçmişi için değişken
        self.chat_history_ids = None

        button_home = tk.Button(self, text="Home", command=lambda: switch_frame(HomePage), font=("Arial", 15), fg="black", bg="white", padx=10)
        button_home.pack(pady=10)

    def receive_user_input(self):
        # Belirli bir süre sonra tekrar kullanıcı girdisi al
        self.master.after(1000, self.receive_user_input)

    def get_chatbot_response(self, user_input, chat_history_ids):
        # Kullanıcının girişini modele uygun formata çevir
        new_user_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')

        # Modelden cevap al
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) \
            if chat_history_ids is not None else new_user_input_ids
        chat_history_ids = self.model.generate(bot_input_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)

        # Cevabı decode et ve döndür
        response = self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response, chat_history_ids

    def send_message(self):
        user_input = self.input_entry.get()
        if user_input:
            # Kullanıcının girdiğini göster
            self.display_message(f"User: {user_input}\n")

            # Burada kullanıcının girdisine uygun bir chatbot cevabı 
            chatbot_response, self.chat_history_ids = self.get_chatbot_response(user_input, self.chat_history_ids)
            self.display_message(f"ChatBot: {chatbot_response}\n")

        # Giriş kutusunu temizle
        self.input_entry.delete(0, tk.END)

    def display_message(self, message):
        # Mesajı göster
        self.chat_display.insert(tk.END, message)
        self.chat_display.yview(tk.END)  # Scroll'u otomatik aşağıya al

class GrammarPage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        master.title("Grammar")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        # Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image1 = self.image1.subsample(2, 2)
        self.label = tk.Label(self, image=self.image1, bg="black")
        self.label.place(anchor="nw", x=5, y=5)

        # GrammarApp content here
        self.questions = self.load_questions()
        self.current_question = None

        self.question_label = tk.Label(self, text="", wraplength=600, justify="center", font=("Arial", 20, 'bold'), fg="white", bg="black")
        self.question_label.pack(pady=20)

        self.option_labels = []
        for i in range(5):
            option_label = tk.Label(self, text="", font=("Arial", 15), fg="white", bg="black")
            option_label.pack(pady=5)
            option_label.bind("<Button-1>", lambda event, index=i: self.select_option(index))
            self.option_labels.append(option_label)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_answer, font=("Arial", 15), fg="black", bg="white")
        self.submit_button.pack(pady=20)

        self.load_question()

        button_home = tk.Button(self, text="Home", command=lambda: switch_frame(HomePage), font=("Arial", 15), fg="black", bg="white")
        button_home.pack(pady=10)

    def load_question(self):
        self.current_question = random.choice(self.questions)
        self.question_label.config(text=self.current_question['question'])
        
        # Ayırıcı karakteri "|" olan seçenekleri ayrıştırma
        options = self.current_question['options'].split('|')
        
        for i, option in enumerate(options):
            self.option_labels[i].config(text=option, fg="white")

    def select_option(self, index):
        for i in range(5):
            self.option_labels[i].config(fg="white")
        self.option_labels[index].config(fg="blue")

    def submit_answer(self):
        selected_option = None
        for i in range(5):
            if self.option_labels[i].cget("fg") == "blue":
                selected_option = chr(ord('A') + i)

        if selected_option == self.current_question['correct_answer']:
            messagebox.showinfo("Correct", "Correct answer!")
        else:
            correct_option_index = ord(self.current_question['correct_answer']) - ord('A')
            correct_option_text = self.current_question['options'].split('|')[correct_option_index]
            messagebox.showerror("Incorrect", f"Wrong answer. Correct answer is: {correct_option_text}")

        self.load_question()

    def load_questions(self):
        # Soruları bir CSV dosyasından okuma
        with open('questions2.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            loaded_questions = list(reader)

        return loaded_questions



class ReadingPage(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        master.title("Reading")

        # Arka plan rengini siyah olarak ayarla
        self.configure(bg='black')

        # Image
        self.image1 = tk.PhotoImage(file="Chat.png")
        self.image1 = self.image1.subsample(2, 2)
        self.label = tk.Label(self, image=self.image1, bg="black")
        self.label.place(anchor="nw", x=10, y=10)

        # ReadingApp content here
        self.questions = self.load_questions()
        self.current_question = None

        self.question_label = tk.Label(self, text="", wraplength=600, justify="center", font=("Arial", 14, 'bold'), fg="white", bg="black")
        self.question_label.pack(pady=20)

        self.option_labels = []
        for i in range(5):
            option_label = tk.Label(self, text="", font=("Arial", 11), fg="white", bg="black")
            option_label.pack(pady=5)
            option_label.bind("<Button-1>", lambda event, index=i: self.select_option(index))
            self.option_labels.append(option_label)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_answer, font=("Arial", 15), fg="black", bg="white")
        self.submit_button.pack(pady=20)

        self.load_question()

        button_home = tk.Button(self, text="Home", command=lambda: switch_frame(HomePage), font=("Arial", 15), fg="black", bg="white")
        button_home.pack(pady=10)

    def load_question(self):
        self.current_question = random.choice(self.questions)
        self.question_label.config(text=self.current_question['question'])

        # Ayırıcı karakteri "|" olan seçenekleri ayrıştırma
        options = self.current_question['options'].split('|')

        for i, option in enumerate(options):
            self.option_labels[i].config(text=option, fg="white")

    def select_option(self, index):
        for i in range(5):
            self.option_labels[i].config(fg="white")
        self.option_labels[index].config(fg="blue")

    def submit_answer(self):
        selected_option = None
        for i in range(5):
            if self.option_labels[i].cget("fg") == "blue":
                selected_option = chr(ord('A') + i)

        if selected_option == self.current_question['correct_answer']:
            messagebox.showinfo("Correct", "Correct answer!")
        else:
            correct_option_index = ord(self.current_question['correct_answer']) - ord('A')
            correct_option_text = self.current_question['options'].split('|')[correct_option_index]
            messagebox.showerror("Incorrect", f"Wrong answer. Correct answer is: {correct_option_text}")

        self.load_question()

    def load_questions(self):
        # Soruları bir CSV dosyasından okuma
        with open('questions.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            loaded_questions = list(reader)

        return loaded_questions



class ChatApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # ChatApp content here

        button_home = tk.Button(self, text="Home", command=lambda: master.master.switch_frame(HomePage))
        button_home.pack(pady=10)


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Project")
        self.geometry("800x600")
        self.current_frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, self.switch_frame, *args)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
