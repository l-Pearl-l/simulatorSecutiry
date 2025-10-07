import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import ipaddress
from datetime import datetime

class InteractiveSecurityTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Интерактивный тренажёр по сетевой безопасности")
        self.root.geometry("1200x800")
        
        self.setup_gui()
        
    def setup_gui(self):
        # Создание вкладок
        self.notebook = ttk.Notebook(self.root)
        
        # Вкладка симуляции сети
        self.network_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.network_frame, text="Симуляция сети")
        
        # Вкладка настройки фаервола
        self.firewall_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.firewall_frame, text="Настройка фаервола")
        
        # Вкладка защиты от атак
        self.defense_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.defense_frame, text="Защита от атак")
        
        self.notebook.pack(expand=True, fill='both')
        
        self.setup_network_simulation()
        self.setup_firewall_config()
        self.setup_attack_defense()
    
    def setup_network_simulation(self):
        # Визуализация сети
        self.network_canvas = tk.Canvas(self.network_frame, width=1000, height=400, bg='white')
        self.network_canvas.pack(pady=10)
        
        # Элементы сети с реальными IP
        self.network_devices = {
            'router': {'x': 100, 'y': 200, 'status': 'secure', 'type': 'router', 'ip': '192.168.1.1'},
            'server': {'x': 300, 'y': 200, 'status': 'secure', 'type': 'server', 'ip': '192.168.1.10'},
            'pc1': {'x': 500, 'y': 100, 'status': 'secure', 'type': 'pc', 'ip': '192.168.1.101'},
            'pc2': {'x': 500, 'y': 300, 'status': 'secure', 'type': 'pc', 'ip': '192.168.1.102'},
            'attacker': {'x': 800, 'y': 200, 'status': 'malicious', 'type': 'hacker', 'ip': '10.0.0.50'}
        }
        
        # Внешние IP для тестирования
        self.external_ips = [
            '203.0.113.15',  # Доверенный IP
            '198.51.100.25', # Подозрительный IP
            '10.0.0.50',     # Атакующий
            '192.168.1.105'  # Новый внутренний IP
        ]
        
        self.draw_network()
        
        # Панель управления
        control_frame = tk.Frame(self.network_frame)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Запустить сканирование", 
                 command=self.start_network_scan).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Обнаружить угрозы", 
                 command=self.detect_threats).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Изолировать угрозу", 
                 command=self.isolate_threat).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Сбросить сеть", 
                 command=self.reset_network).pack(side=tk.LEFT, padx=5)
        
        # Лог событий
        log_frame = tk.Frame(self.network_frame)
        log_frame.pack(pady=10)
        tk.Label(log_frame, text="Лог событий сети:", font=('Arial', 10)).pack()
        self.network_log = tk.Text(log_frame, height=8, width=100)
        self.network_log.pack(pady=5)
    
    def setup_firewall_config(self):
    # Конфигуратор фаервола
        config_frame = tk.Frame(self.firewall_frame)
        config_frame.pack(pady=10)
        
        tk.Label(config_frame, text="Настройка правил межсетевого экрана", font=('Arial', 14, 'bold')).pack()
        
        # Основные настройки фаервола
        settings_frame = tk.LabelFrame(self.firewall_frame, text="Политика по умолчанию")
        settings_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(settings_frame, text="Политика для входящего трафика:").grid(row=0, column=0, sticky='w')
        self.inbound_policy = tk.StringVar(value="deny")
        tk.OptionMenu(settings_frame, self.inbound_policy, "deny", "allow").grid(row=0, column=1, padx=5)
        
        tk.Label(settings_frame, text="Политика для исходящего трафика:").grid(row=0, column=2, sticky='w', padx=20)
        self.outbound_policy = tk.StringVar(value="allow")
        tk.OptionMenu(settings_frame, self.outbound_policy, "deny", "allow").grid(row=0, column=3, padx=5)
        
        # Добавление правил
        rules_frame = tk.LabelFrame(self.firewall_frame, text="Добавить правило")
        rules_frame.pack(pady=10, padx=10, fill='x')
        
        # Строка 1: Направление и действие
        row1 = tk.Frame(rules_frame)
        row1.pack(pady=5)
        
        tk.Label(row1, text="Направление:").pack(side=tk.LEFT)
        self.direction_var = tk.StringVar(value="inbound")
        tk.OptionMenu(row1, self.direction_var, "inbound", "outbound").pack(side=tk.LEFT, padx=5)
        
        tk.Label(row1, text="Действие:").pack(side=tk.LEFT, padx=10)
        self.action_var = tk.StringVar(value="allow")
        tk.OptionMenu(row1, self.action_var, "allow", "deny").pack(side=tk.LEFT, padx=5)
        
        # Строка 2: Протокол и порт
        row2 = tk.Frame(rules_frame)
        row2.pack(pady=5)
        
        tk.Label(row2, text="Протокол:").pack(side=tk.LEFT)
        self.protocol_var = tk.StringVar(value="tcp")
        tk.OptionMenu(row2, self.protocol_var, "tcp", "udp", "icmp", "any").pack(side=tk.LEFT, padx=5)
        
        tk.Label(row2, text="Порт:").pack(side=tk.LEFT, padx=10)
        self.port_entry = tk.Entry(row2, width=10)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row2, text="(0-65535, any для любого)").pack(side=tk.LEFT)
        
        # Строка 3: IP-адреса
        row3 = tk.Frame(rules_frame)
        row3.pack(pady=5)
        
        tk.Label(row3, text="Источник:").pack(side=tk.LEFT)
        self.source_ip = tk.Entry(row3, width=15)
        self.source_ip.pack(side=tk.LEFT, padx=5)
        self.source_ip.insert(0, "any")
        
        tk.Label(row3, text="Назначение:").pack(side=tk.LEFT, padx=10)
        self.dest_ip = tk.Entry(row3, width=15)
        self.dest_ip.pack(side=tk.LEFT, padx=5)
        self.dest_ip.insert(0, "any")
        
        # Кнопки управления правилами
        button_frame = tk.Frame(rules_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Добавить правило", 
                command=self.add_firewall_rule, bg='lightblue').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Удалить последние", 
                command=self.delete_firewall_rule, bg='lightcoral').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить все", 
                command=self.clear_firewall_rules).pack(side=tk.LEFT, padx=5)
        
        # Список правил
        listbox_frame = tk.LabelFrame(self.firewall_frame, text="Текущие правила фаервола")
        listbox_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Заголовки колонок
        headers = ["№", "Направление", "Действие", "Протокол", "Порт", "Источник", "Назначение"]
        for i, header in enumerate(headers):
            tk.Label(listbox_frame, text=header, font=('Arial', 9, 'bold')).grid(row=0, column=i, padx=2, pady=2)
        
        # Прокручиваемый фрейм для правил
        rules_container = tk.Frame(listbox_frame)
        rules_container.grid(row=1, column=0, columnspan=7, sticky='nsew')
        
        self.rules_canvas = tk.Canvas(rules_container, height=200)
        scrollbar = tk.Scrollbar(rules_container, orient="vertical", command=self.rules_canvas.yview)
        self.rules_scrollable_frame = tk.Frame(self.rules_canvas)  # ИСПРАВЛЕНО: правильное название
        
        self.rules_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.rules_canvas.configure(scrollregion=self.rules_canvas.bbox("all"))
        )
        
        self.rules_canvas.create_window((0, 0), window=self.rules_scrollable_frame, anchor="nw")
        self.rules_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.rules_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.firewall_rules = []
        self.rule_widgets = []
        
        # Тестирование фаервола
        test_frame = tk.LabelFrame(self.firewall_frame, text="Тестирование правил")
        test_frame.pack(pady=10, padx=10, fill='x')
        
        test_row1 = tk.Frame(test_frame)
        test_row1.pack(pady=5)
        
        tk.Label(test_row1, text="Тестовое подключение:").pack(side=tk.LEFT)
        
        # Выбор тестового сценария
        test_scenarios = [
            ("Внутренний трафик (PC1 → Server)", "internal"),
            ("Внешний доверенный IP", "trusted_external"),
            ("Внешний подозрительный IP", "suspicious_external"),
            ("Атакующий IP", "attacker")
        ]
        
        self.test_scenario = tk.StringVar(value="internal")
        for text, mode in test_scenarios:
            tk.Radiobutton(test_row1, text=text, variable=self.test_scenario, 
                        value=mode).pack(side=tk.LEFT, padx=10)
        
        test_row2 = tk.Frame(test_frame)
        test_row2.pack(pady=5)
        
        tk.Button(test_row2, text="Протестировать подключение", 
                command=self.test_firewall_connection, bg='lightgreen').pack(side=tk.LEFT, padx=5)
        
        self.test_result = tk.Label(test_frame, text="", font=('Arial', 11), wraplength=800)
        self.test_result.pack(pady=10)
        
    def setup_attack_defense(self):
        # Симулятор атак
        attack_frame = tk.Frame(self.defense_frame)
        attack_frame.pack(pady=10)
        
        tk.Label(attack_frame, text="Симулятор кибератак и защиты", font=('Arial', 14, 'bold')).pack()
        
        # Выбор типа атаки
        self.attack_type = tk.StringVar(value="phishing")
        
        attacks_frame = tk.LabelFrame(self.defense_frame, text="Выбор типа атаки")
        attacks_frame.pack(pady=10, padx=10, fill='x')
        
        attacks = [
            ("Фишинг атака", "phishing"),
            ("DDoS атака", "ddos"),
            ("Атака грубой силы", "bruteforce"),
            ("MITM атака", "mitm"),
            ("Сканирование портов", "port_scan")
        ]
        
        for i, (text, mode) in enumerate(attacks):
            tk.Radiobutton(attacks_frame, text=text, variable=self.attack_type, 
                          value=mode).grid(row=i//2, column=i%2, sticky='w', padx=20, pady=2)
        
        # Кнопки управления
        button_frame = tk.Frame(self.defense_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Запустить атаку", 
                 command=self.launch_attack, bg='red', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Применить защиту", 
                 command=self.apply_defense, bg='green', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить лог", 
                 command=self.clear_attack_log).pack(side=tk.LEFT, padx=5)
        
        # Визуализация атаки
        canvas_frame = tk.LabelFrame(self.defense_frame, text="Визуализация атаки")
        canvas_frame.pack(pady=10, padx=10, fill='x')
        
        self.attack_canvas = tk.Canvas(canvas_frame, width=800, height=250, bg='black')
        self.attack_canvas.pack(pady=5)
        
        # Лог атак
        log_frame = tk.LabelFrame(self.defense_frame, text="Лог атак и защиты")
        log_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.attack_log = tk.Text(log_frame, height=12, width=100)
        scrollbar = tk.Scrollbar(log_frame, command=self.attack_log.yview)
        self.attack_log.configure(yscrollcommand=scrollbar.set)
        self.attack_log.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def add_firewall_rule(self):
        try:
            direction = self.direction_var.get()
            action = self.action_var.get()
            protocol = self.protocol_var.get()
            port = self.port_entry.get().strip()
            source = self.source_ip.get().strip()
            destination = self.dest_ip.get().strip()
            
            # Валидация порта
            if port and port != "any":
                if not port.isdigit() or not (0 <= int(port) <= 65535):
                    raise ValueError("Порт должен быть числом от 0 до 65535")
            
            # Дополнительная проверка для TCP/UDP
            if protocol in ["tcp", "udp"] and not port:
                raise ValueError("Для TCP/USP укажите порт или 'any'")
            
            # Валидация IP-адресов
            if source != "any":
                try:
                    ipaddress.ip_network(source, strict=False)
                except ValueError:
                    raise ValueError("Некорректный IP-адрес источника")
            
            if destination != "any":
                try:
                    ipaddress.ip_network(destination, strict=False)
                except ValueError:
                    raise ValueError("Некорректный IP-адрес назначения")
            
            rule = {
                'direction': direction,
                'action': action,
                'protocol': protocol,
                'port': port if port else "any",
                'source': source,
                'destination': destination
            }
            
            self.firewall_rules.append(rule)
            self.update_rules_display()
            
            # Очистка полей
            self.port_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")  


    def update_rules_display(self):
        """
        Обновляет отображение правил фаервола в интерфейсе
        """
        # Очистка предыдущих виджетов
        for widget in self.rule_widgets:
            widget.destroy()
        self.rule_widgets.clear()
        
        # Отображение новых правил
        for i, rule in enumerate(self.firewall_rules, 1):
            row = i
            
            # Цвет строки в зависимости от действия
            bg_color = 'lightgreen' if rule['action'] == 'allow' else 'lightcoral'
            
            labels = [
                str(i),
                rule['direction'],
                rule['action'], 
                rule['protocol'],
                rule['port'],
                rule['source'],
                rule['destination']
            ]
            
            for col, text in enumerate(labels):
                label = tk.Label(self.rules_scrollable_frame, text=text, bg=bg_color, 
                            relief='solid', borderwidth=1, padx=5, pady=2, font=('Arial', 8))
                label.grid(row=row, column=col, sticky='ew', padx=1, pady=1)
                self.rule_widgets.append(label)
                
    def test_firewall_connection(self):
        scenario = self.test_scenario.get()
        
        # Определение тестовых параметров в зависимости от сценария
        test_cases = {
            "internal": {
                'direction': 'inbound',
                'protocol': 'tcp',
                'port': '80',
                'source': '192.168.1.101',  # PC1
                'destination': '192.168.1.10',  # Server
                'description': 'Внутренний трафик PC1 → Server (порт 80)'
            },
            "trusted_external": {
                'direction': 'inbound', 
                'protocol': 'tcp',
                'port': '443',
                'source': '203.0.113.15',  # Доверенный внешний IP
                'destination': '192.168.1.10',
                'description': 'Внешний доверенный IP → Server (HTTPS)'
            },
            "suspicious_external": {
                'direction': 'inbound',
                'protocol': 'tcp', 
                'port': '22',
                'source': '198.51.100.25',  # Подозрительный IP
                'destination': '192.168.1.10',
                'description': 'Внешний подозрительный IP → Server (SSH)'
            },
            "attacker": {
                'direction': 'inbound',
                'protocol': 'any',
                'port': 'any',
                'source': '10.0.0.50',  # Атакующий
                'destination': 'any',
                'description': 'Атакующий IP → Любой узел сети'
            }
        }
        
        test_case = test_cases[scenario]
        result = self.check_firewall_rules(test_case)
        
        # Формирование результата
        if result['allowed']:
            color = 'green'
            icon = '✅'
            action_text = "РАЗРЕШЕНО"
        else:
            color = 'red' 
            icon = '❌'
            action_text = "БЛОКИРОВАНО"
        
        rule_info = ""
        if result['matched_rule'] is not None:
            rule_info = f"\nСработало правило #{result['matched_rule'] + 1}"
        elif result['default_policy']:
            rule_info = f"\nПрименена политика по умолчанию ({result['default_policy']})"
        
        result_text = f"{icon} {action_text}\n{test_case['description']}{rule_info}"
        self.test_result.config(text=result_text, fg=color)
    
    def check_firewall_rules(self, packet):
        """
        Проверяет пакет по правилам фаервола
        """
        direction = packet['direction']
        protocol = packet['protocol'] 
        port = packet['port']
        source = packet['source']
        destination = packet['destination']
        
        # Сначала проверяем правила
        for i, rule in enumerate(self.firewall_rules):
            # Проверка направления
            if rule['direction'] != direction:
                continue
                
            # Проверка протокола
            if rule['protocol'] != 'any' and rule['protocol'] != protocol:
                continue
                
            # Проверка порта
            if rule['port'] != 'any' and rule['port'] != port:
                continue
                
            # Проверка источника
            if rule['source'] != 'any' and not self.ip_matches(source, rule['source']):
                continue
                
            # Проверка назначения  
            if rule['destination'] != 'any' and not self.ip_matches(destination, rule['destination']):
                continue
                
            # Правило совпало
            return {
                'allowed': (rule['action'] == 'allow'),
                'matched_rule': i,
                'default_policy': None
            }
        
        # Если правила не совпали, применяем политику по умолчанию
        default_policy = self.inbound_policy.get() if direction == 'inbound' else self.outbound_policy.get()
        return {
            'allowed': (default_policy == 'allow'),
            'matched_rule': None,
            'default_policy': default_policy
        }
    
    def ip_matches(self, ip, rule_ip):
        """
        Проверяет, соответствует ли IP адрес правилу
        """
        if rule_ip == 'any':
            return True
            
        try:
            ip_obj = ipaddress.ip_address(ip)
            network_obj = ipaddress.ip_network(rule_ip, strict=False)
            return ip_obj in network_obj
        except ValueError:
            return False
    
    def delete_firewall_rule(self):
        if not self.firewall_rules:
            messagebox.showinfo("Инфо", "Нет правил для удаления")
            return
            
        if self.firewall_rules:
            # В реальном приложении здесь бы был выбор конкретного правила
            # Для простоты удаляем последнее правило
            self.firewall_rules.pop()
            self.update_rules_display()
            self.log_attack_event("🗑️ Удалено последнее правило фаервола")
    
    def clear_firewall_rules(self):
        if self.firewall_rules:
            self.firewall_rules.clear()
            self.update_rules_display()
            self.log_attack_event("🧹 Все правила фаервола очищены")
    
    def draw_network(self):
        self.network_canvas.delete("all")
        
        colors = {
            'secure': '#90EE90',      # Светло-зеленый
            'infected': '#FFB6C1',    # Светло-красный
            'malicious': '#FFD700',   # Золотой
            'protected': '#87CEEB'    # Светло-синий
        }
        
        outlines = {
            'secure': 'darkgreen',
            'infected': 'darkred', 
            'malicious': 'darkorange',
            'protected': 'darkblue'
        }
        
        for device, info in self.network_devices.items():
            x, y = info['x'], info['y']
            color = colors[info['status']]
            outline = outlines[info['status']]
            
            if info['type'] == 'router':
                # Рисуем роутер
                self.network_canvas.create_rectangle(x-25, y-20, x+25, y+20, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="🔄", font=('Arial', 14))
                # Антенны
                self.network_canvas.create_line(x-15, y-20, x-15, y-40, width=2, fill=outline)
                self.network_canvas.create_line(x+15, y-20, x+15, y-40, width=2, fill=outline)
                
            elif info['type'] == 'server':
                # Рисуем сервер
                self.network_canvas.create_rectangle(x-30, y-25, x+30, y+25, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="🖥️", font=('Arial', 16))
                # Индикаторы
                for i in range(3):
                    self.network_canvas.create_oval(x+15, y-15+i*10, x+20, y-10+i*10, fill='green')
                
            elif info['type'] == 'pc':
                # Рисуем компьютер
                self.network_canvas.create_rectangle(x-20, y-15, x+20, y+15, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="💻", font=('Arial', 12))
                
            elif info['type'] == 'hacker':
                # Рисуем хакера
                self.network_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="⚡", font=('Arial', 14))
            
            # Подпись устройства с IP
            self.network_canvas.create_text(x, y+40, text=f"{device}\n{info['ip']}", 
                                          font=('Arial', 8), fill='black')
        
        # Рисуем соединения
        connections = [
            (100, 200, 300, 200),  # router -> server
            (300, 200, 500, 100),  # server -> pc1
            (300, 200, 500, 300),  # server -> pc2
            (800, 200, 600, 200),  # attacker -> сеть
        ]
        
        for x1, y1, x2, y2 in connections:
            self.network_canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, 
                                          dash=(4, 2), width=2, fill='gray')
    
    def start_network_scan(self):
        self.log_network_event("🔍 Запуск сканирования сети на наличие уязвимостей...")
        
        # Симуляция сканирования с прогрессом
        devices = ['router', 'server', 'pc1', 'pc2']
        for i, device in enumerate(devices):
            progress = (i + 1) * 25
            self.log_network_event(f"📡 Сканирование {device} ({progress}%)...")
            self.root.update()
            self.root.after(800)  # Задержка для наглядности
            
            # 30% шанс обнаружения угрозы
            if random.random() < 0.3:
                self.network_devices[device]['status'] = 'infected'
                self.log_network_event(f"⚠️ ОБНАРУЖЕНА УГРОЗА на устройстве {device}!")
                # Подсветка зараженного устройства
                self.highlight_device(device, 'red')
            else:
                self.log_network_event(f"✅ {device} безопасен")
                self.highlight_device(device, 'green')
            
            self.draw_network()
            self.root.update()
        
        self.log_network_event("✅ Сканирование завершено")
    
    def detect_threats(self):
        threats = [dev for dev, info in self.network_devices.items() 
                  if info['status'] in ['infected', 'malicious']]
        
        if threats:
            self.log_network_event(f"🚨 СИСТЕМА ОБНАРУЖЕНИЯ: найдены угрозы: {', '.join(threats)}")
            for threat in threats:
                self.log_network_event(f"🔴 Угроза: {threat} ({self.network_devices[threat]['ip']})")
                self.highlight_device(threat, 'red')
        else:
            self.log_network_event("✅ Угроз не обнаружено")
    
    def isolate_threat(self):
        isolated_count = 0
        for device, info in self.network_devices.items():
            if info['status'] == 'infected':
                info['status'] = 'protected'
                self.log_network_event(f"🛡️ Устройство {device} изолировано от сети")
                self.highlight_device(device, 'blue')
                isolated_count += 1
        
        if isolated_count == 0:
            self.log_network_event("ℹ️ Нет активных угроз для изоляции")
        else:
            self.log_network_event(f"✅ Изолировано угроз: {isolated_count}")
        
        self.draw_network()
    
    def reset_network(self):
        for device in ['router', 'server', 'pc1', 'pc2']:
            self.network_devices[device]['status'] = 'secure'
        self.network_devices['attacker']['status'] = 'malicious'
        self.log_network_event("🔄 Сеть сброшена в исходное состояние")
        self.draw_network()
    
    def launch_attack(self):
        attack_type = self.attack_type.get()
        attack_names = {
            "phishing": "Фишинг атака",
            "ddos": "DDoS атака", 
            "bruteforce": "Атака грубой силы",
            "mitm": "MITM атака",
            "port_scan": "Сканирование портов"
        }
        
        self.log_attack_event(f"🔥 ЗАПУСК АТАКИ: {attack_names[attack_type]}")
        self.attack_canvas.delete("all")
        
        if attack_type == "ddos":
            self.simulate_ddos()
        elif attack_type == "phishing":
            self.simulate_phishing()
        elif attack_type == "bruteforce":
            self.simulate_bruteforce()
        elif attack_type == "mitm":
            self.simulate_mitm()
        elif attack_type == "port_scan":
            self.simulate_port_scan()
    
    def apply_defense(self):
        attack_type = self.attack_type.get()
        defenses = {
            "ddos": "Настройка DDoS защиты, лимитов трафика и CDN",
            "phishing": "Обучение сотрудников, фильтрация email, двухфакторная аутентификация",
            "bruteforce": "Сильные пароли, ограничение попыток входа, CAPTCHA",
            "mitm": "SSL/TLS шифрование, VPN, certificate pinning",
            "port_scan": "Скрытие портов, фаервол, IDS/IPS системы"
        }
        
        self.log_attack_event(f"🛡️ ПРИМЕНЕНА ЗАЩИТА: {defenses[attack_type]}")
        self.attack_canvas.delete("all")
        self.attack_canvas.create_text(400, 125, text="АТАКА ОТБИТА", 
                                      font=('Arial', 24, 'bold'), fill='green')
        self.attack_canvas.create_text(400, 160, text="Система защищена", 
                                      font=('Arial', 12), fill='lightgreen')
    
    def clear_attack_log(self):
        self.attack_log.delete(1.0, tk.END)
        self.log_attack_event("🧹 Лог очищен")
    
    def simulate_ddos(self):
        self.log_attack_event("🎯 Цель: перегрузить сервер фальшивыми запросами")
        
        # Сервер в центре
        server_x, server_y = 400, 125
        self.attack_canvas.create_oval(server_x-20, server_y-20, server_x+20, server_y+20, 
                                      fill='red', outline='darkred')
        self.attack_canvas.create_text(server_x, server_y, text="🖥️", font=('Arial', 12))
        self.attack_canvas.create_text(server_x, server_y+30, text="СЕРВЕР", fill='white')
        
        # Атака множественными запросами
        for i in range(30):  # Уменьшил количество для скорости
            x = random.randint(50, 750)
            y = random.randint(50, 200)
            # Линия от атакующего к серверу
            self.attack_canvas.create_line(x, y, server_x, server_y, fill='red', width=1, dash=(2,1), tags="ddos")
            # Точка атаки
            self.attack_canvas.create_oval(x-2, y-2, x+2, y+2, fill='orange', tags="ddos")
            self.attack_canvas.update()
            self.root.after(50)
        
        self.log_attack_event("💥 Сервер перегружен! DDoS атака успешна")
    
    def simulate_phishing(self):
        self.log_attack_event("🎯 Цель: обман пользователей для получения данных")
        
        messages = [
            "🔓 СРОЧНО: Ваш аккаунт будет заблокирован!",
            "🎁 ВЫ ВЫИГРАЛИ: Нажмите для получения приза!",
            "🔐 ТРЕБУЕТСЯ: Обновление безопасности",
            "📧 ПОДТВЕРЖДЕНИЕ: Проверьте свои данные"
        ]
        
        y_pos = 50
        for msg in messages:
            self.attack_canvas.create_text(400, y_pos, text=msg, 
                                          font=('Arial', 12, 'bold'), fill='yellow', tags="phishing")
            self.attack_canvas.create_text(400, y_pos+20, text="⬇️ НАЖМИТЕ ЗДЕСЬ ⬇️", 
                                          font=('Arial', 10), fill='red', tags="phishing")
            y_pos += 60
            self.attack_canvas.update()
            self.root.after(1000)
        
        self.log_attack_event("📧 Фишинг письма отправлены! Ожидание жертв...")
    
    def simulate_bruteforce(self):
        self.log_attack_event("🎯 Цель: подбор пароля методом грубой силы")
        
        passwords = ["123456", "password", "admin", "qwerty", "12345678", 
                    "111111", "123123", "admin123", "letmein", "welcome"]
        
        target_x, target_y = 400, 100
        self.attack_canvas.create_rectangle(target_x-40, target_y-20, target_x+40, target_y+20, 
                                          fill='darkred', outline='white', tags="bruteforce")
        self.attack_canvas.create_text(target_x, target_y, text="🔐", font=('Arial', 14), tags="bruteforce")
        self.attack_canvas.create_text(target_x, target_y+30, text="СИСТЕМА", fill='white', tags="bruteforce")
        
        for i, pwd in enumerate(passwords):
            x = 100 + (i % 5) * 150
            y = 180 + (i // 5) * 30
            
            self.attack_canvas.create_text(x, y, text=f"Попытка: {pwd}", 
                                          font=('Arial', 9), fill='orange', anchor='w', tags="bruteforce")
            # Линия атаки
            self.attack_canvas.create_line(x, y-10, target_x, target_y+20, 
                                          fill='red', width=1, dash=(1,1), tags="bruteforce")
            self.attack_canvas.update()
            self.root.after(300)
        
        self.log_attack_event("💥 Пароль '123456' подобран! Доступ получен")
    
    def simulate_mitm(self):
        self.log_attack_event("🎯 Цель: перехват трафика между клиентом и сервером")
        
        # Позиции участников
        client_x, client_y = 200, 125
        hacker_x, hacker_y = 400, 175
        server_x, server_y = 600, 125
        
        # Участники
        self.attack_canvas.create_rectangle(client_x-25, client_y-20, client_x+25, client_y+20, 
                                          fill='lightblue', outline='blue', tags="mitm")
        self.attack_canvas.create_text(client_x, client_y, text="👤", font=('Arial', 12), tags="mitm")
        self.attack_canvas.create_text(client_x, client_y+30, text="КЛИЕНТ", fill='white', tags="mitm")
        
        self.attack_canvas.create_oval(hacker_x-25, hacker_y-20, hacker_x+25, hacker_y+20, 
                                     fill='red', outline='darkred', tags="mitm")
        self.attack_canvas.create_text(hacker_x, hacker_y, text="⚡", font=('Arial', 14), tags="mitm")
        self.attack_canvas.create_text(hacker_x, hacker_y+30, text="ХАКЕР", fill='white', tags="mitm")
        
        self.attack_canvas.create_rectangle(server_x-30, server_y-25, server_x+30, server_y+25, 
                                          fill='lightgreen', outline='green', tags="mitm")
        self.attack_canvas.create_text(server_x, server_y, text="🖥️", font=('Arial', 14), tags="mitm")
        self.attack_canvas.create_text(server_x, server_y+35, text="СЕРВЕР", fill='white', tags="mitm")
        
        # Анимация перехвата
        for i in range(2):  # Уменьшил количество циклов
            # Прямое соединение (исходное)
            direct_line = self.attack_canvas.create_line(client_x+25, client_y, server_x-30, server_y, 
                                                       arrow=tk.BOTH, fill='green', width=2, tags="mitm")
            self.attack_canvas.create_text(400, 80, text="Легальное соединение", fill='green', tags="mitm")
            self.attack_canvas.update()
            self.root.after(800)
            self.attack_canvas.delete(direct_line)
            
            # Перехваченное соединение
            hack_line1 = self.attack_canvas.create_line(client_x+25, client_y, hacker_x, hacker_y-20, 
                                                      arrow=tk.LAST, fill='red', width=2, tags="mitm")
            hack_line2 = self.attack_canvas.create_line(hacker_x, hacker_y+20, server_x-30, server_y, 
                                                      arrow=tk.LAST, fill='red', width=2, tags="mitm")
            self.attack_canvas.create_text(400, 80, text="ПЕРЕХВАЧЕНО!", fill='red', font=('Arial', 12, 'bold'), tags="mitm")
            self.attack_canvas.update()
            self.root.after(800)
            self.attack_canvas.delete(hack_line1, hack_line2)
        
        self.log_attack_event("📡 Трафик перехвачен! MITM атака успешна")
    
    def simulate_port_scan(self):
        self.log_attack_event("🎯 Цель: обнаружение открытых портов системы")
        
        target_x, target_y = 400, 125
        self.attack_canvas.create_rectangle(target_x-50, target_y-30, target_x+50, target_y+30, 
                                          fill='gray', outline='white', tags="portscan")
        self.attack_canvas.create_text(target_x, target_y, text="🎯", font=('Arial', 16), tags="portscan")
        self.attack_canvas.create_text(target_x, target_y+40, text="ЦЕЛЕВОЙ СЕРВЕР", fill='white', tags="portscan")
        
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 3389, 8080]
        open_ports = random.sample(ports, 3)  # Случайные открытые порты
        
        for i, port in enumerate(ports):
            x = 100 + (i % 5) * 160
            y = 180 + (i // 5) * 40
            
            if port in open_ports:
                # Открытый порт
                color = 'red'
                status = "ОТКРЫТ"
                self.attack_canvas.create_line(x, y, target_x, target_y, fill='red', width=2, tags="portscan")
            else:
                # Закрытый порт
                color = 'gray'
                status = "закрыт"
                self.attack_canvas.create_line(x, y, target_x, target_y, fill='gray', width=1, dash=(2,2), tags="portscan")
            
            self.attack_canvas.create_rectangle(x-25, y-15, x+25, y+15, fill=color, outline='white', tags="portscan")
            self.attack_canvas.create_text(x, y, text=f"Порт {port}", font=('Arial', 8), fill='white', tags="portscan")
            self.attack_canvas.create_text(x, y+20, text=status, font=('Arial', 7), fill='white', tags="portscan")
            self.attack_canvas.update()
            self.root.after(400)
        
        self.log_attack_event(f"🔍 Найдены открытые порты: {', '.join(map(str, open_ports))}")
    
    def highlight_device(self, device, color='yellow'):
        info = self.network_devices[device]
        x, y = info['x'], info['y']
        
        for i in range(3):
            highlight_id = self.network_canvas.create_oval(x-35, y-35, x+35, y+35, 
                                                         outline=color, width=3, tags="highlight")
            self.network_canvas.update()
            self.root.after(300)
            self.network_canvas.delete(highlight_id)
    
    def log_network_event(self, event):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.network_log.insert(tk.END, f"[{timestamp}] {event}\n")
        self.network_log.see(tk.END)
    
    def log_attack_event(self, event):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.attack_log.insert(tk.END, f"[{timestamp}] {event}\n")
        self.attack_log.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveSecurityTrainer(root)
    root.mainloop()