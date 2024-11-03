from colorama import init, Fore, Back

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(Fore.RED + "Пожалуйста, введите корректное число." + Fore.RESET)

def draw_well():
    print(Fore.YELLOW)
    print("""
           ||
           ||
           ||
           || 
          /  \\
         /____\\
        |      |
        |  Пакер  |  (глубина установки пакера)
        |      |
        |      |
        |  Насос  |  (глубина спуска насоса)
        |      |
        |______|
    """)
    print(Fore.RESET)

def main():
    init()
    print(Fore.RED)
    print("ПРИВЕТ! ЭТО АВТОМАТИЧЕСКИЙ РАСЧЕТ ПЛОТНОСТИ И ОБЪЕМА ГЛУШЕНИЯ СКВАЖИНЫ С ЭКСПЛУАТАЦИОННОЙ КОЛОННОЙ 146мм И ТОЛЩИНОЙ СТЕНКИ 5,5мм")
    print(Fore.GREEN)

    # Проверка типа скважины
    what = input('Скважина с эксплуатационной колонной 146мм и толщиной стенки 5,5мм? (да, нет): ').strip().lower()
    if what != "да":
        print(Fore.GREEN)
        print("Данный расчет вам не подходит, т.к. не может гарантировать точный расчет для безопасной замены скважинной жидкости")
        input('Press ENTER to exit')
        return

    print(Fore.RED)

    # Ввод необходимых данных
    a = get_float_input('Введите интервал верхних перфорационных отверстий: ')
    b = get_float_input('Введите интервал нижних перфорационных отверстий: ')
    c = get_float_input('Введите удлинение на ср.интервал перфораций: ')
    d = get_float_input('Введите статический уровень в скважине: ')
    e = get_float_input('Введите избыточное давление или давление в затрубном пространстве в МПа: ')
    f = get_float_input('Введите процент обводненности в продукции: ')
    q = get_float_input('Введите искусственный забой в скважине: ')
    o = get_float_input('Введите глубину спуска насоса или глубину спуска фонтанного лифта в метрах: ')

    # Запрашиваем наличие пакера
    has_packer = input('Есть ли пакер в скважине? (да, нет): ').strip().lower()

    # Отрисовка скважины
    draw_well()

    # Подготовка для расчетов
    density = (((1.02 - 0.86) * f) / 100) + 0.86
    avg_perforation_interval = (b + a) / 2
    static_pressure = (((avg_perforation_interval - c) - d) * density / 100) + e

    # Объемы
    volume1 = ((1.07 * static_pressure) * 1000) / ((avg_perforation_interval - c) * 9.81)
    depth_adjustment = (volume1 * ((b + a) / 2) - c) / 100

    # Запрос глубины установки пакера
    if has_packer == "да":
        paker_H = get_float_input('Введите глубину установки пакера: ')
        additional_volume = (q - o) * 13.6 / 1000 + o * 3 / 1000 + (o - paker_H) * 9.5 / 1000
        volume_XZ = paker_H * 9.5 / 1000 + o * 3 / 1000
        total_volume = volume_XZ + additional_volume
        
        # Вывод результатов после всех вводов
        print(Back.RED)
        print(Fore.WHITE)
        print("<<<!!!Результат!!!>>>")
        print(Back.BLACK)
        print(Fore.WHITE)
        print(f"Плотность жидкости глушения г/см³: {density:.2f}")
        print(f"Пластовое давление в МПа: {static_pressure:.2f}")
        print(f"Давление гидростатического столба жидкости в МПа: {depth_adjustment:.2f}")
        print(f"Общий объем жидкости для глушения с пакером в кубометрах: {total_volume:.2f}")
        print(f"Объем жидкости для глушения первого цикла: {additional_volume:.2f}")
        print(f"Объем жидкости для глушения второго цикла после срыва пакера и тех.отстоя: {volume_XZ:.2f}")
    else:
        # Если пакера нет, выводим только основные результаты
        print(Back.RED)
        print(Fore.WHITE)
        print("<<<!!!Результат!!!>>>")
        print(Back.BLACK)
        print(Fore.WHITE)
        print(f"Плотность жидкости глушения г/см³: {density:.2f}")
        print(f"Пластовое давление в МПа: {static_pressure:.2f}")
        print(f"V1 (объем жидкости для глушения 1 циклом с тех.отстоем 12 часов) в кубометрах: {volume1:.2f}")

    input('Press ENTER to exit')

if __name__ == "__main__":
    main()
