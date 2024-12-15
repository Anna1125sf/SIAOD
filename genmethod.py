import random
import tkinter as tk
from tkinter import ttk


def has_time_conflict(start, end, schedule):
    return any(s < end and start < e for s, e in schedule)


def is_in_working_hours(start, end, work_start, work_end):
    return work_start <= start < work_end and work_start < end <= work_end

# Генетический алгоритм для распределения маршрутов
def genetic_algorithm(drivers, num_routes, generations, population_size, work_hours):
    route_times = list(range(8, 23))  
    route_duration = 2  

    # Создание случайного расписания
    def create_random_schedule():
        schedules = {driver: [] for driver in drivers}
        routes = []

        
        while len(routes) < num_routes:
            start = random.choice(route_times)
            end = start + route_duration
            if end <= 24:  
                routes.append((start, end))

        # Равномерное распределение маршрутов по водителям
        for i, (start, end) in enumerate(routes):
            driver = drivers[i % len(drivers)]  
            work_start, work_end = work_hours[driver]
            if (not has_time_conflict(start, end, schedules[driver]) and
                    is_in_working_hours(start, end, work_start, work_end)):
                schedules[driver].append((start, end))
        
        return schedules

    # Оценка расписания 
    def evaluate(schedule):
        total_routes = sum(len(routes) for routes in schedule.values())
        return total_routes

    
    def crossover(parent1, parent2, drivers):
        child = {driver: [] for driver in drivers}
        for driver in drivers:
            if random.random() > 0.5:
                child[driver] = parent1[driver]
            else:
                child[driver] = parent2[driver]
        return child

    # Создание начальной популяции
    population = [create_random_schedule() for _ in range(population_size)]

    # Генетическая эволюция
    for _ in range(generations):
        population.sort(key=evaluate, reverse=True)  
        new_population = population[:2]  

       
        for _ in range(population_size - 2):
            parent1, parent2 = random.sample(population[:5], 2)
            child = crossover(parent1, parent2, drivers)
            new_population.append(child)

        population = new_population

    
    return max(population, key=evaluate)

# Функция для генерации и отображения расписания
def generate_schedule(drivers, work_hours):
    try:
        num_routes = int(entry_num_routes.get())
        generations = int(entry_generations.get())
        population_size = int(entry_population.get())

        if num_routes <= 0 or generations <= 0 or population_size <= 0:
            output_text.insert(tk.END, "Ошибка: Введите положительные числа.\n")
            return

        schedule = genetic_algorithm(drivers, num_routes, generations, population_size, work_hours)
        display_schedule(schedule)
    except ValueError:
        output_text.insert(tk.END, "Ошибка: Введите корректные числовые значения.\n")


def display_schedule(schedules):
    output_text.delete("1.0", tk.END)
    for driver, schedule in schedules.items():
        output_text.insert(tk.END, f"Водитель: {driver}\n")
        for start, end in schedule:
            output_text.insert(tk.END, f"  {start:02d}:00 - {end:02d}:00\n")
        output_text.insert(tk.END, "\n")

# Генерация расписания для типа A
def generate_schedule_for_type_a():
    work_hours = {driver: (8, 16) for driver in drivers_a}  # Рабочие часы с 8:00 до 16:00
    generate_schedule(drivers_a, work_hours)# Генерация расписания для типа B
def generate_schedule_for_type_b():
    work_hours = {driver: (0, 24) for driver in drivers_b}  # Рабочие часы с 0:00 до 24:00
    generate_schedule(drivers_b, work_hours)

# Интерфейс
root = tk.Tk()
root.title("Распределение маршрутов с использованием ГА")
root.geometry("800x600")

# Ввод данных
label_num_routes = ttk.Label(root, text="Количество маршрутов:")
label_num_routes.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_num_routes = ttk.Entry(root, width=10)
entry_num_routes.grid(row=0, column=1, padx=5, pady=5)

label_generations = ttk.Label(root, text="Количество поколений:")
label_generations.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_generations = ttk.Entry(root, width=10)
entry_generations.grid(row=1, column=1, padx=5, pady=5)

label_population = ttk.Label(root, text="Размер популяции:")
label_population.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_population = ttk.Entry(root, width=10)
entry_population.grid(row=2, column=1, padx=5, pady=5)

# Кнопки генерации
button_generate_a = ttk.Button(root, text="Генерировать для типа A", command=generate_schedule_for_type_a)
button_generate_a.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

button_generate_b = ttk.Button(root, text="Генерировать для типа B", command=generate_schedule_for_type_b)
button_generate_b.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

# Поле для вывода
output_text = tk.Text(root, wrap="word", font=("Courier", 10))
output_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")


scrollbar = ttk.Scrollbar(root, command=output_text.yview)
output_text.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=4, column=3, sticky="ns")


drivers_a = ["Водитель A1", "Водитель A2", "Водитель A3", "Водитель А4"]
drivers_b = ["Водитель B1", "Водитель B2", "Водитель В3"]

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

root.mainloop()
