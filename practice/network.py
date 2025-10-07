import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from datetime import datetime

class NetworkModule:
    def __init__(self):
        self.frame = None
        self.firewall_module = None
        
        # Устройства сети с их фаерволами
        self.devices = {
            'router': {'x': 100, 'y': 200, 'ip': '192.168.1.1', 'status': 'secure', 'type': 'router', 'firewall_rules': []},
            'server': {'x': 300, 'y': 200, 'ip': '192.168.1.10', 'status': 'secure', 'type': 'server', 'firewall_rules': []},
            'pc1': {'x': 500, 'y': 100, 'ip': '192.168.1.101', 'status': 'secure', 'type': 'pc', 'firewall_rules': []},
            'pc2': {'x': 500, 'y': 300, 'ip': '192.168.1.102', 'status': 'secure', 'type': 'pc', 'firewall_rules': []},
            'attacker': {'x': 800, 'y': 200, 'ip': '10.0.0.50', 'status': 'malicious', 'type': 'hacker', 'firewall_rules': []},
        }
        
        self.network_canvas = None
        self.network_log = None
    
    def set_firewall_module(self, firewall_module):
        self.firewall_module = firewall_module
    
    def get_frame(self, parent):
        if not self.frame:
            self.frame = ttk.Frame(parent)
            self.setup_network_gui()
        return self.frame
    
    def setup_network_gui(self):
        # Визуализация сети
        self.network_canvas = tk.Canvas(self.frame, width=1000, height=400, bg='white')
        self.network_canvas.pack(pady=10)
        
        self.draw_network()
        
        # Панель управления
        control_frame = tk.Frame(self.frame)
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
        log_frame = tk.Frame(self.frame)
        log_frame.pack(pady=10)
        tk.Label(log_frame, text="Лог событий сети:", font=('Arial', 10)).pack()
        self.network_log = tk.Text(log_frame, height=8, width=100)
        scrollbar = tk.Scrollbar(log_frame, command=self.network_log.yview)
        self.network_log.configure(yscrollcommand=scrollbar.set)
        self.network_log.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
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
        
        for device, info in self.devices.items():
            x, y = info['x'], info['y']
            color = colors[info['status']]
            outline = outlines[info['status']]
            
            if info['type'] == 'router':
                self.network_canvas.create_rectangle(x-25, y-20, x+25, y+20, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="🔄", font=('Arial', 14))
                self.network_canvas.create_line(x-15, y-20, x-15, y-40, width=2, fill=outline)
                self.network_canvas.create_line(x+15, y-20, x+15, y-40, width=2, fill=outline)
                
            elif info['type'] == 'server':
                self.network_canvas.create_rectangle(x-30, y-25, x+30, y+25, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="🖥️", font=('Arial', 16))
                for i in range(3):
                    self.network_canvas.create_oval(x+15, y-15+i*10, x+20, y-10+i*10, fill='green')
                
            elif info['type'] == 'pc':
                self.network_canvas.create_rectangle(x-20, y-15, x+20, y+15, fill=color, outline=outline, width=2)
                self.network_canvas.create_text(x, y, text="💻", font=('Arial', 12))
                
            elif info['type'] == 'hacker':
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
        
        devices = ['router', 'server', 'pc1', 'pc2']
        for i, device in enumerate(devices):
            progress = (i + 1) * 25
            self.log_network_event(f"📡 Сканирование {device} ({progress}%)...")
            self.frame.update()
            self.frame.after(800)
            
            if random.random() < 0.3:
                self.devices[device]['status'] = 'infected'
                self.log_network_event(f"⚠️ ОБНАРУЖЕНА УГРОЗА на устройстве {device}!")
                self.highlight_device(device, 'red')
            else:
                self.log_network_event(f"✅ {device} безопасен")
                self.highlight_device(device, 'green')
            
            self.draw_network()
            self.frame.update()
        
        self.log_network_event("✅ Сканирование завершено")
    
    def detect_threats(self):
        threats = [dev for dev, info in self.devices.items() 
                  if info['status'] in ['infected', 'malicious']]
        
        if threats:
            self.log_network_event(f"🚨 СИСТЕМА ОБНАРУЖЕНИЯ: найдены угрозы: {', '.join(threats)}")
            for threat in threats:
                self.log_network_event(f"🔴 Угроза: {threat} ({self.devices[threat]['ip']})")
                self.highlight_device(threat, 'red')
        else:
            self.log_network_event("✅ Угроз не обнаружено")
    
    def isolate_threat(self):
        isolated_count = 0
        for device, info in self.devices.items():
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
            self.devices[device]['status'] = 'secure'
        self.devices['attacker']['status'] = 'malicious'
        self.log_network_event("🔄 Сеть сброшена в исходное состояние")
        self.draw_network()
    
    def highlight_device(self, device, color='yellow'):
        info = self.devices[device]
        x, y = info['x'], info['y']
        
        for i in range(3):
            highlight_id = self.network_canvas.create_oval(x-35, y-35, x+35, y+35, 
                                                         outline=color, width=3, tags="highlight")
            self.network_canvas.update()
            self.frame.after(300)
            self.network_canvas.delete(highlight_id)
    
    def log_network_event(self, event):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.network_log.insert(tk.END, f"[{timestamp}] {event}\n")
        self.network_log.see(tk.END)
    
    def set_device_firewall_rules(self, device_name, rules):
        """Устанавливает правила фаервола для устройства"""
        self.devices[device_name]['firewall_rules'] = rules
        self.log_network_event(f"🛡️ Обновлены правила фаервола для {device_name}")
    
    def check_device_firewall(self, device_name, packet):
        """Проверяет пакет через фаерволл устройства"""
        rules = self.devices[device_name]['firewall_rules']
        return self._evaluate_rules(rules, packet)
    
    def _evaluate_rules(self, rules, packet):
        """Оценивает правила фаервола"""
        # Если нет правил - разрешаем по умолчанию (для демонстрации)
        if not rules:
            return True
            
        for rule in rules:
            if self._rule_matches(rule, packet):
                return rule['action'] == 'allow'
        return False  # Если правила есть, но ни одно не совпало - блокировать
    
    def _rule_matches(self, rule, packet):
        """Проверяет совпадает ли правило с пакетом"""
        # Проверка протокола
        if rule['protocol'] != 'any' and rule['protocol'] != packet.get('protocol', 'tcp'):
            return False
            
        # Проверка порта
        if rule['port'] != 'any' and rule['port'] != str(packet.get('port', 80)):
            return False
            
        # Проверка IP источника (упрощенная)
        if rule['source'] != 'any' and rule['source'] != packet.get('source_ip', 'any'):
            return False
            
        # Проверка IP назначения (упрощенная)  
        if rule['destination'] != 'any' and rule['destination'] != packet.get('target_ip', 'any'):
            return False
            
        return True
    
    def get_devices(self):
        """Возвращает список устройств"""
        return list(self.devices.keys())