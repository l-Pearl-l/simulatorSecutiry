import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw
import os

class Theory:
    def __init__(self, root):
        self.root = root
        self.user_score = 0
        self.max_score = 100
        self.current_scenario = None
        self.user_choices = []
        self.images = {}

        self.setup_styles()
        self.load_images()
        self.show_main_menu()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 11))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#3498db')
        self.style.configure('Score.TLabel', font=('Arial', 12, 'bold'), foreground='#f39c12')
        self.style.configure('Game.TButton', font=('Arial', 10), padding=10)
        self.style.map('Game.TButton',
                      background=[('active', '#2980b9'), ('pressed', '#21618c')],
                      foreground=[('active', 'white')])

    def load_images(self):
        """Загружаем реальные изображения из папки images"""
        try:
            if not os.path.exists('images'):
                os.makedirs('images')
                print("Создана папка 'images'. Добавьте туда ваши изображения.")
                return
            
            # Список всех необходимых изображений
            image_keys = [
                'prevention_1', 'prevention_2', 'prevention_3',
                'detection_1', 'detection_2', 'detection_3', 
                'response_1', 'response_2', 'response_3',
                'logfile_1', 'logfile_2', 'logfile_3', 'logfile_4', 
                'logfile_5', 'logfile_6', 'logfile_7'
            ]
            
            # Поддерживаемые форматы
            supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
            
            for key in image_keys:
                image_loaded = False
                for format in supported_formats:
                    image_path = os.path.join('images', f"{key}{format}")
                    if os.path.exists(image_path):
                        try:
                            img = Image.open(image_path)
                            img = img.resize((350, 200), Image.Resampling.LANCZOS)
                            self.images[key] = ImageTk.PhotoImage(img)
                            image_loaded = True
                            break
                        except Exception as e:
                            print(f"Ошибка загрузки {image_path}: {e}")
                
                # Если изображение не найдено, создаем placeholder
                if not image_loaded:
                    print(f"Предупреждение: {key} не найден в папке images")
                    img = Image.new('RGB', (350, 200), color='#34495e')
                    d = ImageDraw.Draw(img)
                    d.rectangle([10, 10, 340, 190], outline='#3498db', width=2)
                    d.text((100, 80), f"Изображение: {key}", fill='white')
                    d.text((120, 110), "Добавьте картинку", fill='#bdc3c7')
                    self.images[key] = ImageTk.PhotoImage(img)
                    
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")

    def clear_screen(self):
        # Сохраняем кнопку возврата если она есть
        back_button = None
        for widget in self.root.winfo_children():
            if hasattr(widget, 'back_button_marker'):  # Помечаем кнопку возврата
                back_button = widget
                continue
            widget.destroy()
        
        # Если нашли кнопку возврата, возвращаем ее на экран
        if back_button:
            back_button.pack(side='bottom', pady=10)

    def show_main_menu(self):
        self.clear_screen()

        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)

        title_label = ttk.Label(header_frame, text="📚 ТЕОРЕТИЧЕСКИЙ МОДУЛЬ", style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(header_frame, text="Изучение основ кибербезопасности", font=('Arial', 12),
                                  foreground='#bdc3c7')
        subtitle_label.pack(pady=5)

        score_frame = ttk.Frame(self.root)
        score_frame.pack(pady=10)

        score_label = ttk.Label(score_frame, text=f"🏆 Текущий счет: {self.user_score}/100", style='Score.TLabel')
        score_label.pack()

        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(pady=30)

        scenarios = [
            ("🛡️ Предотвращение атак", self.start_prevention_scenario),
            ("🔍 Обнаружение вторжений", self.start_detection_scenario),
            ("🚨 Реакция на инциденты", self.start_response_scenario),
            ("📝 Работа с логами", self.start_logfile_scenario),
            ("📊 Статистика обучения", self.show_statistics),
        ]

        for text, command in scenarios:
            btn = ttk.Button(menu_frame, text=text, command=command, style='Game.TButton', width=25)
            btn.pack(pady=8)

    def create_question_frame(self, question, options, correct_answer, hints, scenario_info="", image_key=None):
        self.clear_screen()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='x', pady=10)

        text_frame = ttk.Frame(top_frame)
        text_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))

        if scenario_info:
            info_label = ttk.Label(text_frame, text=scenario_info, font=('Arial', 10, 'italic', 'bold'), 
                                foreground='#e74c3c', wraplength=500)
            info_label.pack(anchor='w', pady=(0, 15))

        question_label = ttk.Label(text_frame, text=question, font=('Arial', 12, 'bold'), 
                                wraplength=500, justify='left')
        question_label.pack(anchor='w', pady=(0, 20))

        if image_key and image_key in self.images:
            image_frame = ttk.Frame(top_frame)
            image_frame.pack(side='right', padx=(20, 0))
            
            image_label = ttk.Label(image_frame, image=self.images[image_key])
            image_label.pack(padx=10, pady=10)

        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill='x', pady=20)

        # Инициализируем переменную для хранения выбора
        self.selected_option = tk.StringVar(value="")

        for i, option in enumerate(options, 1):
            option_frame = ttk.Frame(options_frame)
            option_frame.pack(fill='x', pady=8)
            
            # Используем обычный tk.Radiobutton вместо ttk.Radiobutton для поддержки wraplength
            rb = tk.Radiobutton(option_frame, 
                            text=f"{i}. {option}",
                            variable=self.selected_option,
                            value=option,
                            wraplength=700,
                            bg='#2c3e50',
                            fg='white',
                            selectcolor='#34495e',
                            activebackground='#34495e',
                            activeforeground='white',
                            font=('Arial', 10),
                            justify='left')
            rb.pack(anchor='w')

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        submit_btn = ttk.Button(button_frame, text="✅ Подтвердить выбор",
                            command=lambda: self.check_answer(correct_answer, hints),
                            style='Game.TButton')
        submit_btn.pack(side='left', padx=10)

        back_btn = ttk.Button(button_frame, text="🔙 Назад",
                            command=self.show_main_menu,
                            style='Game.TButton')
        back_btn.pack(side='left', padx=10)

    def check_answer(self, correct_answer, hints):
        if not self.selected_option.get():
            messagebox.showwarning("Внимание", "Пожалуйста, выберите вариант ответа")
            return

        selected = self.selected_option.get()
        self.user_choices.append(selected)

        if selected == correct_answer:
            self.user_score += 10
            self.show_feedback("✅ Правильно!", "Ваш выбор верный. Продолжайте в том же духе!", "info")
        else:
            hint = hints.get(selected, "Подумайте о последствиях этого выбора для безопасности сети.")
            self.show_feedback("⚠️ Неверный выбор", f"{hint}\n\nПравильный ответ: {correct_answer}", "warning")

    def show_feedback(self, title, message, message_type):
        if message_type == "info":
            messagebox.showinfo(title, message)
        else:
            messagebox.showwarning(title, message)

        if hasattr(self, 'current_question_index'):
            self.current_question_index += 1
            if self.current_question_index < len(self.scenario_questions):
                self.show_next_question()
            else:
                self.show_scenario_results()
        else:
            self.show_main_menu()

    def start_prevention_scenario(self):
        self.current_scenario = "prevention"
        self.scenario_questions = [
            {
                "scenario_info": "📋 ЭТАП 1: Настройка политики удаленного доступа",
                "question": "Компания внедряет удаленную работу. Как настроить доступ для сотрудников?",
                "options": [
                    "Разрешить RDP доступ напрямую с любого IP для удобства",
                    "Настроить VPN с двухфакторной аутентификацией и ограничить доступ по IP",
                    "Использовать TeamViewer с простыми паролями для быстрого развертывания",
                    "Разрешить SSH доступ на все рабочие станции с паролем 'admin'"
                ],
                "correct": "Настроить VPN с двухфакторной аутентификацией и ограничить доступ по IP",
                "hints": {
                    "Разрешить RDP доступ напрямую с любого IP для удобства": "Прямой RDP доступ - любимая цель брутфорс атак!",
                    "Использовать TeamViewer с простыми паролями для быстрого развертывания": "TeamViewer часто взламывают, а простые пароли уязвимы",
                    "Разрешить SSH доступ на все рабочие станции с паролем 'admin'": "SSH с слабыми паролями легко взламывается автоматическими скриптами"
                },
                "image_key": "prevention_1"
            },
            {
                "scenario_info": "📋 ЭТАП 2: Управление обновлениями в критической системе", 
                "question": "Обнаружена критическая уязвимость в системе контроля доступа. Система работает 24/7.",
                "options": [
                    "Отложить обновление до следующего планового обслуживания через 3 месяца",
                    "Немедленно установить обновление в рабочее время без тестирования", 
                    "Протестировать обновление на стенде, затем установить в период низкой нагрузки",
                    "Настроить WAF правила как временное решение вместо обновления"
                ],
                "correct": "Протестировать обновление на стенде, затем установить в период низкой нагрузки",
                "hints": {
                    "Отложить обновление до следующего планового обслуживания через 3 месяца": "Критические уязвимости должны исправляться немедленно!",
                    "Немедленно установить обновление в рабочее время без тестирования": "Обновление может сломать критическую систему", 
                    "Настроить WAF правила как временное решение вместо обновления": "WAF не заменяет патчи для уязвимостей приложения"
                },
                "image_key": "prevention_2"
            },
            {
                "scenario_info": "📋 ЭТАП 3: Политика резервного копирования",
                "question": "Как организовать защиту от ransomware для финансовых данных?",
                "options": [
                    "Ежедневное копирование на сетевой диск с общим доступом",
                    "3-2-1 правило: 3 копии, 2 разных носителя, 1 вне офиса + immutable backup", 
                    "Копирование раз в неделю на внешний HDD который хранится рядом с сервером",
                    "Использовать только облачное копирование без локальных копий"
                ],
                "correct": "3-2-1 правило: 3 копии, 2 разных носителя, 1 вне офиса + immutable backup",
                "hints": {
                    "Ежедневное копирование на сетевой диск с общим доступом": "Ransomware шифрует и сетевые диски!",
                    "Копирование раз в неделю на внешний HDD который хранится рядом с сервером": "Мало копий и они могут быть уничтожены вместе с сервером",
                    "Использовать только облачное копирование без локальных копий": "Облачные копии могут синхронизировать зашифрованные файлы" 
                },
                "image_key": "prevention_3"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_detection_scenario(self):
        self.current_scenario = "detection" 
        self.scenario_questions = [
            {
                "scenario_info": "🔍 ЭТАП 1: Анализ подозрительной активности в логах",
                "question": "В логах обнаружены множественные failed logins с разных IP, но успешный login с IP сотрудника. Что делать?",
                "options": [
                    "Заблокировать IP сотрудника как скомпрометированный",
                    "Проигнорировать - раз есть успешный вход, все в порядке", 
                    "Проверить геолокацию IP сотрудника и время входа на аномалии, запросить подтверждение",
                    "Сменить пароль сотрудника и попросить больше не беспокоить"
                ],
                "correct": "Проверить геолокацию IP сотрудника и время входа на аномалии, запросить подтверждение",
                "hints": {
                    "Заблокировать IP сотрудника как скомпрометированный": "Может быть ложное срабатывание - нужна проверка",
                    "Проигнорировать - раз есть успешный вход, все в порядке": "Успешный вход мог быть сделан злоумышленником!", 
                    "Сменить пароль сотрудника и попросить больше не беспокоить": "Не решает проблему возможного компрометации аккаунта"
                },
                "image_key": "detection_1"
            },
            {
                "scenario_info": "🔍 ЭТАП 2: Обнаружение lateral movement",
                "question": "Система обнаружила необычный трафик между рабочими станциями в одном сегменте сети. Как реагировать?",
                "options": [
                    "Это нормальный трафик между коллегами - игнорировать",
                    "Немедленно отключить все рабочие станции от сети",
                    "Проанализировать тип трафика, проверить процессы на вовлеченных машинах",
                    "Увеличить пропускную способность сети чтобы трафик не мешал работе"
                ],
                "correct": "Проанализировать тип трафика, проверить процессы на вовлеченных машинах",
                "hints": {
                    "Это нормальный трафик между коллегами - игнорировать": "Lateral movement - ключевой признак продвинутой атаки!",
                    "Немедленно отключить все рабочие станции от сети": "Слишком радикально, может быть легитимная причина",
                    "Увеличить пропускную способность сети чтобы трафик не мешал работе": "Не решает проблему безопасности, только маскирует симптомы"
                },
                "image_key": "detection_2"
            },
            {
                "scenario_info": "🔍 ЭТАП 3: Расследование инцидента с данными",
                "question": "Обнаружены большие исходящие передачи данных ночью. Подозревается утечка. С чего начать расследование?",
                "options": [
                    "Немедленно сообщить в правоохранительные органы без внутреннего расследования",
                    "Проверить логи доступа, DLP системы, идентифицировать пользователя и данные",
                    "Отключить интернет чтобы предотвратить дальнейшую утечку",
                    "Ничего не делать - ночные передачи это норма для backup систем"
                ],
                "correct": "Проверить логи доступа, DLP системы, идентифицировать пользователя и данные",
                "hints": {
                    "Немедленно сообщить в правоохранительные органы без внутреннего расследования": "Нужно сначала собрать evidence для передачи",
                    "Отключить интернет чтобы предотвратить дальнейшую утечку": "Уничтожает возможность отследить конечную точку утечки",
                    "Ничего не делать - ночные передачи это норма для backup систем": "Backup обычно входящий трафик, а не исходящий большими объемами"
                },
                "image_key": "detection_3"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_response_scenario(self):
        self.current_scenario = "response"
        self.scenario_questions = [
            {
                "scenario_info": "🚨 ЭТАП 1: Обнаружен активный ransomware в сети", 
                "question": "Несколько рабочих станций зашифрованы. Пользователи сообщают о требованиях выкупа. Ваши первые действия?",
                "options": [
                    "Заплатить выкуп чтобы быстро восстановить работу",
                    "Немедленно отключить всю корпоративную сеть от интернета", 
                    "Изолировать зараженные машины, сохранить образы памяти для анализа",
                    "Переустановить все системы без анализа инцидента"
                ],
                "correct": "Изолировать зараженные машины, сохранить образы памяти для анализа", 
                "hints": {
                    "Заплатить выкуп чтобы быстро восстановить работу": "Нет гарантии восстановления, финансирует преступников!",
                    "Немедленно отключить всю корпоративную сеть от интернета": "Может помешать бизнесу и уничтожить evidence", 
                    "Переустановить все системы без анализа инцидента": "Не позволяет понять вектор атаки для предотвращения повторения"
                },
                "image_key": "response_1"
            },
            {
                "scenario_info": "🚨 ЭТАП 2: Восстановление после атаки",
                "question": "После изоляции ransomware, как безопасно восстановить данные?",
                "options": [
                    "Восстановить из последнего backup даже если он может быть заражен",
                    "Использовать инструменты дешифрования от антивирусных компаний",
                    "Восстановить из backup сделанного до атаки, проверив его чистоту",
                    "Вручную восстановить данные из зашифрованных файлов"
                ],
                "correct": "Восстановить из backup сделанного до атаки, проверив его чистоту",
                "hints": {
                    "Восстановить из последнего backup даже если он может быть заражен": "Может восстановить уже зараженные данные!",
                    "Использовать инструменты дешифрования от антивирусных компаний": "Не всегда работают, особенно с новыми ransomware",
                    "Вручную восстановить данные из зашифрованных файлов": "Обычно невозможно без ключа дешифрования"
                },
                "image_key": "response_2"
            },
            {
                "scenario_info": "🚨 ЭТАП 3: Пост-инцидентный анализ и отчетность",
                "question": "Руководство требует отчет об инциденте. Что включить чтобы избежать повторения?",
                "options": [
                    "Минимизировать информацию чтобы не беспокоить руководство",
                    "Полный технический отчет без рекомендаций для бизнеса",
                    "Детальный анализ: вектор атаки, уязвимости, рекомендации по улучшению",
                    "Обвинить конкретного сотрудника в нарушении политик"
                ],
                "correct": "Детальный анализ: вектор атаки, уязвимости, рекомендации по улучшению",
                "hints": {
                    "Минимизировать информацию чтобы не беспокоить руководство": "Скрытие информации мешает улучшению безопасности",
                    "Полный технический отчет без рекомендаций для бизнеса": "Бизнес-руководство не поймет чисто технический отчет",
                    "Обвинить конкретного сотрудника в нарушении политик": "Не конструктивно, системные проблемы останутся"
                },
                "image_key": "response_3"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_logfile_scenario(self):
        self.current_scenario = "logfile"
        self.scenario_questions = [
            {
                "scenario_info": "📋 ЭТАП 1: Обнаружение подозрительной активности в логах",
                "question": "В лог-файлах веб-сервера обнаружены множественные запросы с одинакового IP: 'POST /login.php' с разными логинами. Что делать?",
                "options": [
                    "Проигнорировать - это нормальная активность пользователей",
                    "Немедленно заблокировать IP в firewall и продолжить анализ", 
                    "Настроить alert на подобные паттерны и усилить мониторинг этого IP",
                    "Увеличить уровень логирования для всех запросов"
                ],
                "correct": "Настроить alert на подобные паттерны и усилить мониторинг этого IP",
                "hints": {
                    "Проигнорировать - это нормальная активность пользователей": "Множественные POST /login - классический признак брутфорс атаки!",
                    "Немедленно заблокировать IP в firewall и продолжить анализ": "Блокировка без анализа может привести к ложным срабатываниям", 
                    "Увеличить уровень логирования для всех запросов": "Избыточное логирование может затруднить анализ реальных угроз"
                },
                "image_key": "logfile_1"
            },
            {
                "scenario_info": "📋 ЭТАП 2: Анализ логов после инцидента",
                "question": "После взлома системы нужно найти следы атаки. С чего начать анализ логов?",
                "options": [
                    "Просмотреть все логи за последний год построчно", 
                    "Начать с последних 24 часов и искать аномалии во времени событий",
                    "Сфокусироваться только на логах аутентификации",
                    "Удалить старые логи чтобы освободить место для анализа"
                ],
                "correct": "Начать с последних 24 часов и искать аномалии во времени событий",
                "hints": {
                    "Просмотреть все логи за последний год построчно": "Анализ года логов займет слишком много времени и может быть неэффективен",
                    "Сфокусироваться только на логах аутентификации": "Атака может использовать другие векторы - нужен комплексный анализ", 
                    "Удалить старые логи чтобы освободить место для анализа": "Старые логи могут содержать важные данные для расследования!"
                },
                "image_key": "logfile_2"
            },
            {
                "scenario_info": "📋 ЭТАП 3: Настройка ротации и хранения логов",
                "question": "Как настроить политику хранения логов для соответствия GDPR и расследования инцидентов?",
                "options": [
                    "Хранить логи 30 дней затем автоматически удалять",
                    "Хранить все логи бессрочно на дешевом S3 хранилище",
                    "Настроить многоуровневое хранение: 7 дней горячих, 30 дней теплых, 1 год холодных",
                    "Логировать только ошибки и хранить 14 дней"
                ],
                "correct": "Настроить многоуровневое хранение: 7 дней горячих, 30 дней теплых, 1 год холодных",
                "hints": {
                    "Хранить логи 30 дней затем автоматически удалять": "30 дней может быть недостаточно для расследования сложных инцидентов",
                    "Хранить все логи бессрочно на дешевом S3 хранилище": "Бессрочное хранение может нарушать GDPR и дорого обходиться",
                    "Логировать только ошибки и хранить 14 дней": "Недостаточное логирование затруднит расследование атак"
                },
                "image_key": "logfile_3"
            },
            {
                "scenario_info": "📋 ЭТАП 4: Обнаружение аномалий в логах приложений",
                "question": "В логах приложения появились записи 'SQL Syntax Error' с необычными символами в параметрах. Что это может означать?",
                "options": [
                    "Обычные ошибки разработки - можно игнорировать",
                    "Попытка SQL-инъекции - нужно срочно исследовать",
                    "Проблемы с кодировкой базы данных",
                    "Сбои в работе сетевого оборудования"
                ],
                "correct": "Попытка SQL-инъекции - нужно срочно исследовать",
                "hints": {
                    "Обычные ошибки разработки - можно игнорировать": "SQL ошибки с необычными символами - классический признак инъекций!",
                    "Проблемы с кодировкой базы данных": "Проблемы кодировки обычно проявляются иначе",
                    "Сбои в работе сетевого оборудования": "Сетевые проблемы не вызывают SQL Syntax Error"
                },
                "image_key": "logfile_4"
            },
            {
                "scenario_info": "📋 ЭТАП 5: Централизованное логирование в распределенной системе",
                "question": "В микросервисной архитектуре нужно обеспечить корреляцию логов между сервисами. Какой подход выбрать?",
                "options": [
                    "Использовать одинаковые имена файлов логов на всех сервисах",
                    "Внедрить сквозные идентификаторы запросов (trace-id)",
                    "Синхронизировать время на всех серверах с точностью до миллисекунд",
                    "Писать все логи в одну общую базу данных"
                ],
                "correct": "Внедрить сквозные идентификаторы запросов (trace-id)",
                "hints": {
                    "Использовать одинаковые имена файлов логов на всех сервисах": "Имена файлов не помогут связать логи одного запроса",
                    "Синхронизировать время на всех серверах с точностью до миллисекунд": "Точное время полезно, но не решает проблему корреляции",
                    "Писать все логи в одну общую базу данных": "Общая БД может стать узким местом и точкой отказа"
                },
                "image_key": "logfile_5"
            },
            {
                "scenario_info": "📋 ЭТАП 6: Реагирование на подозрительные логи аутентификации",
                "question": "В логах видны успешные логины с IP из разных стран в течение короткого времени. Пользователь утверждает, что не путешествовал. Что делать?",
                "options": [
                    "Считать это нормальным - пользователь использует VPN",
                    "Немедленно сбросить пароль пользователя и включить 2FA",
                    "Подождать следующего инцидента для сбора больше данных",
                    "Заблокировать учетную запись навсегда"
                ],
                "correct": "Немедленно сбросить пароль пользователя и включить 2FA",
                "hints": {
                    "Считать это нормальным - пользователь использует VPN": "Логины из разных стран за короткое время - явный признак компрометации!",
                    "Подождать следующего инцидента для сбора больше данных": "Ожидание дает злоумышленнику больше времени для действий",
                    "Заблокировать учетную запись навсегда": "Блокировка без исследования может быть излишней мерой"
                },
                "image_key": "logfile_6"
            },
            {
                "scenario_info": "📋 ЭТАП 7: Оптимизация производительности системы логирования",
                "question": "Приложение стало медленным из-за интенсивного логирования. Как оптимизировать без потери безопасности?",
                "options": [
                    "Отключить логирование полностью для повышения производительности",
                    "Использовать асинхронное логирование с буферизацией",
                    "Логировать только критические ошибки",
                    "Увеличить размер лог-файлов чтобы реже их ротировать"
                ],
                "correct": "Использовать асинхронное логирование с буферизацией",
                "hints": {
                    "Отключить логирование полностью для повышения производительности": "Без логов невозможно расследовать инциденты!",
                    "Логировать только критические ошибки": "Многие атаки не вызывают критических ошибок",
                    "Увеличить размер лог-файлов чтобы реже их ротировать": "Размер файлов не влияет на производительность записи"
                },
                "image_key": "logfile_7"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def show_next_question(self):
        question_data = self.scenario_questions[self.current_question_index]
        self.create_question_frame(
            question_data["question"],
            question_data["options"], 
            question_data["correct"],
            question_data["hints"],
            question_data["scenario_info"],
            question_data["image_key"]
        )

    def show_scenario_results(self):
        self.clear_screen()

        result_frame = ttk.Frame(self.root)
        result_frame.pack(expand=True, fill='both', padx=20, pady=20)

        scenario_titles = {
            "prevention": "🛡️ Результаты сценария предотвращения",
            "detection": "🔍 Результаты сценария обнаружения",
            "response": "🚨 Результаты сценария реагирования",
            "logfile": "📋 Результаты сценария работы с логами"
        }

        title = ttk.Label(result_frame, text=scenario_titles.get(self.current_scenario, "Результаты"),
                          style='Title.TLabel')
        title.pack(pady=20)

        score_label = ttk.Label(result_frame, text=f"🏆 Набрано баллов: {self.user_score}/100",
                                style='Score.TLabel')
        score_label.pack(pady=10)

        feedback_text = scrolledtext.ScrolledText(result_frame, width=80, height=10, font=('Arial', 10))
        feedback_text.pack(pady=20, fill='both', expand=True)

        if self.user_score >= 80:
            feedback = "✅ Отлично! Вы демонстрируете отличные знания в области кибербезопасности."
        elif self.user_score >= 60:
            feedback = "⚠️ Хорошо, но есть области для улучшения. Рекомендуется дополнительная практика."
        else:
            feedback = "❌ Требуется дополнительное обучение. Рекомендуется пройти сценарий еще раз."

        feedback_text.insert('1.0', f"{feedback}\n\n")
        feedback_text.insert('end', "Ваши выборы:\n")
        for i, choice in enumerate(self.user_choices[-3:], 1):
            feedback_text.insert('end', f"{i}. {choice}\n")

        feedback_text.config(state='disabled')

        button_frame = ttk.Frame(result_frame)
        button_frame.pack(pady=20)

        retry_btn = ttk.Button(button_frame, text="🔄 Пройти снова",
                               command=getattr(self, f'start_{self.current_scenario}_scenario'),
                               style='Game.TButton')
        retry_btn.pack(side='left', padx=10)

        menu_btn = ttk.Button(button_frame, text="📋 Главное меню",
                              command=self.show_main_menu,
                              style='Game.TButton')
        menu_btn.pack(side='left', padx=10)

    def show_statistics(self):
        self.clear_screen()

        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(expand=True, fill='both', padx=20, pady=20)

        title = ttk.Label(stats_frame, text="📊 Статистика обучения", style='Title.TLabel')
        title.pack(pady=20)

        score_label = ttk.Label(stats_frame, text=f"🏆 Общий счет: {self.user_score}/100",
                                style='Score.TLabel')
        score_label.pack(pady=10)

        progress_frame = ttk.Frame(stats_frame)
        progress_frame.pack(pady=20)

        progress = ttk.Progressbar(progress_frame, orient='horizontal', length=400, mode='determinate')
        progress['value'] = self.user_score
        progress.pack(pady=10)

        recommendations = scrolledtext.ScrolledText(stats_frame, width=80, height=8, font=('Arial', 10))
        recommendations.pack(pady=10, fill='both', expand=True)

        if self.user_score >= 80:
            rec_text = "🎉 Превосходно! Вы готовы к реальным вызовам кибербезопасности.\nРекомендуется: Практика на реальных CTF-соревнованиях"
        elif self.user_score >= 60:
            rec_text = "👍 Хороший уровень знаний.\nРекомендуется: Пройти все сценарии еще раз для закрепления"
        else:
            rec_text = "📚 Необходимо улучшить знания по кибербезопасности.\nРекомендуется: Пройти все сценарии, обращая внимание на подсказки"

        recommendations.insert('1.0', f"Рекомендации по обучению:\n\n{rec_text}")
        recommendations.config(state='disabled')

        back_btn = ttk.Button(stats_frame, text="🔙 Назад",
                              command=self.show_main_menu,
                              style='Game.TButton')
        back_btn.pack(pady=20)