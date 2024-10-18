import tkinter as tk
from tkinter import filedialog, messagebox
import json
import math

# Просчёт q
def calculate_cumulative_probabilities(probabilities):
    q = [0] * len(probabilities)
    q[0] = 0
    for i in range(1, len(probabilities)):
        q[i] = q[i - 1] + probabilities[i - 1]
    return q

# Просчёт словаря [символ, его код]
def shannon_coding(symbols, probabilities):
    code_dict = {}
    cumulative_probs = calculate_cumulative_probabilities(probabilities)

    for i, symbol in enumerate(symbols):
        prob = probabilities[i]
        cum_prob = cumulative_probs[i]

        # Вычисляем длину кодового слова
        code_length = math.ceil(-math.log2(prob))
        code_word = ""

        # Преобразуем кумулятивную вероятность в двоичный вид с точностью до code_length символов
        fractional_part = cum_prob
        for _ in range(code_length):
            fractional_part *= 2
            if fractional_part >= 1:
                code_word += "1"
                fractional_part -= 1
            else:
                code_word += "0"

        code_dict[symbol] = code_word

    return code_dict

# Кодирование
def encode(sequence, code_dict):
    try:
        return ''.join([code_dict[symbol] for symbol in sequence])
    except Exception:
        messagebox.showerror("Error", "Присутствуют символы которых нет в словаре")

# Декодирование
def decode(encoded_sequence, code_dict):
    reverse_dict = {v: k for k, v in code_dict.items()}
    decoded_sequence = []
    current_code = ""
    
    for bit in encoded_sequence:
        current_code += bit
        if current_code in reverse_dict:
            decoded_sequence.append(reverse_dict[current_code])
            current_code = ""
    
    return ''.join(decoded_sequence)

# Среднее
def average_code_length(probabilities, code_lengths):
    return sum(p * l for p, l in zip(probabilities, code_lengths))

# Энтропия
def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

# Избыточность
def redundancy(average_length, entropy_value):
    return average_length - entropy_value

# Условия Крафта
def kraft_inequality(code_lengths):
    return sum(2**(-l) for l in code_lengths)

# Интерфейс tkinter
class ShannonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Кодирование Шеноном")
        self.geometry("800x800")

        # Поля для ввода и вывода
        self.symbols_label = tk.Label(self, text="Символы и их вероятности")
        self.symbols_label.place(x=20, y=30)

        self.symbols_text = tk.Text(self, height=6, width=30)
        self.symbols_text.place(x=20, y=50)

        
        self.props = tk.Label(self, text="Кодировка")
        self.props.place(x=520, y=30)

        self.props_text = tk.Text(self, height=6, width=30)
        self.props_text.place(x=520, y=50)

        y_shift = 200
        y_step_text = 30
        y_step = 80
        self.sequence_label = tk.Label(self, text="Последовательность для кодирования")
        self.sequence_label.place(x=20, y=y_shift)

        self.sequence_entry = tk.Entry(self, width=50)
        self.sequence_entry.place(x=20, y=y_shift + y_step_text)

        # Поля для отображения кодов и результатов
        self.code_label = tk.Label(self, text="Закодированная последовательность")
        self.code_label.place(x=20, y=y_shift + y_step * 1)

        self.code_text = tk.Entry(self, width=50)
        self.code_text.place(x=20, y=y_shift + y_step * 1 + y_step_text)

        self.decode_label = tk.Label(self, text="Раскодированная последовательность")
        self.decode_label.place(x=20, y=y_shift + y_step * 2)

        self.decode_text = tk.Entry(self, width=50)
        self.decode_text.place(x=20, y=y_shift + y_step * 2 + y_step_text)

        # Характеристики
        self.avarage_word = tk.Label(self, text="Средняя длина кодового слова")
        self.avarage_word.place(x=20, y=y_shift + y_step * 3.2)

        self.avarage_word_text = tk.Entry(self, width=50)
        self.avarage_word_text.place(x=20, y=y_shift + y_step * 3.2 + y_step_text)

        self.redundancy = tk.Label(self, text="Избыточность")
        self.redundancy.place(x=20, y=y_shift + y_step * 4)

        self.redundancy_text = tk.Entry(self, width=50)
        self.redundancy_text.place(x=20, y=y_shift + y_step * 4 + y_step_text)

        self.craft = tk.Label(self, text="Неравенство крафта")
        self.craft.place(x=20, y=y_shift + y_step * 5)

        self.kraft_text = tk.Entry(self, width=50)
        self.kraft_text.place(x=20, y=y_shift + y_step * 5 + y_step_text)

        # Кнопки для действий
        y_shift = 230
        y_step = 30
        self.load_button = tk.Button(self, text="Загрузка символов и их вероятностей", command=self.load_json)
        self.load_button.place(x=520, y=y_shift)

        self.encode_button = tk.Button(self, text="Загрузить последовательность", command=self.load_sequence)
        self.encode_button.place(x=520, y=y_shift + y_step * 1)
        
        self.encode_button = tk.Button(self, text="Закодировать", command=self.encode_sequence)
        self.encode_button.place(x=520, y=y_shift + y_step * 2)

        self.save_encoded_button = tk.Button(self, text="Сохранить в файл закодированнуб последовательность", command=self.save_encoded)
        self.save_encoded_button.place(x=520, y=y_shift + y_step * 3)

        self.load_encoded_button = tk.Button(self, text="Загрузить закодированную последовательность", command=self.load_encoded)
        self.load_encoded_button.place(x=520, y=y_shift + y_step * 4)

        self.decode_button = tk.Button(self, text="Раскодировать", command=self.decode_sequence)
        self.decode_button.place(x=520, y=y_shift + y_step * 5)

        self.save_encoded_button = tk.Button(self, text="Сохранить в файл раскодированную последовательность", command=self.save_decoded)
        self.save_encoded_button.place(x=520, y=y_shift + y_step * 6)
        

        self.specifications_button = tk.Button(self, text="Просчитать характеристики", command=self.solve_specification)
        self.specifications_button.place(x=520, y=y_shift + y_step * 8)

        # Хранение данных
        self.symbols = []
        self.probabilities = []
        self.code_dict = {}

    def load_json(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filepath:
            return

        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                self.symbols = data['symbols']
                self.probabilities = data['probabilities']
                self.coder = [[self.symbols[i], self.probabilities[i]] for i in range(len(self.symbols))]
                self.coder = sorted(self.coder, key=lambda x: x[1], reverse=True)
                self.symbols = [i[0] for i in self.coder]
                self.probabilities = [i[1] for i in self.coder]


                self.code_dict = shannon_coding(self.symbols, self.probabilities)
                
                # Отображаем символы и вероятности в текстовом поле
                self.symbols_text.delete(1.0, tk.END)
                self.props_text.delete(1.0, tk.END)
                for symbol, prob in zip(self.symbols, self.probabilities):
                    self.symbols_text.insert(tk.END, f"{symbol}: {prob}\n")
                for i in self.code_dict.keys():
                    self.props_text.insert(tk.END, f"{i}: {self.code_dict[i]}\n")
                messagebox.showinfo("Success", "Символы и вероятности загружены успешно")
        except Exception:
            messagebox.showerror("Error", "Ошибка загрузки файла")

    # Кодировать введеную последовательность
    def encode_sequence(self):
        sequence = self.sequence_entry.get().strip()
        if not sequence or not self.code_dict:
            messagebox.showerror("Error", "ВВедите последовательность")
            return

        encoded_sequence = encode(sequence, self.code_dict)
        self.code_text.delete(0, tk.END)
        self.code_text.insert(0, encoded_sequence)

    # Декодировать введенную последовательность
    def decode_sequence(self):
        encoded_sequence = self.code_text.get().strip()
        if not encoded_sequence or not self.code_dict:
            messagebox.showerror("Error", "Введите закодированную последовательность")
            return

        decoded_sequence = decode(encoded_sequence, self.code_dict)
        self.decode_text.delete(0, tk.END)
        self.decode_text.insert(0, decoded_sequence)

    # Сохранить закодированную последовательность
    def save_encoded(self):
        encoded_sequence = self.code_text.get().strip()
        if not encoded_sequence:
            messagebox.showerror("Error", "Нет последовательности для сохранения")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, 'w') as file:
            file.write(encoded_sequence)
        messagebox.showinfo("Success", "Закодированная последовательность сохранена успешно")
    
    # Сохранить Декодированную последовательность
    def save_decoded(self):
        decode_sequence = self.decode_text.get().strip()
        if not decode_sequence:
            messagebox.showerror("Error", "Нет последовательности для сохранения")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filepath:
            return
        try:
            with open(filepath, 'w') as file:
                file.write(decode_sequence)
            messagebox.showinfo("Success", "Раскодированная последовательность сохранена успешно")
        except Exception:
            messagebox.showerror("Error", "Ошибка сохранения файла")

    # Загрузить закодированную последовательность
    def load_encoded(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, 'r') as file:
            encoded_sequence = file.read().strip()
            self.code_text.delete(0, tk.END)
            self.code_text.insert(0, encoded_sequence)

    # Загрузить Последовательность
    def load_sequence(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, 'r') as file:
            encoded_sequence = file.read().strip()
            self.sequence_entry.delete(0, tk.END)
            self.sequence_entry.insert(0, encoded_sequence)

    # Характеристики (среднее, избыточность, Крафт)
    def solve_specification(self):
        # Средняя длина кодового слова
        self.code_lengths = [len(self.code_dict[i]) for i in self.code_dict.keys()]
        self.avarage_word_text.delete(0, tk.END)
        average = average_code_length(self.probabilities, self.code_lengths)
        self.avarage_word_text.insert(0, average)

        # Избыточность
        entropy_value = entropy(self.probabilities)
        redundancy_value = redundancy(average, entropy_value)
        self.redundancy_text.delete(0, tk.END)
        self.redundancy_text.insert(0, redundancy_value)

        # Неравенство крафта
        if (kraft_inequality(self.code_lengths) <= 1):
            self.kraft_text.delete(0, tk.END)
            self.kraft_text.insert(0, "Выполняется")
        else:
            self.kraft_text.delete(0, tk.END)
            self.kraft_text.insert(0, "Не Выполняется")


if __name__ == "__main__":
    app = ShannonApp()
    app.mainloop()
