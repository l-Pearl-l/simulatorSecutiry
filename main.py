import tkinter as tk
from tkinter import ttk
from practice import network, firewall, attack
from theory import theory

class SecurityTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажёр по сетевой безопасности")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        self.setup_styles()
        self.show_mode_selection()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 11))
        self.style.configure('Title.TLabel', font=('Arial', 20, 'bold'), foreground='#3498db')
        self.style.configure('Mode.TButton', font=('Arial', 14, 'bold'), padding=15)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_mode_selection(self):
        """Показывает выбор между теорией и практикой"""
        self.clear_screen()

        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Заголовок
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=40)

        title_label = ttk.Label(title_frame, 
                               text="🛡️ Тренажёр Кибербезопасности", 
                               style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(title_frame, 
                                  text="Network Security Trainer", 
                                  font=('Arial', 14),
                                  foreground='#bdc3c7')
        subtitle_label.pack(pady=10)

        # Фрейм для кнопок выбора режима
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(pady=50)

        # Кнопка Теории
        theory_btn = ttk.Button(mode_frame,
                               text="📚 ТЕОРИЯ\nИзучение основ безопасности",
                               command=self.start_theory_mode,
                               style='Mode.TButton',
                               width=30,)
        theory_btn.pack(pady=20)

        # Кнопка Практики  
        practice_btn = ttk.Button(mode_frame,
                                 text="🛠️ ПРАКТИКА\nСимуляция сетевых атак",
                                 command=self.start_practice_mode,
                                 style='Mode.TButton',
                                 width=25)
        practice_btn.pack(pady=20)

        # Описание режимов
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(pady=30)

        theory_desc = ttk.Label(desc_frame,
                               text="📚 Теория: Изучите основы кибербезопасности, ответьте на вопросы сценариев\n"
                                    "и проверьте свои знания в различных ситуациях",
                               font=('Arial', 10),
                               foreground='#ecf0f1',
                               justify='center')
        theory_desc.pack(pady=5)

        practice_desc = ttk.Label(desc_frame,
                                 text="🛠️ Практика: Настройте сеть, фаерволлы и защититесь от реальных атак\n"
                                      "в интерактивной симуляции",
                                 font=('Arial', 10),
                                 foreground='#ecf0f1',
                                 justify='center')
        practice_desc.pack(pady=5)
    
    def start_theory_mode(self):
        """Запускает режим теории"""
        self.clear_screen()
        
        # Создаем модуль теории
        self.theory_module = TheoryModule(self.root)
        
        # Добавляем кнопку возврата в главное меню
        back_frame = ttk.Frame(self.root)
        back_frame.pack(side='bottom', pady=10)
        
        back_btn = ttk.Button(back_frame,
                            text="🔙 Назад в главное меню",
                            command=self.show_mode_selection,
                            width=30)
        back_btn.pack()
        
        # Помечаем кнопку возврата специальным атрибутом
        back_frame.back_button_marker = True
    
    def start_practice_mode(self):
        """Запускает режим практики"""
        self.clear_screen()
        
        # Создаем модули практики
        self.network_module = network.NetworkModule()
        self.firewall_module = firewall.FirewallModule()
        self.attack_module = attack.AttackModule()
        
        # Связываем модули между собой
        self.setup_module_connections()
        self.setup_practice_gui()
    
    def setup_module_connections(self):
        """Связывает модули для взаимодействия"""
        self.attack_module.set_firewall_module(self.firewall_module)
        self.attack_module.set_network_module(self.network_module)
        self.firewall_module.set_network_module(self.network_module)
        self.network_module.set_firewall_module(self.firewall_module)
    
    def setup_practice_gui(self):
        """Настраивает GUI для практического режима"""
        
        # Верхняя панель с кнопкой возврата
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        back_btn = ttk.Button(top_frame,
                             text="🔙 Назад в главное меню",
                             command=self.show_mode_selection)
        back_btn.pack(side='left')
        
        title_label = ttk.Label(top_frame,
                               text="🛠️ ПРАКТИЧЕСКИЙ РЕЖИМ - СИМУЛЯЦИЯ СЕТЕВОЙ БЕЗОПАСНОСТИ",
                               font=('Arial', 12, 'bold'),
                               foreground='#3498db')
        title_label.pack(side='left', padx=20)

        # Создаем вкладки для практических модулей
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Добавляем вкладки из модулей
        self.notebook.add(self.network_module.get_frame(self.notebook), text="🌐 Сеть")
        self.notebook.add(self.firewall_module.get_frame(self.notebook), text="🛡️ Фаерволлы")
        self.notebook.add(self.attack_module.get_frame(self.notebook), text="⚡ Атаки")

# Создаем адаптер для твоего модуля теории
class TheoryModule:
    def __init__(self, root):
        # Используем твой существующий класс CyberSecurityTrainer
        # но адаптируем его для работы в рамках нашей системы
        self.trainer = theory.Theory(root)
        
        # Переопределяем метод show_main_menu чтобы он не очищал экран полностью
        original_show_main_menu = self.trainer.show_main_menu
        
        def adapted_show_main_menu():
            # Не очищаем весь экран, только содержимое тренажера
            for widget in self.trainer.root.winfo_children():
                if hasattr(widget, '_name') and widget._name:  # Оставляем верхнюю панель
                    continue
                widget.destroy()
            # Вызываем оригинальный метод
            original_show_main_menu()
        
        self.trainer.show_main_menu = adapted_show_main_menu
        self.trainer.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityTrainer(root)
    root.mainloop()