import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress

class FirewallModule:
    def __init__(self):
        self.frame = None
        self.network_module = None
        self.current_device = 'router'
        
        # Правила для каждого устройства {device_name: [rules]}
        self.device_rules = {
            'router': [],
            'server': [], 
            'pc1': [],
            'pc2': [],
            'attacker': []
        }
        
        # GUI элементы
        self.rules_canvas = None
        self.rules_scrollable_frame = None
        self.rule_widgets = []
        
        # Переменные для формы
        self.direction_var = None
        self.action_var = None
        self.protocol_var = None
        self.port_entry = None
        self.source_ip = None
        self.dest_ip = None
        
        self.test_scenario = None
        self.test_result = None
    
    def set_network_module(self, network_module):
        self.network_module = network_module
    
    def get_frame(self, parent):
        if not self.frame:
            self.frame = ttk.Frame(parent)
            self.setup_firewall_gui()
        return self.frame
    
    def setup_firewall_gui(self):
        # Заголовок
        title_frame = tk.Frame(self.frame)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Настройка фаерволлов устройств", 
                font=('Arial', 14, 'bold')).pack()
        
        # Выбор устройства
        device_frame = tk.LabelFrame(self.frame, text="Выбор устройства")
        device_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(device_frame, text="Устройство:").pack(side='left')
        self.device_var = tk.StringVar(value='router')
        devices = ['router', 'server', 'pc1', 'pc2']
        tk.OptionMenu(device_frame, self.device_var, *devices, 
                     command=self.on_device_change).pack(side='left', padx=10)
        
        # Статус устройства
        self.device_status = tk.Label(device_frame, text="", font=('Arial', 10))
        self.device_status.pack(side='left', padx=20)
        
        # Форма добавления правил
        self.setup_rules_form()
        
        # Список правил
        self.setup_rules_list()
        
        # Тестирование
        self.setup_testing()
        
        # Загружаем правила для выбранного устройства
        self.on_device_change('router')
    
    def setup_rules_form(self):
        rules_form = tk.LabelFrame(self.frame, text="Добавить правило фаервола")
        rules_form.pack(pady=10, padx=10, fill='x')
        
        # Строка 1: Направление и действие
        row1 = tk.Frame(rules_form)
        row1.pack(pady=5)
        
        tk.Label(row1, text="Направление:").pack(side=tk.LEFT)
        self.direction_var = tk.StringVar(value="inbound")
        tk.OptionMenu(row1, self.direction_var, "inbound", "outbound").pack(side=tk.LEFT, padx=5)
        
        tk.Label(row1, text="Действие:").pack(side=tk.LEFT, padx=10)
        self.action_var = tk.StringVar(value="allow")
        tk.OptionMenu(row1, self.action_var, "allow", "deny").pack(side=tk.LEFT, padx=5)
        
        # Строка 2: Протокол и порт
        row2 = tk.Frame(rules_form)
        row2.pack(pady=5)
        
        tk.Label(row2, text="Протокол:").pack(side=tk.LEFT)
        self.protocol_var = tk.StringVar(value="tcp")
        tk.OptionMenu(row2, self.protocol_var, "tcp", "udp", "icmp", "any").pack(side=tk.LEFT, padx=5)
        
        tk.Label(row2, text="Порт:").pack(side=tk.LEFT, padx=10)
        self.port_entry = tk.Entry(row2, width=10)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row2, text="(0-65535, any для любого)").pack(side=tk.LEFT)
        
        # Строка 3: IP-адреса
        row3 = tk.Frame(rules_form)
        row3.pack(pady=5)
        
        tk.Label(row3, text="Источник:").pack(side=tk.LEFT)
        self.source_ip = tk.Entry(row3, width=15)
        self.source_ip.pack(side=tk.LEFT, padx=5)
        self.source_ip.insert(0, "any")
        
        tk.Label(row3, text="Назначение:").pack(side=tk.LEFT, padx=10)
        self.dest_ip = tk.Entry(row3, width=15)
        self.dest_ip.pack(side=tk.LEFT, padx=5)
        self.dest_ip.insert(0, "any")
        
        # Кнопки управления
        button_frame = tk.Frame(rules_form)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Добавить правило", 
                 command=self.add_firewall_rule, bg='lightblue').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Удалить последнее", 
                 command=self.delete_firewall_rule, bg='lightcoral').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить все", 
                 command=self.clear_firewall_rules).pack(side=tk.LEFT, padx=5)
    
    def setup_rules_list(self):
        listbox_frame = tk.LabelFrame(self.frame, text="Правила фаервола устройства")
        listbox_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Заголовки колонок
        headers = ["№", "Направление", "Действие", "Протокол", "Порт", "Источник", "Назначение"]
        for i, header in enumerate(headers):
            tk.Label(listbox_frame, text=header, font=('Arial', 9, 'bold')).grid(row=0, column=i, padx=2, pady=2)
        
        # Прокручиваемый фрейм для правил
        rules_container = tk.Frame(listbox_frame)
        rules_container.grid(row=1, column=0, columnspan=7, sticky='nsew')
        
        self.rules_canvas = tk.Canvas(rules_container, height=150)
        scrollbar = tk.Scrollbar(rules_container, orient="vertical", command=self.rules_canvas.yview)
        self.rules_scrollable_frame = tk.Frame(self.rules_canvas)
        
        self.rules_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.rules_canvas.configure(scrollregion=self.rules_canvas.bbox("all"))
        )
        
        self.rules_canvas.create_window((0, 0), window=self.rules_scrollable_frame, anchor="nw")
        self.rules_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.rules_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_testing(self):
        test_frame = tk.LabelFrame(self.frame, text="Тестирование фаервола")
        test_frame.pack(pady=10, padx=10, fill='x')
        
        test_row1 = tk.Frame(test_frame)
        test_row1.pack(pady=5)
        
        tk.Label(test_row1, text="Тестовый сценарий:").pack(side=tk.LEFT)
        
        test_scenarios = [
            ("Внутренняя атака (PC1 → Устройство)", "internal"),
            ("Внешняя атака (Хакер → Устройство)", "external"),
            ("Веб-атака (порт 80)", "web"),
            ("SSH атака (порт 22)", "ssh")
        ]
        
        self.test_scenario = tk.StringVar(value="internal")
        for text, mode in test_scenarios:
            tk.Radiobutton(test_row1, text=text, variable=self.test_scenario, 
                          value=mode).pack(side=tk.LEFT, padx=10)
        
        test_row2 = tk.Frame(test_frame)
        test_row2.pack(pady=5)
        
        tk.Button(test_row2, text="Протестировать фаерволл", 
                 command=self.test_firewall, bg='lightgreen').pack(side=tk.LEFT, padx=5)
        
        self.test_result = tk.Label(test_frame, text="", font=('Arial', 11), wraplength=800)
        self.test_result.pack(pady=10)
    
    def on_device_change(self, device_name):
        """При смене устройства"""
        self.current_device = device_name
        self.device_status.config(text=f"Правил: {len(self.device_rules[device_name])}")
        self.update_rules_display()
    
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
            
            self.device_rules[self.current_device].append(rule)
            self.update_rules_display()
            
            # Обновляем правила в сетевом модуле
            if self.network_module:
                self.network_module.set_device_firewall_rules(
                    self.current_device, 
                    self.device_rules[self.current_device]
                )
            
            # Очистка полей
            self.port_entry.delete(0, tk.END)
            self.device_status.config(text=f"Правил: {len(self.device_rules[self.current_device])}")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
    
    def update_rules_display(self):
        # Очистка предыдущих виджетов
        for widget in self.rule_widgets:
            widget.destroy()
        self.rule_widgets = []
        
        # Отображение правил текущего устройства
        for i, rule in enumerate(self.device_rules[self.current_device], 1):
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
    
    def delete_firewall_rule(self):
        if not self.device_rules[self.current_device]:
            messagebox.showinfo("Инфо", "Нет правил для удаления")
            return
            
        self.device_rules[self.current_device].pop()
        self.update_rules_display()
        
        if self.network_module:
            self.network_module.set_device_firewall_rules(
                self.current_device, 
                self.device_rules[self.current_device]
            )
        
        self.device_status.config(text=f"Правил: {len(self.device_rules[self.current_device])}")
    
    def clear_firewall_rules(self):
        if not self.device_rules[self.current_device]:
            messagebox.showinfo("Инфо", "Нет правил для очистки")
            return
            
        self.device_rules[self.current_device].clear()
        self.update_rules_display()
        
        if self.network_module:
            self.network_module.set_device_firewall_rules(
                self.current_device, 
                self.device_rules[self.current_device]
            )
        
        self.device_status.config(text=f"Правил: {len(self.device_rules[self.current_device])}")
    
    def test_firewall(self):
        scenario = self.test_scenario.get()
        current_device_ip = self.get_device_ip(self.current_device)
        
        # Определение тестовых параметров
        test_cases = {
            "internal": {
                'source_ip': '192.168.1.101',  # PC1
                'target_ip': current_device_ip,
                'port': 80,
                'protocol': 'tcp',
                'description': f'Внутренняя атака PC1 → {self.current_device} (порт 80)'
            },
            "external": {
                'source_ip': '10.0.0.50',  # Хакер
                'target_ip': current_device_ip, 
                'port': 443,
                'protocol': 'tcp',
                'description': f'Внешняя атака Хакер → {self.current_device} (HTTPS)'
            },
            "web": {
                'source_ip': '10.0.0.50',
                'target_ip': current_device_ip,
                'port': 80,
                'protocol': 'tcp', 
                'description': f'Веб-атака на {self.current_device} (порт 80)'
            },
            "ssh": {
                'source_ip': '10.0.0.50',
                'target_ip': current_device_ip,
                'port': 22,
                'protocol': 'tcp',
                'description': f'SSH атака на {self.current_device} (порт 22)'
            }
        }
        
        test_case = test_cases[scenario]
        
        # Проверяем через фаерволл устройства
        if self.network_module:
            allowed = self.network_module.check_device_firewall(self.current_device, test_case)
            
            if allowed:
                color = 'red'
                icon = '⚠️'
                action_text = "ПРОПУЩЕНО"
                details = "Фаерволл разрешил атаку!"
            else:
                color = 'green'
                icon = '✅'
                action_text = "БЛОКИРОВАНО" 
                details = "Фаерволл заблокировал атаку!"
            
            result_text = f"{icon} {action_text}\n{test_case['description']}\n{details}"
            self.test_result.config(text=result_text, fg=color)
    
    def get_device_ip(self, device_name):
        """Возвращает IP устройства"""
        device_ips = {
            'router': '192.168.1.1',
            'server': '192.168.1.10',
            'pc1': '192.168.1.101', 
            'pc2': '192.168.1.102',
            'attacker': '10.0.0.50'
        }
        return device_ips.get(device_name, '192.168.1.1')