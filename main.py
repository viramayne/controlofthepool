__author__ = 'Vira.Mayne'
from tkinter import *
from ModelTimer import ModelTimer
# from math import round


def show_check():
    global u1, u2
    u1 = var1.get()
    u2 = var2.get()
    Label(pool, text="Temp = %f" % round(temp, 3), background="white").place(x=100, y=290)  # Вывод текущих значений на экран
    Label(pool, text="Level = %f" % round(level, 3), background="white").place(x=100, y=310)


def refresh_data(event):
    global ll, lh, tl, th, ct, s, tin, tout, q, k, level, temp, p, time
    global is_running, loop_now, iteration_on, iteration_off, time, counter1, counter2
    if is_running:
        model_timer.cancel()
        model_timer2.cancel()
    for i in range(0, iteration_on + 1):
        Label(pool, text='      ', background="white").place(x=10 + i * 20, y=620)
    canvas1.delete("deleted")
    canvas2.delete("deleted")
    Label(pool, text="Temp =                        ", background="white").place(x=100, y=290)
    Label(pool, text="Level =                       ", background="white").place(x=100, y=310)
    loop_now = canvas2.create_oval(0, 0, 0, 0, tag="deleted")
    time = 0
    ll = float(LL_ent.get())
    lh = float(LH_ent.get())
    tl = float(TL_ent.get())
    th = float(TH_ent.get())
    ct = float(Ct_ent.get())
    s = float(S_ent.get())
    tin = float(Tin_ent.get())
    tout = float(Tout_ent.get())
    q = float(Q_ent.get())
    k = float(K_ent.get())
    level = float(Level_ent.get())
    temp = float(Temp_ent.get())
    p = float(P_ent.get())
    iteration_on = 0
    iteration_off = 0
    time = 0
    counter1 = 0
    counter2 = 0
    canvas2.coords(im_ll, 30, 420 - ll * 39, 420, 420 - ll * 39)
    canvas2.coords(im_lh, 30, 420 - lh * 39, 420, 420 - lh * 39)
    canvas2.coords(im_tl, 30 + tl * 7.8, 30, 30 + tl * 7.8, 420)
    canvas2.coords(im_th, 30 + th * 7.8, 30, 30 + th * 7.8, 420)


def auto_play(event):
    global is_automatic
    if is_automatic:
        button3.config(text="Ручное управление")
        is_automatic = False
    else:
        button3.config(text="Автоматическое управление")
        is_automatic = True
    pass


def play(event):
    global is_running, model_timer
    if is_running:
        model_timer.cancel()
        model_timer2.cancel()
        is_running = False
        button2.config(text="Запуск симуляции")
    else:
        model_timer.start()
        model_timer2.start()
        is_running = True
        button2.config(text="Остановка симуляции")
    pass


def model_timer_callback():
    global is_running, temp, level, u1, u2, iteration_on, iteration_off, dt, counter1, counter2, time
    if is_running:
        # Основные вычисления программы
        model_timer.start()

        calculations()

        canvas1.create_rectangle(90, 10, 230, 130, outline="gray", fill="white", width=2)
        canvas1.create_rectangle(90, 120 - level * 12, 230, 130, fill="blue", width=2, tag="deleted")
        Label(pool, text="Temp = %.2f°C" % round(temp, 3), background="white").place(x=100, y=290)  # Вывод текущих значений на экран
        Label(pool, text="Level = %.2f м" % round(level, 3), background="white").place(x=100, y=310)
        x = 30 + temp * 7.8
        y = 420 - level * 39
        canvas2.coords(loop_now, x - 2, y - 2, x + 2, y + 2)
        canvas2.itemconfig(loop_now, outline="red", fill="red", width=4)
        canvas2.create_oval(x - 1, y - 1, x + 1, y + 1, fill='black', tag="deleted")
        time += dt
        var1.set(u1)
        var2.set(u2)

        # Вывод значений управлений насосами 1 и 2 в label
        Label(pool, text='Управление 1 = %d' % u1, background="white").place(x=30, y=200)
        Label(pool, text='Управление 2 = %d' % u2, background="white").place(x=240, y=200)
        last_u1 = mas_control[len(mas_control) - 1][0]
        last_u2 = mas_control[len(mas_control) - 1][1]
        if last_u1 != u1 or last_u2 != u2:
            mas_control.append([u1, u2])

            canvas1.create_oval(28 + iteration_on * 20, 600 - u1 * 100, 32 + iteration_on * 20, 606 - u1 * 100,
                                fill="red", tag="deleted")
            Label(pool, text=round(iteration_off * dt), background="white").place(x=10 + (iteration_on + 1) * 20, y=620)
            canvas1.create_oval(28 + iteration_on * 20, 594 - u2 * 100, 32 + iteration_on * 20, 600 - u2 * 100,
                                fill="blue", tag="deleted")
            iteration_on += 1
        else:
            iteration_off += 1
            if last_u1 == u1 and u1 == 1:
                counter1 += 1
            if last_u2 == u2 and u2 == 1:
                counter2 += 1
        Label(pool, text="Время работы насоса 1  = %.2f с" % round(counter1 * dt), background="white").place(x=100, y=350)
        Label(pool, text="Время работы насоса 2 = %.2f с" % round(counter2 * dt), background="white").place(x=100, y=370)
        Label(pool, text="Время симуляции = %.2f с" % round(time, 1), background="white").place(x=100, y=390)
    pass


def model_timer_callback2():
    global is_running, temp, level, is_automatic
    if is_running:
        # Основные вычисления программы
        model_timer2.start()
        if is_automatic:
            zone = get_zone()
            set_u(zone)
        pass
    pass


def calculations():
    global ct, s, k, p, u1, u2, tin, tout, dt, q, level, temp

    V = level * s
    v_next = V + q * dt * (u1 - u2)

    q_o = ct * p * V * temp
    q_isp = k * s * (temp - tout)
    q_nas = ct * p * q * dt * (u1 * (tin - temp) - u2)

    q_next = q_o - q_isp + q_nas
    t_next = q_next / (ct * p * V)

    temp = t_next
    level = v_next / s


def get_zone():
    global temp, level, tl, th, ll, lh
    if temp < tl:
        if level < ll:
            return 1
        elif level < lh:
            return 2
        else:
            return 3
    elif temp < th:
        if level < ll:
            return 8
        elif level < lh:
            return 9
        else:
            return 4
    else:
        if level < ll:
            return 7
        elif level < lh:
            return 6
        else:
            return 5


def set_u(zone):
    global u1, u2, temp, tl, th, ll, lh, level, eps_l, eps_t
    if zone == 1 or zone == 7 or zone == 8:
        u1 = 1
        u2 = 0
    elif zone == 3 or zone == 4 or zone == 5:
        u1 = 0
        u2 = 1
    elif zone == 6:
        u1 = 0
        u2 = 0
    elif zone == 2:
        u1 = 1
        u2 = 1
    else:
        # 9 ая зона
        if level > (lh - eps_l):
            u1 = 0
            u2 = 1
        elif level < (ll + eps_l):
            u1 = 1
            u2 = 0
        elif u1 != u2:
            u1 = 0
            u2 = 0
        if (u1 & u2) and (temp > (th - eps_t)):
            u1 = 0
            u2 = 0
        if not (u1 & u2) and temp < (tl + eps_t):
            u1 = 1
            u2 = 1
        pass


is_running = False
is_automatic = True
root = Tk()
root.geometry("1350x690+0+0")
root.config(background="white")
root.title("Pool")

# Начальные данные

ll = 4.0
lh = 8.0
tl = 20.0
th = 30.0
ct = 4180.0
s = 100.0
tin = 50.0
tout = 3.0
q = 15.0
k = 100000.0
level = 2.0
temp = 5.0
p = 998.2
dt = 0.5
dtr = 2
eps_t = 0.5
eps_l = 0.2
V = s * level
iteration_on = 0
iteration_off = 0
counter1 = 0
counter2 = 0
time = 0
# начальное значение управления
set_u(get_zone())
var1 = IntVar()
var1.set(u1)
var2 = IntVar()
var2.set(u2)

mas_control = [[u1, u2]]
# Список всех параметров и их данные
parameters = LabelFrame(root, text="Параметры", height=700, width=500, background="white")
parameters.pack(fill="both", side=RIGHT, expand="yes")
Label(parameters, text="LL, Нижний предел уровеня жидкости", background="white").grid(row=1, column=1, sticky=W)
LL_ent = Entry(parameters, bd=5)
LL_ent.grid(row=1, column=3)
LL_ent.insert(2, ll)

Label(parameters, text="LH, Верхний предел уровеня жидкости", background="white").grid(row=2, column=1, sticky=W)
LH_ent = Entry(parameters, bd=5)
LH_ent.grid(row=2, column=3)
LH_ent.insert(0, lh)

Label(parameters, text="TL, Нижний предел температуры", background="white").grid(row=3, column=1, sticky=W)
TL_ent = Entry(parameters, bd=5)
TL_ent.grid(row=3, column=3)
TL_ent.insert(0, tl)

Label(parameters, text="TH, Верхний предел температуры", background="white").grid(row=4, column=1, sticky=W)
TH_ent = Entry(parameters, bd=5)
TH_ent.grid(row=4, column=3)
TH_ent.insert(0, th)

Label(parameters, text="Ct, Теплоемкость жидкости", background="white").grid(row=5, column=1, sticky=W)
Ct_ent = Entry(parameters, bd=5)
Ct_ent.grid(row=5, column=3)
Ct_ent.insert(0, ct)

Label(parameters, text="S, Площадь бассейна", background="white").grid(row=6, column=1, sticky=W)
S_ent = Entry(parameters, bd=5)
S_ent.grid(row=6, column=3)
S_ent.insert(0, s)

Label(parameters, text="Tin, Температура жидкости на входе", background="white").grid(row=7, column=1, sticky=W)
Tin_ent = Entry(parameters, bd=5)
Tin_ent.grid(row=7, column=3)
Tin_ent.insert(0, tin)

Label(parameters, text="Tout, Температура внешней среды", background="white").grid(row=8, column=1, sticky=W)
Tout_ent = Entry(parameters, bd=5)
Tout_ent.grid(row=8, column=3)
Tout_ent.insert(0, tout)

Label(parameters, text="Q, Производительность насосов", background="white").grid(row=9, column=1, sticky=W)
Q_ent = Entry(parameters, bd=5)
Q_ent.grid(row=9, column=3)
Q_ent.insert(0, q)

Label(parameters, text="K, Коэфициент остывания", background="white").grid(row=10, column=1, sticky=W)
K_ent = Entry(parameters, bd=5)
K_ent.grid(row=10, column=3)
K_ent.insert(0, k)

Label(parameters, text="Temp, Текущая температура жидкости", background="white").grid(row=11, column=1, sticky=W)
Temp_ent = Entry(parameters, bd=5)
Temp_ent.grid(row=11, column=3)
Temp_ent.insert(0, temp)

Label(parameters, text="Level, Уровень жидкости", background="white").grid(row=12, column=1, sticky=W)
Level_ent = Entry(parameters, bd=5)
Level_ent.grid(row=12, column=3)
Level_ent.insert(0, level)

Label(parameters, text="p, Плотность жидкости", background="white").grid(row=13, column=1, sticky=W)
P_ent = Entry(parameters, bd=5)
P_ent.grid(row=13, column=3)
P_ent.insert(0, p)

button1 = Button(parameters, text="Обновить данные", background="white")
button1.bind('<Button-1>', refresh_data)
button1.place(x=100, y=500)

button2 = Button(parameters, text="Запуск симуляции", background="white")  # старт процесса управления
button2.bind('<Button-1>', play)
button2.place(x=100, y=400)

button3 = Button(parameters, text="Автоматическое управление", background="white")
button3.place(x=100, y=450)
button3.bind('<Button-1>', auto_play)


# Графическое изображение бассейна
pool = LabelFrame(root, text="Бассейн", height=700, width=450, background="white")
pool.pack(fill="both", side=RIGHT, expand="yes")
canvas1 = Canvas(pool, background="white")
canvas1.create_oval(40, 100, 70, 130, outline="red", fill="red", width=2)
c1 = Checkbutton(pool, text="Работа", variable=var1, command=show_check, background="white")
c2 = Checkbutton(pool, text="Работа", variable=var2, command=show_check, background="white")
c1.place(x=30, y=170)
c2.place(x=240, y=170)

Label(pool, text="Насос 1", background="white").place(x=30, y=150)
canvas1.create_rectangle(90, 10, 230, 130, outline="gray", fill="white", width=2)
canvas1.create_oval(250, 100, 280, 130, outline="red", fill="red", width=2)
Label(pool, text="Насос 2", background="white").place(x=240, y=150)
canvas1.pack(fill="both", side=RIGHT, expand="yes")

# График изменения управлений
Label(pool, text="Управление насосами", background="white").place(x=140, y=460)
canvas1.create_line(30, 600, 30, 480, arrow=LAST)
canvas1.create_line(30, 600, 420, 600, arrow=LAST)
Label(pool, text="0", background="white").place(x=10, y=605)
Label(pool, text="1", background="white").place(x=15, y=500)
Label(pool, text="u1,", fg="red", background="white").place(x=5, y=465)
Label(pool, text="u2", fg="blue", background="white").place(x=5, y=485)
Label(pool, text="t", background="white").place(x=420, y=605)

# Зоны Управления
zones = LabelFrame(root, text="Зоны управления", height=700, width=450, background="white")
zones.pack(fill="both", side=RIGHT, expand="yes")

canvas2 = Canvas(zones, background="white")

# Оси координат и их подписи
canvas2.create_line(30, 420, 30, 30, arrow=LAST)
canvas2.create_line(30, 420, 420, 420, arrow=LAST)
Label(zones, text="0,0", background="white").place(x=10, y=420)
Label(zones, text="level", background="white").place(x=5, y=5)
Label(zones, text="temp", background="white").place(x=420, y=440)
# Подписи шкалы осей координат
for i in range(1, 11):
    Label(zones, text="%d" % i, background="white").place(x=5, y=415 - i * 39 - 5)
j = 0
while j < 51:
    if j != 0:
        Label(zones, text="%d" % j, background="white").place(x=22 + j * 7.8, y=425)
        j += 5
    else:
        j += 5

# Значения LL, LH, TL, TH
im_ll = canvas2.create_line(30, 420 - ll * 39, 420, 420 - ll * 39, fill="red", dash=(4, 2))
im_lh = canvas2.create_line(30, 420 - lh * 39, 420, 420 - lh * 39, fill="red", dash=(4, 2))
im_tl = canvas2.create_line(30 + tl * 7.8, 30, 30 + tl * 7.8, 420, fill="red", dash=(4, 2))
im_th = canvas2.create_line(30 + th * 7.8, 30, 30 + th * 7.8, 420, fill="red", dash=(4, 2))
loop_now = canvas2.create_oval(0, 0, 0, 0, tag="deleted")  # указатель в текущий момент времени
canvas2.pack(fill="both", expand="yes")

# Таймеры для работы процесса управления
model_timer = ModelTimer(dt, model_timer_callback)  # для самого процесса
model_timer2 = ModelTimer(dtr, model_timer_callback2)  # для получения управления

root.mainloop()