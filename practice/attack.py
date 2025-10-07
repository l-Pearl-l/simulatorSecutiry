import tkinter as tk
from tkinter import ttk
import random
import time
from datetime import datetime

class AttackModule:
    def __init__(self):
        self.frame = None
        self.firewall_module = None
        self.network_module = None
        
        self.attack_canvas = None
        self.attack_log = None
        self.attack_type = None
        self.result_label = None
    
    def set_firewall_module(self, firewall_module):
        self.firewall_module = firewall_module
    
    def set_network_module(self, network_module):
        self.network_module = network_module
    
    def get_frame(self, parent):
        if not self.frame:
            self.frame = ttk.Frame(parent)
            self.setup_attack_gui()
        return self.frame
    
    def setup_attack_gui(self):
        # Заголовок
        title_frame = tk.Frame(self.frame)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Симулятор кибератак и защиты", 
                font=('Arial', 14, 'bold')).pack()
        
        # Выбор атаки и цели
        attack_config = tk.LabelFrame(self.frame, text="Настройка атаки")
        attack_config.pack(pady=10, padx=10, fill='x')
        
        # Выбор типа атаки
        type_frame = tk.Frame(attack_config)
        type_frame.pack(pady=5)
        
        tk.Label(type_frame, text="Тип атаки:").pack(side=tk.LEFT)
        self.attack_type = tk.StringVar(value="port_scan")
        
        attacks = [
            ("Сканирование портов", "port_scan"),
            ("DDoS атака", "ddos"),
            ("Фишинг атака", "phishing"),
            ("Атака грубой силы", "bruteforce"),
            ("MITM атака", "mitm")
        ]
        
        for text, mode in attacks:
            tk.Radiobutton(type_frame, text=text, variable=self.attack_type, 
                          value=mode).pack(side=tk.LEFT, padx=5)
        
        # Выбор цели
        target_frame = tk.Frame(attack_config)
        target_frame.pack(pady=5)
        
        tk.Label(target_frame, text="Цель атаки:").pack(side=tk.LEFT)
        self.target_var = tk.StringVar(value="server")
        targets = ['router', 'server', 'pc1', 'pc2']
        tk.OptionMenu(target_frame, self.target_var, *targets).pack(side=tk.LEFT, padx=10)
        
        # Кнопки управления
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Запустить атаку", 
                 command=self.launch_attack, bg='red', fg='white', 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Применить защиту", 
                 command=self.apply_defense, bg='green', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить лог", 
                 command=self.clear_attack_log).pack(side=tk.LEFT, padx=5)
        
        # Визуализация атаки
        canvas_frame = tk.LabelFrame(self.frame, text="Визуализация атаки")
        canvas_frame.pack(pady=10, padx=10, fill='x')
        
        self.attack_canvas = tk.Canvas(canvas_frame, width=800, height=250, bg='black')
        self.attack_canvas.pack(pady=5)
        
        # Результат атаки
        self.result_label = tk.Label(self.frame, text="", font=('Arial', 12), wraplength=800)
        self.result_label.pack(pady=5)
        
        # Лог атак
        log_frame = tk.LabelFrame(self.frame, text="Лог атак и защиты")
        log_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.attack_log = tk.Text(log_frame, height=10, width=100)
        scrollbar = tk.Scrollbar(log_frame, command=self.attack_log.yview)
        self.attack_log.configure(yscrollcommand=scrollbar.set)
        self.attack_log.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def launch_attack(self):
        attack_type = self.attack_type.get()
        target_device = self.target_var.get()
        
        attack_names = {
            "phishing": "Фишинг атака",
            "ddos": "DDoS атака", 
            "bruteforce": "Атака грубой силы",
            "mitm": "MITM атака",
            "port_scan": "Сканирование портов"
        }
        
        self.log_attack_event(f"🔥 ЗАПУСК АТАКИ: {attack_names[attack_type]} на {target_device}")
        self.attack_canvas.delete("all")
        
        # Создаем пакет атаки
        attack_packet = self.create_attack_packet(attack_type, target_device)
        
        # Проверяем фаерволл целевого устройства
        if self.network_module:
            allowed = self.network_module.check_device_firewall(target_device, attack_packet)
            
            if allowed:
                self.result_label.config(text="✅ Атака ПРОШЛА через фаерволл!", fg='red')
                self.log_attack_event("⚠️ Атака успешна! Фаерволл не заблокировал.")
            else:
                self.result_label.config(text="❌ Атака БЛОКИРОВАНА фаерволлом!", fg='green') 
                self.log_attack_event("🛡️ Атака заблокирована фаерволлом!")
        
        # Запускаем визуализацию атаки
        if attack_type == "ddos":
            self.simulate_ddos(target_device)
        elif attack_type == "phishing":
            self.simulate_phishing(target_device)
        elif attack_type == "bruteforce":
            self.simulate_bruteforce(target_device)
        elif attack_type == "mitm":
            self.simulate_mitm(target_device)
        elif attack_type == "port_scan":
            self.simulate_port_scan(target_device)
    
    def create_attack_packet(self, attack_type, target_device):
        """Создает пакет атаки для проверки фаерволлом"""
        target_ips = {
            'router': '192.168.1.1',
            'server': '192.168.1.10',
            'pc1': '192.168.1.101',
            'pc2': '192.168.1.102'
        }
        
        base_packet = {
            'source_ip': '10.0.0.50',  # Атакующий
            'target_ip': target_ips.get(target_device, '192.168.1.1'),
            'protocol': 'tcp'
        }
        
        # Настройки для разных типов атак
        attack_configs = {
            "ddos": {'port': 80, 'description': 'DDoS на веб-сервер'},
            "phishing": {'port': 443, 'description': 'Фишинг через HTTPS'},
            "bruteforce": {'port': 22, 'description': 'Подбор пароля SSH'},
            "mitm": {'port': 8080, 'description': 'Перехват трафика'},
            "port_scan": {'port': 0, 'description': 'Сканирование портов'}
        }
        
        config = attack_configs.get(attack_type, {'port': 80, 'description': 'Общая атака'})
        base_packet['port'] = config['port']
        base_packet['description'] = config['description']
        
        return base_packet
    
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
        self.result_label.config(text="🛡️ Защита применена успешно!", fg='blue')
    
    def clear_attack_log(self):
        self.attack_log.delete(1.0, tk.END)
        self.log_attack_event("🧹 Лог очищен")
    
    def simulate_ddos(self, target_device):
        self.log_attack_event(f"🎯 Цель DDoS: перегрузить {target_device}")
        
        target_x, target_y = 400, 125
        self.attack_canvas.create_oval(target_x-20, target_y-20, target_x+20, target_y+20, 
                                      fill='red', outline='darkred')
        self.attack_canvas.create_text(target_x, target_y, text="🎯", font=('Arial', 12))
        self.attack_canvas.create_text(target_x, target_y+30, text=target_device.upper(), fill='white')
        
        for i in range(20):
            x = random.randint(50, 750)
            y = random.randint(50, 200)
            self.attack_canvas.create_line(x, y, target_x, target_y, fill='red', width=1, 
                                          dash=(2,1), tags="ddos")
            self.attack_canvas.create_oval(x-2, y-2, x+2, y+2, fill='orange', tags="ddos")
            self.attack_canvas.update()
            self.frame.after(50)
    
    def simulate_phishing(self, target_device):
        self.log_attack_event(f"🎯 Цель фишинга: обмануть пользователей {target_device}")
        
        messages = [
            "🔓 СРОЧНО: Ваш аккаунт будет заблокирован!",
            "🎁 ВЫ ВЫИГРАЛИ: Нажмите для получения приза!",
            f"🔐 {target_device}: Требуется обновление безопасности"
        ]
        
        y_pos = 50
        for msg in messages:
            self.attack_canvas.create_text(400, y_pos, text=msg, 
                                          font=('Arial', 12, 'bold'), fill='yellow', tags="phishing")
            self.attack_canvas.create_text(400, y_pos+20, text="⬇️ НАЖМИТЕ ЗДЕСЬ ⬇️", 
                                          font=('Arial', 10), fill='red', tags="phishing")
            y_pos += 60
            self.attack_canvas.update()
            self.frame.after(1000)
    
    def simulate_bruteforce(self, target_device):
        self.log_attack_event(f"🎯 Цель brute-force: подобрать пароль {target_device}")
        
        passwords = ["123456", "password", "admin", target_device, "qwerty"]
        
        target_x, target_y = 400, 100
        self.attack_canvas.create_rectangle(target_x-40, target_y-20, target_x+40, target_y+20, 
                                          fill='darkred', outline='white', tags="bruteforce")
        self.attack_canvas.create_text(target_x, target_y, text="🔐", font=('Arial', 14), tags="bruteforce")
        self.attack_canvas.create_text(target_x, target_y+30, text=target_device.upper(), fill='white', tags="bruteforce")
        
        for i, pwd in enumerate(passwords):
            x = 100 + (i % 4) * 180
            y = 180
            
            self.attack_canvas.create_text(x, y, text=f"Пароль: {pwd}", 
                                          font=('Arial', 9), fill='orange', tags="bruteforce")
            self.attack_canvas.create_line(x, y-10, target_x, target_y+20, 
                                          fill='red', width=1, tags="bruteforce")
            self.attack_canvas.update()
            self.frame.after(500)
    
    def simulate_mitm(self, target_device):
        self.log_attack_event(f"🎯 Цель MITM: перехватить трафик {target_device}")
        
        client_x, client_y = 200, 125
        hacker_x, hacker_y = 400, 175
        target_x, target_y = 600, 125
        
        # Участники
        self.attack_canvas.create_rectangle(client_x-25, client_y-20, client_x+25, client_y+20, 
                                          fill='lightblue', outline='blue', tags="mitm")
        self.attack_canvas.create_text(client_x, client_y, text="👤", font=('Arial', 12), tags="mitm")
        
        self.attack_canvas.create_oval(hacker_x-25, hacker_y-20, hacker_x+25, hacker_y+20, 
                                     fill='red', outline='darkred', tags="mitm")
        self.attack_canvas.create_text(hacker_x, hacker_y, text="⚡", font=('Arial', 14), tags="mitm")
        
        self.attack_canvas.create_rectangle(target_x-30, target_y-25, target_x+30, target_y+25, 
                                          fill='lightgreen', outline='green', tags="mitm")
        self.attack_canvas.create_text(target_x, target_y, text="🖥️", font=('Arial', 14), tags="mitm")
        self.attack_canvas.create_text(target_x, target_y+35, text=target_device.upper(), fill='white', tags="mitm")
        
        # Анимация перехвата
        for i in range(2):
            direct_line = self.attack_canvas.create_line(client_x+25, client_y, target_x-30, target_y, 
                                                       arrow=tk.BOTH, fill='green', width=2, tags="mitm")
            self.attack_canvas.update()
            self.frame.after(500)
            self.attack_canvas.delete(direct_line)
            
            hack_line1 = self.attack_canvas.create_line(client_x+25, client_y, hacker_x, hacker_y-20, 
                                                      arrow=tk.LAST, fill='red', width=2, tags="mitm")
            hack_line2 = self.attack_canvas.create_line(hacker_x, hacker_y+20, target_x-30, target_y, 
                                                      arrow=tk.LAST, fill='red', width=2, tags="mitm")
            self.attack_canvas.update()
            self.frame.after(500)
            self.attack_canvas.delete(hack_line1, hack_line2)
    
    def simulate_port_scan(self, target_device):
        self.log_attack_event(f"🎯 Цель сканирования: найти открытые порты {target_device}")
        
        target_x, target_y = 400, 125
        self.attack_canvas.create_rectangle(target_x-50, target_y-30, target_x+50, target_y+30, 
                                          fill='gray', outline='white', tags="portscan")
        self.attack_canvas.create_text(target_x, target_y, text="🎯", font=('Arial', 16), tags="portscan")
        self.attack_canvas.create_text(target_x, target_y+40, text=target_device.upper(), fill='white', tags="portscan")
        
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 3389]
        open_ports = random.sample(ports, 3)
        
        for i, port in enumerate(ports):
            x = 100 + (i % 5) * 150
            y = 180 + (i // 5) * 40
            
            if port in open_ports:
                color = 'red'
                status = "ОТКРЫТ"
                self.attack_canvas.create_line(x, y, target_x, target_y, fill='red', width=2, tags="portscan")
            else:
                color = 'gray'
                status = "закрыт"
                self.attack_canvas.create_line(x, y, target_x, target_y, fill='gray', width=1, 
                                              dash=(2,2), tags="portscan")
            
            self.attack_canvas.create_rectangle(x-25, y-15, x+25, y+15, fill=color, 
                                              outline='white', tags="portscan")
            self.attack_canvas.create_text(x, y, text=f"Порт {port}", 
                                          font=('Arial', 8), fill='white', tags="portscan")
            self.attack_canvas.update()
            self.frame.after(300)
    
    def log_attack_event(self, event):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.attack_log.insert(tk.END, f"[{timestamp}] {event}\n")
        self.attack_log.see(tk.END)