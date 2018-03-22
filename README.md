# controlofthepool
Код написан на языке программирования **python** с использванием модуля **tkinter** для GUI.
Данный проект представляет собой модель интеллектуальной системы автоматического управления температурой и уровнем воды в бассейне.

### Описание задачи
Имеется бассейн с площадью поверхности **S**. Необходимо поддерживать температуру и уровнь воды в бассейне в рамках заданных значений. Регулировка этих параметров происходит с помощью включения и выключения нососов ( один для накачки, другой - для откачки воды из бассейна). Производительность насосов одинаковая (**Q1 = Q2, Q = const**).

В работе были учитаны следующие допущения:
- Через стенки бассейна теплообмен не происходит;
- Остывание происходит без изменения объема жидкости.

Рассмотрим график, в котором по оси абсцисс тображается температура бассейна, а по ои ординат - уровеннь воды. Разобьем его на зоны, с учетом заданных значений LL, LH, TL и TH. Пронумеровав зоны, получим такую картину: 
![zones of pool](https://github.com/viramayne/controlofthepool/blob/master/zonesofpool.png)
где
* LL - нижний уровень воды;
* LH - верхний уровень воды;
* TL - нижний уроень температура;
* TH - верхний уровень температуры;
* Lmax - максимальный уровень воды в бассейне;
* Tmax - максимальны уровень температуры воды в басейне.

Зону 9 будем считать оптимальной. Управление - переход из текущей неоптимальной зоны (1-8) в оптимальную (9) и удержание параметров в ее рамках.
