import random
import tkinter as tk
from tkinter import ttk



def has_time_conflict(start, end, schedule):
    return any(s < end and start < e for s, e in schedule)


def is_in_working_hours(start, end, work_start, work_end):
    return work_start <= start < work_end and work_start < end <= work_end

# Генерация расписания для водителей
def generate_driver_schedule(drivers, num_routes, route_duration, work_hours):
    # Генерируем маршруты только в рамках доступного времени
    routes = []
    for _ in range(num_routes):
        route_start = random.choice(route_times)
        route_end = route_start + route_duration
        if route_end <= 24: 
            routes.append((route_start, route_end))

    schedules = {driver: [] for driver in drivers}

    for route_start, route_end in routes:
        assigned = False
        for driver in drivers:
            work_start, work_end = work_hours[driver]
            
            if (not has_time_conflict(route_start, route_end, schedules[driver]) and
                    is_in_working_hours(route_start, route_end, work_start, work_end)):
                schedules[driver].append((route_start, route_end))
                assigned = True
                break
        if not assigned:
            output_text.insert(tk.END, f"Маршрут с {route_start:02d}:00 до {route_end:02d}:00 не удалось назначить!\n")
    return schedules

# Вывод расписания
def display_schedule(schedules):
    output_text.delete("1.0", tk.END)
    for driver, schedule in schedules.items():
        output_text.insert(tk.END, f"Водитель: {driver}\n")
        for start, end in schedule:
            output_text.insert(tk.END, f"  {start:02d}:00 - {end:02d}:00\n")
        output_text.insert(tk.END, "\n")

# Генерация расписания для типа A
def generate_schedule_for_type_a():
    try:
        num_routes = int(entry_num_routes.get())
        if num_routes <= 0:
            output_text.insert(tk.END, "Ошибка: Количество маршрутов должно быть больше 0.\n")
            return
        
        work_hours = {driver: (8, 16) for driver in drivers_a}
        schedule = generate_driver_schedule(drivers_a, num_routes, route_duration, work_hours)
        display_schedule(schedule)
    
    except ValueError:
        output_text.insert(tk.END, "Ошибка: Введите корректное количество маршрутов.\n")

# Генерация расписания для типа B
def generate_schedule_for_type_b():
    try:
        num_routes = int(entry_num_routes.get())
        if num_routes <= 0:
            output_text.insert(tk.END, "Ошибка: Количество маршрутов должно быть больше 0.\n")
            return

        work_hours = {driver: (0, 24) for driver in drivers_b}
        schedule = generate_driver_schedule(drivers_b, num_routes, route_duration, work_hours)
        display_schedule(schedule)
    except ValueError:
        output_text.insert(tk.END, "Ошибка: Введите корректное количество маршрутов.\n")




route_times = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
route_duration = 1  # Продолжительность маршрута в часах
drivers_a = ["Водитель A1", "Водитель A2", "Водитель A3", "Водитель А4"]
drivers_b = ["Водитель B1", "Водитель B2", "Водитель В3"]

# Интерфейс
root = tk.Tk()
root.title("Распределение маршрутов")
root.geometry("740x580")


main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Поле ввода количества маршрутов
label_num_routes = ttk.Label(main_frame, text="Количество маршрутов:")
label_num_routes.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry_num_routes = ttk.Entry(main_frame, width=10)
entry_num_routes.grid(row=0, column=1, padx=5, pady=5)

# Кнопки генерации расписания
button_generate_a = ttk.Button(main_frame, text="Генерировать для типа A", command=generate_schedule_for_type_a)
button_generate_a.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

button_generate_b = ttk.Button(main_frame, text="Генерировать для типа B", command=generate_schedule_for_type_b)
button_generate_b.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
# Поле для вывода расписания
output_text = tk.Text(main_frame, height=20, wrap="word", font=("Courier", 10))
output_text.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Добавление прокрутки
scrollbar = ttk.Scrollbar(main_frame, command=output_text.yview)
output_text.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=2, column=2, sticky="ns")


main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)


root.mainloop()
