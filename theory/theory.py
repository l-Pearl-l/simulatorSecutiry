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
        self.scenario_progress = {
            "prevention": 0,
            "detection": 0,
            "response": 0,
            "logfile": 0,
            "cryptography": 0,
            "network": 0,
            "web": 0,
            "incident_response": 0,
            "firewall_ips": 0,
            "cloud_security": 0
        }

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

            image_keys = [
                'prevention_1', 'prevention_2', 'prevention_3', 'prevention_4', 'prevention_5',
                'detection_1', 'detection_2', 'detection_3', 'detection_4', 'detection_5',
                'response_1', 'response_2', 'response_3', 'response_4', 'response_5',
                'logfile_1', 'logfile_2', 'logfile_3', 'logfile_4', 'logfile_5', 'logfile_6', 'logfile_7',
                'crypto_1', 'crypto_2', 'crypto_3', 'crypto_4', 'crypto_5',
                'network_1', 'network_2', 'network_3', 'network_4', 'network_5', 'network_6', 'network_7',
                'web_1', 'web_2', 'web_3', 'web_4', 'web_5',
                'incident_1', 'incident_2', 'incident_3', 'incident_4', 'incident_5',
                'firewall_1', 'firewall_2', 'firewall_3', 'firewall_4', 'firewall_5',
                'cloud_1', 'cloud_2', 'cloud_3', 'cloud_4', 'cloud_5'
            ]

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
        for widget in self.root.winfo_children():
            if hasattr(widget, 'back_button_marker'):
                continue
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()

        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)

        title_label = ttk.Label(header_frame, text="📚 РАСШИРЕННЫЙ ТЕОРЕТИЧЕСКИЙ МОДУЛЬ", style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(header_frame, text="Комплексное изучение кибербезопасности и защиты сетей",
                                   font=('Arial', 12), foreground='#bdc3c7')
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
            ("📝 Анализ логов и мониторинг", self.start_logfile_scenario),
            ("🔐 Криптография и PKI", self.start_cryptography_scenario),
            ("🌐 Защита сетевой инфраструктуры", self.start_network_scenario),
            ("⚡ Веб-безопасность и приложения", self.start_web_scenario),
            ("🔄 Действия при проникновении", self.start_incident_response_scenario),
            ("🛡️ Firewall и IPS", self.start_firewall_ips_scenario),
            ("☁️ Cloud Security", self.start_cloud_security_scenario),
            ("📊 Детальная статистика", self.show_statistics),
        ]

        for text, command in scenarios:
            btn = ttk.Button(menu_frame, text=text, command=command, style='Game.TButton', width=30)
            btn.pack(pady=6)

    def create_question_frame(self, question, options, correct_answer, hints, scenario_info="", image_key=None,
                              theory_text=""):
        self.clear_screen()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='x', pady=10)

        text_frame = ttk.Frame(top_frame)
        text_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))

        if scenario_info:
            info_label = ttk.Label(text_frame, text=scenario_info,
                                   font=('Arial', 10, 'italic', 'bold'),
                                   foreground='#e74c3c', wraplength=500)
            info_label.pack(anchor='w', pady=(0, 10))

        if theory_text:
            theory_frame = ttk.Frame(text_frame)
            theory_frame.pack(fill='x', pady=(0, 15))

            theory_label = ttk.Label(theory_frame, text="📖 Теоретическая справка:",
                                     font=('Arial', 11, 'bold'), foreground='#2ecc71')
            theory_label.pack(anchor='w')

            theory_content = ttk.Label(theory_frame, text=theory_text,
                                       font=('Arial', 10), wraplength=500, justify='left')
            theory_content.pack(anchor='w', pady=(5, 0))

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

        self.selected_option = tk.StringVar(value="")

        for i, option in enumerate(options, 1):
            option_frame = ttk.Frame(options_frame)
            option_frame.pack(fill='x', pady=6)

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
            self.user_score += 3  # Уменьшаем баллы за вопрос
            if self.current_scenario in self.scenario_progress:
                self.scenario_progress[self.current_scenario] += 1
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
                "scenario_info": "📋 ЭТАП 1: Базовые принципы информационной безопасности",
                "theory_text": "Принцип наименьших привилегий (PoLP) - пользователи и процессы должны иметь минимальные права, необходимые для выполнения задач. Defense in Depth - многоуровневая защита, где при нарушении одного уровня другие продолжают защищать.",
                "question": "Какой принцип безопасности нарушается, когда бухгалтеру дают права администратора для 'удобства'?",
                "options": [
                    "Принцип наименьших привилегий",
                    "Глубина защиты (Defense in Depth)",
                    "Разделение обязанностей",
                    "Полномочие по умолчанию"
                ],
                "correct": "Принцип наименьших привилегий",
                "hints": {
                    "Глубина защиты (Defense in Depth)": "Это про многоуровневую защиту, а не про права доступа",
                    "Разделение обязанностей": "Это про распределение критических задач между разными людьми",
                    "Полномочие по умолчанию": "Такого принципа в кибербезопасности нет"
                },
                "image_key": "prevention_1"
            },
            {
                "scenario_info": "📋 ЭТАП 2: Управление доступом и аутентификация",
                "theory_text": "MFA (Multi-Factor Authentication) значительно повышает безопасность, требуя два или более фактора аутентификации: что-то известное (пароль), что-то имеемое (токен), что-то присущее (биометрия).",
                "question": "Почему двухфакторная аутентификация считается обязательной для административного доступа?",
                "options": [
                    "Она полностью исключает возможность взлома",
                    "Она ускоряет процесс входа в систему",
                    "Требуется по стандарту PCI DSS для всех пользователей",
                    "Даже при компрометации пароля злоумышленнику нужен второй фактор"
                ],
                "correct": "Даже при компрометации пароля злоумышленнику нужен второй фактор",
                "hints": {
                    "Она полностью исключает возможность взлома": "MFA значительно улучшает безопасность, но не делает систему неуязвимой",
                    "Она ускоряет процесс входа в систему": "MFA обычно немного замедляет процесс аутентификации",
                    "Требуется по стандарту PCI DSS для всех пользователей": "PCI DSS требует MFA для административного доступа, но не для всех пользователей"
                },
                "image_key": "prevention_2"
            },
            {
                "scenario_info": "📋 ЭТАП 3: Сегментация сети и микросегментация",
                "theory_text": "Сегментация сети делит сеть на изолированные зоны для ограничения распространения атак. Микросегментация применяет политики безопасности на уровне отдельных workload.",
                "question": "Компания имеет единую плоскую сеть. После ransomware атаки, которая зашифровала все отделы, что рекомендуется?",
                "options": [
                    "Внедрить сегментацию сети на VLAN по отделам",
                    "Увеличить пропускную способность сети",
                    "Установить более мощный файрволл на периметре",
                    "Перейти на Wi-Fi 6 для всех сотрудников"
                ],
                "correct": "Внедрить сегментацию сети на VLAN по отделам",
                "hints": {
                    "Увеличить пропускную способность сети": "Пропускная способность не предотвращает распространение атак",
                    "Установить более мощный файрволл на периметре": "Периметровая защита не помогает при внутренних атаках",
                    "Перейти на Wi-Fi 6 для всех сотрудников": "Новая технология Wi-Fi не решает проблему сегментации"
                },
                "image_key": "prevention_3"
            },
            {
                "scenario_info": "📋 ЭТАП 4: Политики паролей и управление учетными данными",
                "theory_text": "NIST SP 800-63B рекомендует: минимальная длина 8 символов, проверка на утечку, отмена регулярной смены паролей. Использование менеджеров паролей значительно повышает безопасность.",
                "question": "Согласно современным рекомендациям NIST, какая политика паролей наиболее эффективна?",
                "options": [
                    "Обязательная ежемесячная смена сложных паролей",
                    "Длинные запоминаемые парольные фразы без обязательной регулярной смены",
                    "Пароли из 6 символов с обязательным использованием специальных символов",
                    "Ежеквартальная смена паролей с ведением истории 10 последних паролей"
                ],
                "correct": "Длинные запоминаемые парольные фразы без обязательной регулярной смены",
                "hints": {
                    "Обязательная ежемесячная смена сложных паролей": "Регулярная смена приводит к созданию слабых предсказуемых паролей",
                    "Пароли из 6 символов с обязательным использованием специальных символов": "Слишком короткие пароли легко подбираются",
                    "Ежеквартальная смена паролей с ведением истории 10 последних паролей": "Устаревшая практика, не рекомендованная NIST"
                },
                "image_key": "prevention_4"
            },
            {
                "scenario_info": "📋 ЭТАП 5: Security by Design и безопасная разработка",
                "theory_text": "SDLC (Software Development Life Cycle) должен включать этапы безопасности на всех стадиях. OWASP SAMM (Software Assurance Maturity Model) помогает организациям внедрять безопасную разработку.",
                "question": "На какой стадии разработки ПО наиболее экономично внедрять меры безопасности?",
                "options": [
                    "Только на стадии тестирования перед выпуском",
                    "После обнаружения уязвимостей в production",
                    "На этапе проектирования архитектуры (Design phase)",
                    "Во время код-ревью перед мержем в main branch"
                ],
                "correct": "На этапе проектирования архитектуры (Design phase)",
                "hints": {
                    "Только на стадии тестирования перед выпуском": "Исправление на поздних стадиях в 10-100 раз дороже",
                    "После обнаружения уязвимостей в production": "Самый дорогой вариант, включая репутационные потери",
                    "Во время код-ревью перед мержем в main branch": "Лучше чем в production, но хуже чем на этапе проектирования"
                },
                "image_key": "prevention_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_detection_scenario(self):
        self.current_scenario = "detection"
        self.scenario_questions = [
            {
                "scenario_info": "🔍 ЭТАП 1: Принципы обнаружения аномалий",
                "theory_text": "Системы обнаружения вторжений (IDS) бывают сетевыми (NIDS) и хостовыми (HIDS). Сигнатурный анализ ищет известные паттерны, поведенческий - отклонения от нормальной активности.",
                "question": "Чем поведенческий анализ (UEBA) отличается от сигнатурного в системах обнаружения?",
                "options": [
                    "Он работает быстрее и требует меньше ресурсов",
                    "Он может обнаруживать неизвестные ранее атаки и аномалии",
                    "Он не требует настройки и обучения",
                    "Он полностью заменяет сигнатурный анализ"
                ],
                "correct": "Он может обнаруживать неизвестные ранее атаки и аномалии",
                "hints": {
                    "Он работает быстрее и требует меньше ресурсов": "Поведенческий анализ обычно более ресурсоемкий",
                    "Он не требует настройки и обучения": "Требует периода обучения для определения нормального поведения",
                    "Он полностью заменяет сигнатурный анализ": "Оба метода дополняют друг друга"
                },
                "image_key": "detection_1"
            },
            {
                "scenario_info": "🔍 ЭТАП 2: Анализ сетевого трафика",
                "theory_text": "DPI (Deep Packet Inspection) анализирует содержимое пакетов, а не только заголовки. NetFlow/sFlow предоставляют метаданные о трафике для анализа аномалий.",
                "question": "В сетевом трафике обнаружены DNS запросы к подозрительным доменам с коротким TTL. Что это может означать?",
                "options": [
                    "Возможное использование DNS туннелирования для exfiltration данных",
                    "Нормальная работа CDN сети",
                    "Проблемы с DNS кешированием",
                    "Обновление антивирусных баз"
                ],
                "correct": "Возможное использование DNS туннелирования для exfiltration данных",
                "hints": {
                    "Нормальная работа CDN сети": "CDN обычно используют доверенные домены с нормальным TTL",
                    "Проблемы с DNS кешированием": "Проблемы кеширования проявляются иначе",
                    "Обновление антивирусных баз": "Антивирусы используют стандартные домены производителей"
                },
                "image_key": "detection_2"
            },
            {
                "scenario_info": "🔍 ЭТАП 3: Эвристический анализ и машинное обучение",
                "theory_text": "Машинное обучение в кибербезопасности использует алгоритмы для классификации аномалий. Важны качественные данные для обучения и предотвращение adversarial attacks.",
                "question": "Какая основная проблема машинного обучения в обнаружении кибератак?",
                "options": [
                    "Слишком высокая стоимость внедрения",
                    "Необходимость больших размеченных datasets для обучения",
                    "Невозможность работы в реальном времени",
                    "Требование квантовых компьютеров для работы"
                ],
                "correct": "Необходимость больших размеченных datasets для обучения",
                "hints": {
                    "Слишком высокая стоимость внедрения": "Есть open-source решения с умеренной стоимостью",
                    "Невозможность работы в реальном времени": "Современные ML системы работают в реальном времени",
                    "Требование квантовых компьютеров для работы": "ML в кибербезопасности не требует квантовых вычислений"
                },
                "image_key": "detection_3"
            },
            {
                "scenario_info": "🔍 ЭТАП 4: Threat Intelligence и IOC",
                "theory_text": "IOC (Indicators of Compromise) - артефакты, указывающие на взлом. TTP (Tactics, Techniques, Procedures) - методы и процедуры злоумышленников. STIX/TAXII - стандарты обмена threat intelligence.",
                "question": "Что из перечисленного является наиболее ценным в Threat Intelligence?",
                "options": [
                    "Списки IP для блокировки",
                    "Хэши известных вредоносных файлов",
                    "Тактики, техники и процедуры (TTP) групп злоумышленников",
                    "Доменные имена C&C серверов"
                ],
                "correct": "Тактики, техники и процедуры (TTP) групп злоумышленников",
                "hints": {
                    "Списки IP для блокировки": "IP легко меняются, низкая ценность",
                    "Хэши известных вредоносных файлов": "Хэши меняются при модификации файлов",
                    "Доменные имена C&C серверов": "Домены быстро сменяются"
                },
                "image_key": "detection_4"
            },
            {
                "scenario_info": "🔍 ЭТАП 5: EDR и поведенческий анализ на endpoint",
                "theory_text": "EDR (Endpoint Detection and Response) системы собирают детальную телеметрию с конечных точек и используют поведенческий анализ для обнаружения сложных атак.",
                "question": "Какое преимущество EDR над традиционным антивирусом?",
                "options": [
                    "Более низкое потребление ресурсов",
                    "Не требует подключения к интернету",
                    "Полная защита от zero-day уязвимостей",
                    "Возможность расследования и реакции на инциденты"
                ],
                "correct": "Возможность расследования и реакции на инциденты",
                "hints": {
                    "Более низкое потребление ресурсов": "EDR обычно более ресурсоемкий из-за сбора телеметрии",
                    "Не требует подключения к интернету": "Требует для получения обновлений и отправки alerts",
                    "Полная защита от zero-day уязвимостей": "Не обеспечивает полную защиту, но улучшает обнаружение"
                },
                "image_key": "detection_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_response_scenario(self):
        self.current_scenario = "response"
        self.scenario_questions = [
            {
                "scenario_info": "🚨 ЭТАП 1: Фреймворки реагирования на инциденты",
                "theory_text": "NIST SP 800-61 определяет фазы реагирования: подготовка, обнаружение, анализ, сдерживание, ликвидация, восстановление, извлечение уроков. SANS Institute предлагает похожий фреймворк.",
                "question": "Какая фаза реагирования на инциденты должна быть выполнена ПЕРЕД обнаружением инцидента?",
                "options": [
                    "Сдерживание (Containment)",
                    "Подготовка (Preparation)",
                    "Ликвидация (Eradication)",
                    "Восстановление (Recovery)"
                ],
                "correct": "Подготовка (Preparation)",
                "hints": {
                    "Сдерживание (Containment)": "Сдерживание происходит после обнаружения",
                    "Ликвидация (Eradication)": "Ликвидация после сдерживания",
                    "Восстановление (Recovery)": "Восстановление после ликвидации"
                },
                "image_key": "response_1"
            },
            {
                "scenario_info": "🚨 ЭТАП 2: Сбор и сохранение доказательств",
                "theory_text": "Цепочка сохранности (Chain of Custody) документирует handling доказательств. Критические данные: память, логи, образы дисков. Важно использовать write-blockers для сохранения целостности.",
                "question": "При сборе цифровых доказательств с компьютера жертвы атаки, что нужно сделать в первую очередь?",
                "options": [
                    "Создать полный образ памяти (memory dump)",
                    "Отключить компьютер от сети для предотвращения дальнейшего ущерба",
                    "Немедленно начать антивирусное сканирование",
                    "Сделать бэкап важных данных пользователя"
                ],
                "correct": "Создать полный образ памяти (memory dump)",
                "hints": {
                    "Отключить компьютер от сети для предотвращения дальнейшего ущерба": "Уничтожает volatile данные в памяти",
                    "Немедленно начать антивирусное сканирование": "Изменяет временные метки и может уничтожить evidence",
                    "Сделать бэкап важных данных пользователя": "Не является приоритетом при сборе доказательств"
                },
                "image_key": "response_2"
            },
            {
                "scenario_info": "🚨 ЭТАП 3: Коммуникация во время инцидента",
                "theory_text": "План коммуникации должен определять: что сообщать, кому, когда и как. Юридический отдел должен участвовать в коммуникации с внешними сторонами.",
                "question": "При серьезном инциденте утечки данных, когда следует уведомлять регулирующие органы?",
                "options": [
                    "Немедленно после обнаружения инцидента",
                    "После полного завершения расследования",
                    "В соответствии с требованиями законодательства (например, 72 часа в GDPR)",
                    "Только по запросу органов"
                ],
                "correct": "В соответствии с требованиями законодательства (например, 72 часа в GDPR)",
                "hints": {
                    "Немедленно после обнаружения инцидента": "Может быть преждевременно без понимания масштаба",
                    "После полного завершения расследования": "Может нарушить законодательные сроки",
                    "Только по запросу органов": "Активное уведомление требуется по закону"
                },
                "image_key": "response_3"
            },
            {
                "scenario_info": "🚨 ЭТАП 4: Пост-инцидентный анализ и улучшения",
                "theory_text": "AAR (After Action Review) должен проводиться после каждого значительного инцидента. Важно фокусироваться на системных улучшениях, а не поиске виноватых.",
                "question": "Что должно быть основным результатом пост-инцидентного анализа?",
                "options": [
                    "Наказание сотрудников, допустивших ошибки",
                    "Сокрытие информации для защиты репутации компании",
                    "Увеличение бюджеты на безопасность без конкретного плана",
                    "Изменение процессов и технологий для предотвращения повторения"
                ],
                "correct": "Изменение процессов и технологий для предотвращения повторения",
                "hints": {
                    "Наказание сотрудников, допустивших ошибки": "Создает культуру страха, а не улучшений",
                    "Сокрытие информации для защиты репутации компании": "Противоправно и не способствует улучшениям",
                    "Увеличение бюджеты на безопасность без конкретного плана": "Деньги без стратегии не эффективны"
                },
                "image_key": "response_4"
            },
            {
                "scenario_info": "🚨 ЭТАП 5: Управление уязвимостями и патч-менеджмент",
                "theory_text": "Программа управления уязвимостями включает: идентификацию, оценку, лечение и переоценку. CVSS (Common Vulnerability Scoring System) помогает приоритизировать исправления.",
                "question": "Критическая уязвимость обнаружена в системе, но установка патча требует ее отключения на 4 часа в рабочее время. Что делать?",
                "options": [
                    "Отложить установку до планового обслуживания через месяц",
                    "Немедленно установить патч несмотря на downtime",
                    "Оценить риск эксплуатации уязвимости vs бизнес-impact downtime и принять решение",
                    "Настроить WAF правила как временную меру на неопределенный срок"
                ],
                "correct": "Оценить риск эксплуатации уязвимости vs бизнес-impact downtime и принять решение",
                "hints": {
                    "Отложить установку до планового обслуживания через месяц": "Критическая уязвимость может быть использована мгновенно",
                    "Немедленно установить патч несмотря на downtime": "Может нанести unacceptable business impact",
                    "Настроить WAF правила как временную меру на неопределенный срок": "WAF не заменяет патчи для уязвимостей приложения"
                },
                "image_key": "response_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_logfile_scenario(self):
        self.current_scenario = "logfile"
        self.scenario_questions = [
            {
                "scenario_info": "📋 ЭТАП 1: Принципы централизованного логирования",
                "theory_text": "SIEM (Security Information and Event Management) системы агрегируют и коррелируют логи из различных источников. Важны нормализация данных и корреляция событий.",
                "question": "Почему локальное хранение логов на серверах считается плохой практикой?",
                "options": [
                    "Занимает слишком много дискового пространства",
                    "Снижает производительность приложений",
                    "Злоумышленник может удалить или модифицировать логи после компрометации",
                    "Требует специального ПО для просмотра"
                ],
                "correct": "Злоумышленник может удалить или модифицировать логи после компрометации",
                "hints": {
                    "Занимает слишком много дискового пространства": "Можно управлять политиками ротации",
                    "Снижает производительность приложений": "Правильно настроенное логирование минимально влияет на производительность",
                    "Требует специального ПО для просмотра": "Не является основной проблемой безопасности"
                },
                "image_key": "logfile_1"
            },
            {
                "scenario_info": "📋 ЭТАП 2: Анализ веб-логов на предмет атак",
                "theory_text": "Веб-логи содержат информацию об HTTP запросах. Паттерны атак: SQL injection, XSS, path traversal, brute force. Важны коды ответов, user-agent, рефереры.",
                "question": "В веб-логах обнаружены запросы с параметрами типа '.../../etc/passwd'. Что это за атака?",
                "options": [
                    "Path Traversal",
                    "SQL Injection",
                    "Cross-Site Scripting",
                    "Local File Inclusion"
                ],
                "correct": "Path Traversal",
                "hints": {
                    "SQL Injection": "SQLi использует SQL команды в параметрах",
                    "Cross-Site Scripting": "XSS использует JavaScript код",
                    "Local File Inclusion": "LFI может использовать path traversal, но это конкретно path traversal атака"
                },
                "image_key": "logfile_2"
            },
            {
                "scenario_info": "📋 ЭТАП 3: Корреляция событий в SIEM",
                "theory_text": "Корреляционные правила выявляют сложные атаки по совокупности событий. Пример: неудачные логины + успешный логин + доступ к чувствительным данным.",
                "question": "Какая последовательность событий наиболее подозрительна для корреляционного правила?",
                "options": [
                    "Множество failed logins с одного IP, затем successful login с того же IP",
                    "Успешный login с корпоративного IP в рабочее время",
                    "Единичный failed login с последующим successful login с другого IP",
                    "Неудачные логины с разных IP в течение дня"
                ],
                "correct": "Множество failed logins с одного IP, затем successful login с того же IP",
                "hints": {
                    "Успешный login с корпоративного IP в рабочее время": "Нормальное поведение",
                    "Единичный failed login с последующим successful login с другого IP": "Может быть опечаткой в пароле",
                    "Неудачные логины с разных IP в течение дня": "Может быть брутфорс, но без успешного входа менее критично"
                },
                "image_key": "logfile_3"
            },
            {
                "scenario_info": "📋 ЭТАП 4: Логирование в облачных средах",
                "theory_text": "CloudTrail (AWS), Activity Log (Azure), Cloud Audit Logs (GCP) предоставляют логи управления облачной инфраструктурой. Важно логировать как data plane, так и control plane события.",
                "question": "В AWS CloudTrail обнаружены вызовы API 'DeleteBucket' и 'TerminateInstances' из необычного региона. Что это может означать?",
                "options": [
                    "Нормальная работа системы автоскейлинга",
                    "Тестирование DRP (Disaster Recovery Plan)",
                    "Автоматическое удаление неиспользуемых ресурсов",
                    "Компрометация учетных данных и попытка разрушения инфраструктуры"
                ],
                "correct": "Компрометация учетных данных и попытка разрушения инфраструктуры",
                "hints": {
                    "Нормальная работа системы автоскейлинга": "Автоскейлинг не удаляет bucket и обычно работает из того же региона",
                    "Тестирование DRP (Disaster Recovery Plan)": "DRP тестирование планируется и известно команде",
                    "Автоматическое удаление неиспользуемых ресурсов": "Обычно происходит по расписанию и не из необычного региона"
                },
                "image_key": "logfile_4"
            },
            {
                "scenario_info": "📋 ЭТАП 5: Анализ производительности и оптимизация логирования",
                "theory_text": "Структурированное логирование (JSON) упрощает парсинг. Уровни логирования: DEBUG, INFO, WARN, ERROR. Sampling может уменьшить объем при сохранении полезности.",
                "question": "Приложение генерирует 10 ГБ логов в день. Как уменьшить объем без потери безопасности?",
                "options": [
                    "Отключить логирование полностью",
                    "Использовать sampling - логировать каждый 10-й запрос",
                    "Настроить уровни логирования и фильтровать ненужные события",
                    "Логировать только ошибки (ERROR level)"
                ],
                "correct": "Настроить уровни логирования и фильтровать ненужные события",
                "hints": {
                    "Отключить логирование полностью": "Делает невозможным расследование инцидентов",
                    "Использовать sampling - логировать каждый 10-й запрос": "Можно пропустить важные события атаки",
                    "Логировать только ошибки (ERROR level)": "Многие атаки не генерируют ERROR level события"
                },
                "image_key": "logfile_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_cryptography_scenario(self):
        self.current_scenario = "cryptography"
        self.scenario_questions = [
            {
                "scenario_info": "🔐 ЭТАП 1: Основы криптографии и типы шифрования",
                "theory_text": "Симметричное шифрование использует один ключ, асимметричное - пару ключей (публичный/приватный). Хэш-функции необратимы, цифровые подписи обеспечивают целостность и аутентичность.",
                "question": "Почему RSA считается более медленным чем AES для шифрования больших объемов данных?",
                "options": [
                    "RSA использует более сложные математические операции",
                    "AES имеет аппаратную поддержку в процессорах",
                    "RSA требует больше вычислительных ресурсов для операций с большими числами",
                    "Все варианты верны"
                ],
                "correct": "Все варианты верны",
                "hints": {
                    "RSA использует более сложные математические операции": "Частично верно, но не полный ответ",
                    "AES имеет аппаратную поддержку в процессорах": "Верно, но также не полный ответ",
                    "RSA требует больше вычислительных ресурсов для операций с большими числами": "Верно, но ответ не полный"
                },
                "image_key": "crypto_1"
            },
            {
                "scenario_info": "🔐 ЭТАП 2: PKI и управление цифровыми сертификатами",
                "theory_text": "PKI (Public Key Infrastructure) включает CA (Certificate Authority), RA (Registration Authority), валидацию сертификатов. OCSP и CRL используются для проверки отозванных сертификатов.",
                "question": "Что происходит при компрометации приватного ключа SSL сертификата?",
                "options": [
                    "Сертификат автоматически обновляется",
                    "Ничего - публичный ключ все еще безопасен",
                    "Владелец должен отозвать сертификат через CA",
                    "Сертификат продолжает работать как обычно"
                ],
                "correct": "Владелец должен отозвать сертификат через CA",
                "hints": {
                    "Сертификат автоматически обновляется": "Автоматического обновления при компрометации нет",
                    "Ничего - публичный ключ все еще безопасен": "Компрометация приватного ключа делает сертификат небезопасным",
                    "Сертификат продолжает работать как обычно": "Работать будет, но будет небезопасен"
                },
                "image_key": "crypto_2"
            },
            {
                "scenario_info": "🔐 ЭТАП 3: Криптографические хэш-функции",
                "theory_text": "Хэш-функции преобразуют данные в фиксированную строку. Свойства: детерминированность, быстрое вычисление, необратимость, устойчивость к коллизиям. SHA-256 - современный стандарт.",
                "question": "Какое свойство хэш-функции делает ее пригодной для хранения паролей?",
                "options": [
                    "Детерминированность - одинаковые входные данные дают одинаковый хэш",
                    "Необратимость - невозможно восстановить исходные данные из хэша",
                    "Быстрое вычисление - хэш считается за доли секунды",
                    "Фиксированная длина вывода независимо от размера ввода"
                ],
                "correct": "Необратимость - невозможно восстановить исходные данные из хэша",
                "hints": {
                    "Детерминированность - одинаковые входные данные дают одинаковый хэш": "Важно, но не основное для безопасности паролей",
                    "Быстрое вычисление - хэш считается за доли секунды": "Может быть недостатком для паролей (ускоряет брутфорс)",
                    "Фиксированная длина вывода независимо от размера ввода": "Удобно, но не критично для безопасности"
                },
                "image_key": "crypto_3"
            },
            {
                "scenario_info": "🔐 ЭТАП 4: Цифровые подписи и целостность данных",
                "theory_text": "Цифровые подписи используют асимметричную криптографию для проверки подлинности и целостности данных. Подпись создается приватным ключом, проверяется публичным.",
                "question": "Что гарантирует цифровая подпись документа?",
                "options": [
                    "Конфиденциальность содержимого документа",
                    "Высокую скорость передачи документа",
                    "Автоматическое шифрование документа при передаче",
                    "Подлинность отправителя и целостность содержимого"
                ],
                "correct": "Подлинность отправителя и целостность содержимого",
                "hints": {
                    "Конфиденциальность содержимого документа": "Цифровая подпись не обеспечивает шифрование",
                    "Высокую скорость передачи документа": "Не связано с функциями подписи",
                    "Автоматическое шифрование документа при передаче": "Требуется отдельная операция шифрования"
                },
                "image_key": "crypto_4"
            },
            {
                "scenario_info": "🔐 ЭТАП 5: Квантовая криптография и будущее",
                "theory_text": "Квантовые компьютеры угрожают современным асимметричным алгоритмам. Разрабатываются квантово-устойчивые алгоритмы. Квантовое распределение ключей (QKD) использует квантовые свойства для безопасного обмена ключами.",
                "question": "Почему квантовые компьютеры представляют угрозу для RSA и ECC?",
                "options": [
                    "Они могут взламывать любые алгоритмы мгновенно",
                    "Алгоритм Шора позволяет эффективно решать задачи факторизации и дискретного логарифма",
                    "Квантовые компьютеры быстрее классических во всех вычислениях",
                    "Они могут угадывать приватные ключи случайным образом"
                ],
                "correct": "Алгоритм Шора позволяет эффективно решать задачи факторизации и дискретного логарифма",
                "hints": {
                    "Они могут взламывать любые алгоритмы мгновенно": "Преувеличение, не все алгоритмы уязвимы",
                    "Квантовые компьютеры быстрее классических во всех вычислениях": "Только для специфических задач",
                    "Они могут угадывать приватные ключи случайным образом": "Некорректное представление работы"
                },
                "image_key": "crypto_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_network_scenario(self):
        self.current_scenario = "network"
        self.scenario_questions = [
            {
                "scenario_info": "🌐 ЭТАП 1: Основы сетевой безопасности",
                "theory_text": "Защита сети включает предотвращение несанкционированного доступа и минимизацию ущерба при успешном проникновении. Ключевые принципы: сегментация, мониторинг, контроль доступа.",
                "question": "Какой подход наиболее эффективен для защиты корпоративной сети от внутренних угроз?",
                "options": [
                    "Установка мощного файрволла на периметре",
                    "Реализация микросегментации и Zero Trust архитектуры",
                    "Использование только проводных соединений",
                    "Полное отключение от интернета"
                ],
                "correct": "Реализация микросегментации и Zero Trust архитектуры",
                "hints": {
                    "Установка мощного файрволла на периметре": "Не защищает от внутренних угроз",
                    "Использование только проводных соединений": "Не решает проблему внутренних атак",
                    "Полное отключение от интернета": "Нереалистично для современного бизнеса"
                },
                "image_key": "network_1"
            },
            {
                "scenario_info": "🌐 ЭТАП 2: Сегментация сети",
                "theory_text": "Сегментация делит сеть на изолированные зоны для ограничения lateral movement. VLAN, ACL, программно-определяемые сети (SDN) - инструменты сегментации.",
                "question": "Почему плоская сеть без сегментации опасна при компрометации одной системы?",
                "options": [
                    "Увеличивается нагрузка на серверы",
                    "Сложнее настраивать оборудование",
                    "Злоумышленник получает доступ ко всей сети",
                    "Замедляется скорость передачи данных"
                ],
                "correct": "Злоумышленник получает доступ ко всей сети",
                "hints": {
                    "Увеличивается нагрузка на серверы": "Не основная проблема безопасности",
                    "Сложнее настраивать оборудование": "Относится к удобству администрирования",
                    "Замедляется скорость передачи данных": "Не является основной угрозой безопасности"
                },
                "image_key": "network_2"
            },
            {
                "scenario_info": "🌐 ЭТАП 3: Обнаружение сетевых аномалий",
                "theory_text": "NIDS (Network Intrusion Detection Systems) анализируют трафик на признаки атак. DPI (Deep Packet Inspection) позволяет анализировать содержимое пакетов.",
                "question": "Какие признаки в сетевом трафике могут указывать на exfiltration данных?",
                "options": [
                    "Регулярные HTTPS соединения к известным сайтам",
                    "Необычно большие объемы исходящего трафика в нерабочее время",
                    "Стабильный VoIP трафик в рабочее время",
                    "DNS запросы к корпоративным доменам"
                ],
                "correct": "Необычно большие объемы исходящего трафика в нерабочее время",
                "hints": {
                    "Регулярные HTTPS соединения к известным сайтам": "Нормальная сетевая активность",
                    "Стабильный VoIP трафик в рабочее время": "Легитимный бизнес-трафик",
                    "DNS запросы к корпоративным доменам": "Стандартная сетевая активность"
                },
                "image_key": "network_3"
            },
            {
                "scenario_info": "🌐 ЭТАП 4: Защита от DDoS атак",
                "theory_text": "DDoS атаки aim to overwhelm resources. Защита включает: rate limiting, scrubbing centers, Anycast, поведенческий анализ трафика.",
                "question": "Какая стратегия наиболее эффективна против сложных DDoS атак?",
                "options": [
                    "Увеличение пропускной способности канала",
                    "Блокировка всех входящих соединений",
                    "Использование облачных scrubbing сервисов",
                    "Отключение веб-серверов на время атаки"
                ],
                "correct": "Использование облачных scrubbing сервисов",
                "hints": {
                    "Увеличение пропускной способности канала": "Атакующие могут увеличить мощность атаки",
                    "Блокировка всех входящих соединений": "Приводит к отказу в обслуживании легитимных пользователей",
                    "Отключение веб-серверов на время атаки": "Достигает цели атакующих"
                },
                "image_key": "network_4"
            },
            {
                "scenario_info": "🌐 ЭТАП 5: Zero Trust архитектура",
                "theory_text": "Zero Trust предполагает 'never trust, always verify'. Все запросы аутентифицируются, авторизуются и шифруются. Микросегментация ограничивает lateral movement.",
                "question": "Какой принцип является основополагающим в Zero Trust?",
                "options": [
                    "Никогда не доверять, всегда проверять",
                    "Доверять, но проверять внутренний трафик",
                    "Полностью изолировать сеть от интернета",
                    "Использовать только аппаратные решения"
                ],
                "correct": "Никогда не доверять, всегда проверять",
                "hints": {
                    "Доверять, но проверять внутренний трафик": "Противоположность Zero Trust",
                    "Полностью изолировать сеть от интернета": "Нереалистично для бизнеса",
                    "Использовать только аппаратные решения": "Не является принципом Zero Trust"
                },
                "image_key": "network_5"
            },
            {
                "scenario_info": "🌐 ЭТАП 6: Защита беспроводных сетей",
                "theory_text": "Wi-Fi безопасность включает: WPA3, сегментацию гостевых сетей, мониторинг rogue access points, сильную аутентификацию.",
                "question": "Что является самой серьезной угрозой для корпоративной Wi-Fi сети?",
                "options": [
                    "Слабый сигнал в некоторых помещениях",
                    "Rogue access points и evil twin атаки",
                    "Использование устаревших протоколов шифрования",
                    "Отсутствие гостевой сети"
                ],
                "correct": "Rogue access points и evil twin атаки",
                "hints": {
                    "Слабый сигнал в некоторых помещениях": "Проблема покрытия, а не безопасности",
                    "Использование устаревших протоколов шифрования": "Важно, но не самая серьезная угроза",
                    "Отсутствие гостевой сети": "Может привести к использованию сотрудниками небезопасных сетей"
                },
                "image_key": "network_6"
            },
            {
                "scenario_info": "🌐 ЭТАП 7: Сетевая forensics",
                "theory_text": "Сетевой forensics включает сбор и анализ сетевых артефактов: PCAP файлы, NetFlow данные, логи сетевых устройств. Важно сохранять цепочку доказательств.",
                "question": "Что критически важно при сборе сетевых доказательств для судебного разбирательства?",
                "options": [
                    "Сбор максимального объема данных без фильтрации",
                    "Соблюдение chain of custody и использование write-blockers",
                    "Немедленное удаление подозрительного трафика",
                    "Использование только открытого ПО для анализа"
                ],
                "correct": "Соблюдение chain of custody и использование write-blockers",
                "hints": {
                    "Сбор максимального объема данных без фильтрации": "Может быть неэффективным и затратным",
                    "Немедленное удаление подозрительного трафика": "Уничтожает доказательства",
                    "Использование только открытого ПО для анализа": "Не гарантирует достоверность доказательств"
                },
                "image_key": "network_7"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_web_scenario(self):
        self.current_scenario = "web"
        self.scenario_questions = [
            {
                "scenario_info": "⚡ ЭТАП 1: OWASP Top 10 и веб-уязвимости",
                "theory_text": "OWASP Top 10 включает: Injection, Broken Authentication, Sensitive Data Exposure, XXE, Broken Access Control, Security Misconfiguration, XSS, Insecure Deserialization, Using Components with Known Vulnerabilities, Insufficient Logging & Monitoring.",
                "question": "Какая уязвимость позволяет злоумышленнику выполнять произвольные команды на сервере?",
                "options": [
                    "Cross-Site Scripting (XSS)",
                    "SQL Injection",
                    "Cross-Site Request Forgery (CSRF)",
                    "Security Misconfiguration"
                ],
                "correct": "SQL Injection",
                "hints": {
                    "Cross-Site Scripting (XSS)": "XSS выполняется в браузере жертвы, а не на сервере",
                    "Cross-Site Request Forgery (CSRF)": "CSRF заставляет жертву выполнять действия, но не произвольные команды",
                    "Security Misconfiguration": "Может позволить доступ, но не обязательно выполнение команд"
                },
                "image_key": "web_1"
            },
            {
                "scenario_info": "⚡ ЭТАП 2: Межсайтовый скриптинг (XSS)",
                "theory_text": "XSS бывает reflected, stored и DOM-based. Защита: валидация input, экранирование output, Content Security Policy (CSP), HTTPOnly cookies.",
                "question": "Какой тип XSS наиболее опасен для пользователей веб-приложения?",
                "options": [
                    "Stored XSS - вредоносный скрипт сохраняется на сервере",
                    "Reflected XSS - уязвимость возникает при немедленном отражении input",
                    "DOM-based XSS - уязвимость в клиентском скрипте",
                    "Все типы одинаково опасны"
                ],
                "correct": "Stored XSS - вредоносный скрипт сохраняется на сервере",
                "hints": {
                    "Reflected XSS - уязвимость возникает при немедленном отражении input": "Требует взаимодействия пользователя",
                    "DOM-based XSS - уязвимость в клиентском скрипте": "Локальная для браузера",
                    "Все типы одинаково опасны": "Stored XSS имеет наибольший охват"
                },
                "image_key": "web_2"
            },
            {
                "scenario_info": "⚡ ЭТАП 3: Аутентификация и сессии",
                "theory_text": "Безопасная аутентификация требует: хэширования паролей с salt, защиты от брутфорса, безопасного управления сессиями, использования secure flags для cookies.",
                "question": "Почему сессионные cookies должны иметь флаги HttpOnly и Secure?",
                "options": [
                    "Чтобы предотвратить кражу cookies через XSS и передачу по HTTP",
                    "Для совместимости со старыми браузерами",
                    "Чтобы разрешить доступ к cookies из JavaScript",
                    "Для ускорения работы приложения"
                ],
                "correct": "Чтобы предотвратить кражу cookies через XSS и передачу по HTTP",
                "hints": {
                    "Для ускорения работы приложения": "Не влияет на производительность",
                    "Для совместимости со старыми браузерами": "Старые браузеры могут не поддерживать эти флаги",
                    "Чтобы разрешить доступ к cookies из JavaScript": "HttpOnly как раз запрещает доступ из JS"
                },
                "image_key": "web_3"
            },
            {
                "scenario_info": "⚡ ЭТАП 4: Безопасность API",
                "theory_text": "REST API уязвимы для: недостаточной авторизации, инъекций, массового назначения (mass assignment). Защита: аутентификация OAuth2/JWT, валидация input, rate limiting.",
                "question": "Какая основная угроза для API без proper rate limiting?",
                "options": [
                    "Утечка данных через инъекции",
                    "Межсайтовый скриптинг",
                    "Брутфорс атаки на аутентификацию",
                    "Недостаточная валидация input"
                ],
                "correct": "Брутфорс атаки на аутентификацию",
                "hints": {
                    "Утечка данных через инъекции": "Решается валидацией input",
                    "Межсайтовый скриптинг": "API обычно не рендерят HTML",
                    "Недостаточная валидация input": "Важно, но не основная угроза для rate limiting"
                },
                "image_key": "web_4"
            },
            {
                "scenario_info": "⚡ ЭТАП 5: Content Security Policy (CSP)",
                "theory_text": "CSP - механизм безопасности, ограничивающий источники исполняемого кода. Предотвращает XSS путем whitelist доверенных источников скриптов, стилей и других ресурсов.",
                "question": "Как CSP помогает защититься от XSS атак?",
                "options": [
                    "Шифрует весь трафик между клиентом и сервером",
                    "Ограничивает источники, из которых могут загружаться скрипты",
                    "Предоставляет двухфакторную аутентификацию",
                    "Автоматически исправляет уязвимости в коде"
                ],
                "correct": "Ограничивает источники, из которых могут загружаться скрипты",
                "hints": {
                    "Шифрует весь трафик между клиентом и сервером": "Это функция HTTPS",
                    "Предоставляет двухфакторную аутентификацию": "Не связано с CSP",
                    "Автоматически исправляет уязвимости в коде": "CSP не исправляет код"
                },
                "image_key": "web_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_incident_response_scenario(self):
        self.current_scenario = "incident_response"
        self.scenario_questions = [
            {
                "scenario_info": "🔄 ЭТАП 1: Обнаружение проникновения",
                "theory_text": "Ранние признаки компрометации: аномальная сетевая активность, необычные процессы, подозрительные логины, изменения в системных файлах. Важно иметь baseline нормального поведения.",
                "question": "Что является наиболее надежным признаком успешного проникновения в сеть?",
                "options": [
                    "Единичный failed login attempt",
                    "Наличие beaconing трафика к внешним C&C серверам",
                    "Временное замедление сети",
                    "Обновление антивирусных баз"
                ],
                "correct": "Наличие beaconing трафика к внешним C&C серверам",
                "hints": {
                    "Единичный failed login attempt": "Может быть ошибкой пользователя",
                    "Временное замедление сети": "Может иметь различные причины",
                    "Обновление антивирусных баз": "Нормальная системная активность"
                },
                "image_key": "incident_1"
            },
            {
                "scenario_info": "🔄 ЭТАП 2: Первоначальные действия",
                "theory_text": "При подтверждении проникновения: изолировать затронутые системы, сохранить доказательства, активировать план реагирования. Не следует сразу выключать системы - это уничтожает volatile данные.",
                "question": "Что следует сделать в первую очередь при подтверждении успешного проникновения?",
                "options": [
                    "Немедленно отключить все затронутые системы от сети",
                    "Собрать образы памяти и критичные логи, затем изолировать",
                    "Начать антивирусное сканирование всех систем",
                    "Переустановить операционные системы на подозрительных машинах"
                ],
                "correct": "Собрать образы памяти и критичные логи, затем изолировать",
                "hints": {
                    "Немедленно отключить все затронутые системы от сети": "Уничтожает доказательства в памяти",
                    "Начать антивирусное сканирование всех систем": "Может изменить временные метки файлов",
                    "Переустановить операционные системы на подозрительных машинах": "Уничтожает все доказательства"
                },
                "image_key": "incident_2"
            },
            {
                "scenario_info": "🔄 ЭТАП 3: Сдерживание распространения",
                "theory_text": "Сдерживание включает: блокировку компрометированных учетных записей, изоляцию сетевых сегментов, отзыв сертификатов. Важно предотвратить lateral movement и exfiltration данных.",
                "question": "Как эффективно ограничить lateral movement злоумышленника в сети?",
                "options": [
                    "Отключить всю корпоративную сеть",
                    "Увеличить права доступа для администраторов",
                    "Применить микросегментацию и заблокировать межсегментный трафик",
                    "Обновить пароли всех пользователей"
                ],
                "correct": "Применить микросегментацию и заблокировать межсегментный трафик",
                "hints": {
                    "Отключить всю корпоративную сеть": "Приводит к полному простою бизнеса",
                    "Увеличить права доступа для администраторов": "Может усугубить ситуацию",
                    "Обновить пароли всех пользователей": "Не останавливает уже активную сессию"
                },
                "image_key": "incident_3"
            },
            {
                "scenario_info": "🔄 ЭТАП 4: Ликвидация и восстановление",
                "theory_text": "Ликвидация включает удаление вредоносного ПО, закрытие уязвимостей. Восстановление - возврат систем в рабочее состояние из чистых бэкапов. Важно проверить бэкапы на наличие malware.",
                "question": "Как безопасно восстановить систему после компрометации?",
                "options": [
                    "Восстановить из последнего доступного бэкапа",
                    "Вручную удалить подозрительные файлы и процессы",
                    "Установить систему заново без восстановления данных",
                    "Восстановить из бэкапа, сделанного до инцидента, проверив его чистоту"
                ],
                "correct": "Восстановить из бэкапа, сделанного до инцидента, проверив его чистоту",
                "hints": {
                    "Восстановить из последнего доступного бэкапа": "Может восстановить уже зараженную систему",
                    "Вручную удалить подозрительные файлы и процессы": "Ненадежно, можно прописать бекдоры",
                    "Установить систему заново без восстановления данных": "Приводит к потере данных"
                },
                "image_key": "incident_4"
            },
            {
                "scenario_info": "🔄 ЭТАП 5: Постинцидентный анализ",
                "theory_text": "После инцидента проводится root cause analysis, оценивается эффективность response, вносятся улучшения в процессы и технологии. Документируются lessons learned.",
                "question": "Что является наиболее важным результатом постинцидентного анализа?",
                "options": [
                    "Наказание виновных сотрудников",
                    "Сокрытие факта инцидента от руководства",

                    "Внесение улучшений для предотвращения подобных инцидентов",
                    "Увеличение бюджета на безопасность без конкретного плана"
                ],
                "correct": "Внесение улучшений для предотвращения подобных инцидентов",
                "hints": {
                    "Наказание виновных сотрудников": "Создает культуру страха, а не улучшений",
                    "Сокрытие факта инцидента от руководства": "Противоправно и не способствует улучшениям",
                    "Увеличение бюджета на безопасность без конкретного плана": "Деньги без стратегии не эффективны"
                },
                "image_key": "incident_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_firewall_ips_scenario(self):
        self.current_scenario = "firewall_ips"
        self.scenario_questions = [
            {
                "scenario_info": "🛡️ ЭТАП 1: Типы файрволлов",
                "theory_text": "Файрволлы бывают: сетевые (пакетные), прикладного уровня, stateful, next-generation. NGFW включают IPS, антивирус, фильтрацию контента. WAF специализируется на веб-приложениях.",
                "question": "Чем next-generation firewall (NGFW) отличается от традиционного stateful firewall?",
                "options": [
                    "NGFW работает на более высоких скоростях",
                    "NGFW анализирует содержимое пакетов на прикладном уровне",
                    "NGFW только блокирует порты без анализа трафика",
                    "NGFW не требует обновлений сигнатур"
                ],
                "correct": "NGFW анализирует содержимое пакетов на прикладном уровне",
                "hints": {
                    "NGFW работает на более высоких скоростях": "Скорость не является основным отличием",
                    "NGFW только блокирует порты без анализа трафика": "Это функция простейших файрволлов",
                    "NGFW не требует обновлений сигнатур": "NGFW как раз требует регулярных обновлений"
                },
                "image_key": "firewall_1"
            },
            {
                "scenario_info": "🛡️ ЭТАП 2: Системы предотвращения вторжений (IPS)",
                "theory_text": "IPS активно блокирует подозрительный трафик, в отличие от IDS которая только обнаруживает. Режимы работы: inline, passive, tap. Важны tuning и мониторинг false positives.",
                "question": "Почему IPS может вызывать ложные срабатывания (false positives) и как это влияет на бизнес?",
                "options": [
                    "IPS всегда идеально точны и не вызывают ложных срабатываний",
                    "IPS только мониторит трафик и не блокирует его",
                    "Ложные срабатывания ускоряют работу сети",
                    "Легитимный трафик может быть ошибочно заблокирован, вызывая простои"
                ],
                "correct": "Легитимный трафик может быть ошибочно заблокирован, вызывая простои",
                "hints": {
                    "IPS всегда идеально точны и не вызывают ложных срабатываний": "Нереалистичное утверждение",
                    "IPS только мониторит трафик и не блокирует его": "Это IDS, а не IPS",
                    "Ложные срабатывания ускоряют работу сети": "Ложные срабатывания замедляют работу"
                },
                "image_key": "firewall_2"
            },
            {
                "scenario_info": "🛡️ ЭТАП 3: Настройка политик доступа",
                "theory_text": "Правила файрвола должны следовать принципу 'default deny'. Важны: логирование rejected пакетов, регулярный аудит правил, сегментация по зонам доверия.",
                "question": "Какая политика доступа считается наиболее безопасной для файрвола?",
                "options": [
                    "Заблокировать весь трафик и разрешать только необходимое (default deny)",
                    "Разрешить весь трафик и блокировать только известные угрозы",
                    "Разрешить весь исходящий трафик без ограничений",
                    "Блокировать только входящий трафик из интернета"
                ],
                "correct": "Заблокировать весь трафик и разрешать только необходимое (default deny)",
                "hints": {
                    "Разрешить весь трафик и блокировать только известные угрозы": "Очень опасный подход",
                    "Разрешить весь исходящий трафик без ограничений": "Позволяет exfiltration данных",
                    "Блокировать только входящий трафик из интернета": "Не защищает от внутренних угроз"
                },
                "image_key": "firewall_3"
            },
            {
                "scenario_info": "🛡️ ЭТАП 4: Обнаружение и предотвращение DDoS",
                "theory_text": "DDoS защита включает: rate limiting, behavioral analysis, scrubbing centers. Важно различать легитимный всплеск трафика и атаку. Cloud-based решения эффективны против объемных атак.",
                "question": "Почему традиционные файрволлы неэффективны против крупных DDoS атак?",
                "options": [
                    "Файрволлы не умеют анализировать DDoS трафик",
                    "Файрволлы становятся bottleneck и сами становятся целью",
                    "DDoS атаки используют только разрешенные порты",
                    "Файрволлы автоматически блокируют весь трафик при DDoS"
                ],
                "correct": "Файрволлы становятся bottleneck и сами становятся целью",
                "hints": {
                    "Файрволлы не умеют анализировать DDoS трафик": "Современные NGFW умеют анализировать",
                    "DDoS атаки используют только разрешенные порты": "Не основная причина",
                    "Файрволлы автоматически блокируют весь трафик при DDoS": "Не соответствует действительности"
                },
                "image_key": "firewall_4"
            },
            {
                "scenario_info": "🛡️ ЭТАП 5: Управление и мониторинг",
                "theory_text": "Эффективное управление файрволлом включает: central management, change control processes, регулярные аудиты правил, мониторинг производительности и alerts.",
                "question": "Что является лучшей практикой для управления изменениями в правилах файрвола?",
                "options": [
                    "Вносить изменения только в нерабочее время без уведомления",
                    "Разрешать администраторам вносить изменения без документирования",
                    "Внедрить процесс change control с тестированием и документированием",
                    "Обновлять правила раз в год для минимизации изменений"
                ],
                "correct": "Внедрить процесс change control с тестированием и документированием",
                "hints": {
                    "Разрешать администраторам вносить изменения без документирования": "Опасно и не отслеживаемо",
                    "Вносить изменения только в нерабочее время без уведомления": "Может вызвать непредвиденные проблемы",
                    "Обновлять правила раз в год для минимизации изменений": "Не соответствует потребностям бизнеса"
                },
                "image_key": "firewall_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def start_cloud_security_scenario(self):
        self.current_scenario = "cloud_security"
        self.scenario_questions = [
            {
                "scenario_info": "☁️ ЭТАП 1: Модель ответственности в облаке",
                "theory_text": "В IaaS провайдер отвечает за инфраструктуру, клиент - за ОС, приложения, данные. В PaaS провайдер отвечает за платформу, клиент - за приложения и данные. В SaaS провайдер отвечает за всё кроме данных и идентификации.",
                "question": "В модели IaaS кто отвечает за безопасность операционной системы?",
                "options": [
                    "Облачный провайдер",
                    "Клиент (пользователь облака)",
                    "Разделенная ответственность 50/50",
                    "Регулирующие органы"
                ],
                "correct": "Клиент (пользователь облака)",
                "hints": {
                    "Облачный провайдер": "Провайдер отвечает только за инфраструктуру",
                    "Разделенная ответственность 50/50": "Не точное описание модели",
                    "Регулирующие органы": "Не относятся к операционной ответственности"
                },
                "image_key": "cloud_1"
            },
            {
                "scenario_info": "☁️ ЭТАП 2: Identity and Access Management (IAM)",
                "theory_text": "Cloud IAM управляет доступом к ресурсам. Принцип наименьших привилегий критически важен. Роли предпочтительнее индивидуальных прав. Необходим регулярный аудит прав доступа.",
                "question": "Почему компрометация облачного IAM учетной записи особенно опасна?",
                "options": [
                    "Злоумышленник получает доступ ко всем ресурсам, разрешенным политиками IAM",
                    "Облачные провайдеры не предоставляют логи доступа",
                    "IAM учетные записи нельзя заблокировать",
                    "Облачные ресурсы автоматически шифруют все данные"
                ],
                "correct": "Злоумышленник получает доступ ко всем ресурсам, разрешенным политиками IAM",
                "hints": {
                    "Облачные провайдеры не предоставляют логи доступа": "Облачные провайдеры предоставляют детальные логи",
                    "IAM учетные записи нельзя заблокировать": "Учетные записи можно заблокировать",
                    "Облачные ресурсы автоматически шифруют все данные": "Не защищает от компрометации IAM"
                },
                "image_key": "cloud_2"
            },
            {
                "scenario_info": "☁️ ЭТАП 3: Защита данных в облаке",
                "theory_text": "Ключевые аспекты: encryption at rest и in transit, key management, DLP, backup и disaster recovery. Важно понимать где физически хранятся данные для compliance.",
                "question": "Какая стратегия шифрования наиболее безопасна для данных в облаке?",
                "options": [
                    "Полагаться только на шифрование провайдера",
                    "Использовать customer-managed keys с собственным key management",
                    "Не шифровать данные для лучшей производительности",
                    "Шифровать только базы данных"
                ],
                "correct": "Использовать customer-managed keys с собственным key management",
                "hints": {
                    "Полагаться только на шифрование провайдера": "Дает провайдеру доступ к данным",
                    "Не шифровать данные для лучшей производительности": "Очень опасно для конфиденциальных данных",
                    "Шифровать только базы данных": "Недостаточно для комплексной защиты"
                },
                "image_key": "cloud_3"
            },
            {
                "scenario_info": "☁️ ЭТАП 4: Cloud Security Posture Management (CSPM)",
                "theory_text": "CSPM инструменты автоматически обнаруживают misconfigurations и compliance violations. Постоянный мониторинг конфигураций против best practices и regulatory requirements.",
                "question": "Что является наиболее распространенной причиной утечек данных из облака?",
                "options": [
                    "Взломы сложных систем шифрования",
                    "Физические атаки на дата-центры",
                    "Ошибки конфигурации и misconfigurations",
                    "Уязвимости в гипервизорах"
                ],
                "correct": "Ошибки конфигурации и misconfigurations",
                "hints": {
                    "Взломы сложных систем шифрования": "Редко происходит при правильном key management",
                    "Физические атаки на дата-центры": "Облачные провайдеры имеют сильную физическую защиту",
                    "Уязвимости в гипервизорах": "Важно, но не самая частая причина утечек"
                },
                "image_key": "cloud_4"
            },
            {
                "scenario_info": "☁️ ЭТАП 5: Multi-cloud и hybrid security",
                "theory_text": "Multi-cloud среды требуют единого управления безопасностью across providers. Hybrid архитектуры соединяют on-prem и cloud. Важны: consistent policies, centralized monitoring, secure connectivity.",
                "question": "Какая основная проблема безопасности в multi-cloud средах?",
                "options": [
                    "Несовместимость технологий разных провайдеров",
                    "Сложность поддержания единых политик безопасности across providers",
                    "Отсутствие инструментов мониторинга",
                    "Более высокая стоимость шифрования"
                ],
                "correct": "Сложность поддержания единых политик безопасности across providers",
                "hints": {
                    "Несовместимость технологий разных провайдеров": "Проблема, но не основная",
                    "Отсутствие инструментов мониторинга": "Инструменты существуют",
                    "Более высокая стоимость шифрования": "Не основная проблема безопасности"
                },
                "image_key": "cloud_5"
            }
        ]
        self.current_question_index = 0
        self.show_next_question()

    def show_next_question(self):
        if self.current_question_index < len(self.scenario_questions):
            question_data = self.scenario_questions[self.current_question_index]
            self.create_question_frame(
                question_data["question"],
                question_data["options"],
                question_data["correct"],
                question_data["hints"],
                question_data["scenario_info"],
                question_data.get("image_key"),
                question_data.get("theory_text", "")
            )
        else:
            self.show_scenario_results()

    def show_scenario_results(self):
        self.clear_screen()

        result_frame = ttk.Frame(self.root)
        result_frame.pack(expand=True, fill='both', padx=20, pady=20)

        scenario_titles = {
            "prevention": "🛡️ Результаты сценария предотвращения",
            "detection": "🔍 Результаты сценария обнаружения",
            "response": "🚨 Результаты сценария реагирования",
            "logfile": "📋 Результаты сценария работы с логами",
            "cryptography": "🔐 Результаты сценария криптографии",
            "network": "🌐 Результаты сценария защиты сетей",
            "web": "⚡ Результаты сценария веб-безопасности",
            "incident_response": "🔄 Результаты сценария действий при проникновении",
            "firewall_ips": "🛡️ Результаты сценария Firewall и IPS",
            "cloud_security": "☁️ Результаты сценария Cloud Security"
        }

        title = ttk.Label(result_frame, text=scenario_titles.get(self.current_scenario, "Результаты"),
                          style='Title.TLabel')
        title.pack(pady=20)

        # Рассчитываем процент правильных ответов для этого сценария
        total_questions = len(self.scenario_questions)
        correct_answers = self.scenario_progress.get(self.current_scenario, 0)
        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        score_label = ttk.Label(result_frame,
                                text=f"🏆 Правильных ответов: {correct_answers}/{total_questions} ({percentage:.0f}%)",
                                style='Score.TLabel')
        score_label.pack(pady=10)

        feedback_text = scrolledtext.ScrolledText(result_frame, width=80, height=12, font=('Arial', 10))
        feedback_text.pack(pady=20, fill='both', expand=True)

        # Улучшенная система оценки
        if percentage >= 80:
            feedback = "🎉 Отлично! Вы демонстрируете отличные знания в этой области."
            color = "#2ecc71"
        elif percentage >= 60:
            feedback = "👍 Хорошо! Есть понимание основных концепций."
            color = "#f39c12"
        else:
            feedback = "💡 Есть над чем поработать. Рекомендуется изучить материал еще раз."
            color = "#e74c3c"

        feedback_text.insert('1.0', f"{feedback}\n\n", "result")
        feedback_text.tag_configure("result", foreground=color, font=('Arial', 11, 'bold'))

        feedback_text.insert('end', "Ключевые аспекты для запоминания:\n")

        key_points = {
            "network": [
                "• Zero Trust архитектура - 'никогда не доверяй, всегда проверяй'",
                "• Сегментация сети ограничивает lateral movement злоумышленников",
                "• Микросегментация обеспечивает гранулярный контроль доступа",
                "• Мониторинг аномального трафика помогает обнаружить exfiltration",
                "• DDoS защита требует многоуровневого подхода",
                "• Беспроводные сети уязвимы для rogue access points",
                "• Сетевой forensics требует сохранения chain of custody"
            ],
            "incident_response": [
                "• Beaconing трафик - надежный индикатор компрометации",
                "• При проникновении сначала сохраняйте доказательства, затем изолируйте",
                "• Lateral movement ограничивается микросегментацией",
                "• Восстановление должно выполняться из проверенных чистых бэкапов",
                "• Постинцидентный анализ фокусируется на улучшении процессов",
                "• Важно документировать все действия для последующего анализа",
                "• Коммуникация во время инцидента должна быть четкой и своевременной"
            ],
            "prevention": [
                "• Принцип наименьших привилегий - основа безопасности",
                "• MFA значительно снижает риск компрометации учетных записей",
                "• Сегментация сети ограничивает распространение атак",
                "• Security by Design - безопасность на этапе проектирования"
            ],
            "detection": [
                "• Поведенческий анализ обнаруживает неизвестные угрозы",
                "• Threat Intelligence ценен TTP, а не только IOC",
                "• EDR обеспечивает видимость и возможность реагирования на endpoint",
                "• Корреляция событий выявляет сложные multi-stage атаки"
            ],
            "response": [
                "• NIST SP 800-61 - стандарт реагирования на инциденты",
                "• Chain of Custody критична для юридических последствий",
                "• Коммуникация должна соответствовать законодательным требованиям",
                "• Пост-инцидентный анализ фокусируется на улучшении процессов"
            ],
            "logfile": [
                "• Централизованное логирование предотвращает потерю evidence",
                "• SIEM системы обеспечивают корреляцию событий",
                "• Cloud logging требует отдельной настройки control plane",
                "• Структурированное логирование упрощает анализ"
            ],
            "cryptography": [
                "• Асимметричное шифрование медленнее симметричного",
                "• Компрометация приватного ключа требует отзыва сертификата",
                "• Хэш-функции должны быть необратимы для безопасности паролей",
                "• Цифровые подписи гарантируют подлинность и целостность",
                "• Квантовые компьютеры угрожают современным алгоритмам"
            ],
            "web": [
                "• SQL Injection позволяет выполнять команды на сервере",
                "• Stored XSS наиболее опасен из-за персистентности",
                "• HttpOnly и Secure флаги защищают cookies",
                "• Rate limiting предотвращает брутфорс API",
                "• CSP ограничивает источники скриптов против XSS"
            ],
            "firewall_ips": [
                "• NGFW анализируют трафик на прикладном уровне",
                "• IPS активно блокирует угрозы, но может вызывать false positives",
                "• Политика 'default deny' - наиболее безопасный подход",
                "• Файрволлы уязвимы как bottleneck при DDoS атаках",
                "• Change control процессы критичны для управления правилами"
            ],
            "cloud_security": [
                "• Модель разделенной ответственности зависит от сервиса (IaaS/PaaS/SaaS)",
                "• Компрометация IAM дает доступ ко всем разрешенным ресурсам",
                "• Customer-managed keys обеспечивают больший контроль над шифрованием",
                "• Misconfigurations - основная причина облачных утечек данных",
                "• Multi-cloud требует единого управления политиками безопасности"
            ]
        }

        points = key_points.get(self.current_scenario, [
            "• Пройдите сценарий для изучения ключевых концепций",
            "• Обращайте внимание на теоретические справки перед вопросами",
            "• Анализируйте подсказки при неправильных ответах"
        ])

        for point in points:
            feedback_text.insert('end', f"{point}\n")

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

        title = ttk.Label(stats_frame, text="📊 Детальная статистика обучения", style='Title.TLabel')
        title.pack(pady=20)

        overall_frame = ttk.Frame(stats_frame)
        overall_frame.pack(pady=10, fill='x')

        score_label = ttk.Label(overall_frame, text=f"🏆 Общий счет: {self.user_score} баллов",
                                style='Score.TLabel')
        score_label.pack()

        progress_frame = ttk.Frame(stats_frame)
        progress_frame.pack(pady=20, fill='x')

        ttk.Label(progress_frame, text="📈 Прогресс по разделам:", font=('Arial', 12, 'bold')).pack(anchor='w')

        scenario_names = {
            "prevention": "🛡️ Предотвращение атак",
            "detection": "🔍 Обнаружение вторжений",
            "response": "🚨 Реакция на инциденты",
            "logfile": "📝 Анализ логов",
            "cryptography": "🔐 Криптография",
            "network": "🌐 Защита сетей",
            "web": "⚡ Веб-безопасность",
            "incident_response": "🔄 Действия при проникновении",
            "firewall_ips": "🛡️ Firewall и IPS",
            "cloud_security": "☁️ Cloud Security"
        }

        for scenario, name in scenario_names.items():
            scenario_frame = ttk.Frame(progress_frame)
            scenario_frame.pack(fill='x', pady=5)

            ttk.Label(scenario_frame, text=name, width=25).pack(side='left')
            progress = ttk.Progressbar(scenario_frame, orient='horizontal', length=200, mode='determinate')

            # Более мягкая система оценки прогресса
            questions_in_scenario = 5  # среднее количество вопросов
            progress_value = min((self.scenario_progress.get(scenario, 0) / questions_in_scenario) * 100, 100)
            progress['value'] = progress_value
            progress.pack(side='left', padx=10)

            percent_label = ttk.Label(scenario_frame, text=f"{progress_value:.0f}%")
            percent_label.pack(side='left')

        recommendations = scrolledtext.ScrolledText(stats_frame, width=80, height=8, font=('Arial', 10))
        recommendations.pack(pady=10, fill='both', expand=True)

        # Улучшенная система рекомендаций
        completed_scenarios = sum(1 for progress in self.scenario_progress.values() if progress > 0)
        total_scenarios = len(self.scenario_progress)

        if completed_scenarios == total_scenarios and self.user_score >= 80:
            rec_text = "🎉 Превосходно! Вы прошли все сценарии с высоким результатом.\nРекомендуется: Практика на реальных CTF-соревнованиях"
        elif completed_scenarios >= total_scenarios * 0.7:
            rec_text = "👍 Хороший прогресс! Продолжайте в том же духе.\nРекомендуется: Закрепить знания в слабых областях"
        else:
            rec_text = "🚀 Начните обучение с основных сценариев защиты сети.\nРекомендуется: Постепенно проходить все разделы"

        weak_scenarios = [scenario for scenario, progress in self.scenario_progress.items()
                          if progress < 2]  # Более мягкий критерий

        if weak_scenarios:
            rec_text += f"\n\nОсобое внимание уделите: {', '.join([scenario_names.get(s, s) for s in weak_scenarios])}"

        recommendations.insert('1.0', f"Рекомендации по обучению:\n\n{rec_text}\n\n")
        recommendations.insert('end', "Советы для эффективного обучения:\n")
        recommendations.insert('end', "• Внимательно читайте теоретические справки перед вопросами\n")
        recommendations.insert('end', "• Анализируйте подсказки при неправильных ответах\n")
        recommendations.insert('end', "• Проходите сценарии несколько раз для закрепления\n")
        recommendations.insert('end', "• Делайте заметки по ключевым концепциям\n")
        recommendations.config(state='disabled')

        back_btn = ttk.Button(stats_frame, text="🔙 Назад",
                              command=self.show_main_menu,
                              style='Game.TButton')
        back_btn.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Расширенный тренажер по кибербезопасности")
    root.geometry("900x700")
    root.configure(bg='#2c3e50')

    app = Theory(root)
    root.mainloop()
