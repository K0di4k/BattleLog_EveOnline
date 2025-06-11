import re
import tkinter as tk
from tkinter import filedialog, ttk
from collections import defaultdict

class CombatAnalyzer:
    def __init__(self):
        self.total_damage = 0
        self.damage_by_enemy = defaultdict(int)
        self.damage_by_weapon = defaultdict(int)
        self.drone_damage = 0
        self.hits = 0

    def parse_log(self, log_text):
        # Patrón para extraer daño, enemigo, corporación, nave, arma y forma de impacto
        pattern = r'\[ \d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2} \] \(combat\) <color=0xffcc0000><b>(\d+)</b> <color=0x77ffffff><font size=10>from</font> <b><color=0xffffffff>([^[]+)\[([^\]]+)\]\(([^)]+)\)</b><font size=10><color=0x77ffffff> - ([^ ]+) - ([^<]+)'
        matches = re.findall(pattern, log_text)
        
        for match in matches:
            damage, enemy, corp, ship, weapon, impact = match
            damage = int(damage)
            self.total_damage += damage
            self.damage_by_enemy[enemy] += damage
            self.damage_by_weapon[weapon] += damage
            # Identificar daño por drones
            if "Drone" in weapon or "Hornet" in weapon or "Warrior" in weapon:
                self.drone_damage += damage
            self.hits += 1

    def get_report(self):
        if self.hits == 0:
            return "No se encontraron datos de combate."
        average_damage = self.total_damage / self.hits
        report = f"**Daño Total Recibido:** {self.total_damage}\n"
        report += f"**Daño Promedio por Impacto:** {average_damage:.2f}\n\n"
        report += "**Daño por Enemigo:**\n"
        for enemy, damage in self.damage_by_enemy.items():
            report += f"  - {enemy}: {damage}\n"
        report += "\n**Daño por Tipo de Arma:**\n"
        for weapon, damage in self.damage_by_weapon.items():
            report += f"  - {weapon}: {damage}\n"
        report += f"\n**Daño Total Recibido por Drones:** {self.drone_damage}\n"
        return report

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_text = file.read()
            analyzer.parse_log(log_text)
            report = analyzer.get_report()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, report)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Analizador de Combate")
root.geometry("800x600")
root.configure(bg="#f8f9fa")  # Fondo claro similar a Bootstrap

analyzer = CombatAnalyzer()

# Estilo para parecerse a Bootstrap
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6, background="#007bff", foreground="black")
style.map("TButton", background=[("active", "#0056b3")])

# Frame principal
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Botón para cargar archivo
load_button = ttk.Button(frame, text="Cargar Registro de Combate", command=load_file, style="TButton")
load_button.pack(pady=10)

# Área de texto para el reporte
text_area = tk.Text(frame, wrap=tk.WORD, width=80, height=30, font=("Helvetica", 12), bg="#ffffff", relief="solid", borderwidth=1)
text_area.pack(fill="both", expand=True, pady=10)

# Iniciar la aplicación
root.mainloop()