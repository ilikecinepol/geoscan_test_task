'''Задание 1 Написать функцию, осуществляющую управление движением мобильного объекта, движущегося в двумерной плоскости.
Функция принимает на вход текущее состояние такого объекта и координаты цели движения, на выход предоставляет линейную и угловую скорости,
позволяющие приблизится к требуемой цели.
Функция вызывается с некоторым (малым) периодом и предоставляет значения скоростей,
необходимых применить к управляемому объекту в вызванный момент времени'''

# Для примера возьмём модуль turtle
import turtle
import math
import time


# Функция установки целевой точки
def set_goal(goal_x, goal_y):
    goal_obj = turtle
    goal_obj.speed(0)
    goal_obj.penup()
    goal_obj.color('red')
    goal_obj.shape('circle')
    goal_obj.goto(goal_x, goal_y)
    return goal_x, goal_y


# Функция ограничения значений
def limitation(value, max_val=100, min_val=-100):
    return max_val if value > max_val else min_val if value < min_val else value


# Функция получения данных о положении объекта управления
def get_coords(obj):
    l_speed = 0
    current_x = obj.xcor()
    current_y = obj.ycor()
    current_yaw = obj.heading()
    return current_x, current_y, current_yaw, l_speed


# Функция движения черепашки
def moving(obj, speed):
    global target_obj
    linear_speed = limitation(speed[0], 10, 0)
    angular_speed = limitation(speed[1], 350, -350)
    obj.speed(linear_speed)
    obj.forward(linear_speed)
    obj.left(angular_speed)


# Функция управления
def control(current_obj, target_obj):
    goal_x = target_obj[0]
    goal_y = target_obj[1]
    x = current_obj[0]
    y = current_obj[1]
    current_yaw = current_obj[2]
    k_angular = 1.0  # Пропорциональный коэффициент
    k_linear = 0.5
    desired_angle_goal = math.degrees(math.atan2(goal_y - y, goal_x - x))
    # Угловая скорость пропорциональна арктангенсу между векторами, проведёнными из текущего положения,
    # один из них сонаправлен с yaw, другой направлен на целевую точку
    angular_speed = (desired_angle_goal - current_yaw) * k_angular
    # Линейная скорость пропорциональна длине вектора, вершины которого находятся в текущей и целевой позиях
    linear_speed = abs(math.sqrt(((x - goal_x) ** 2) + ((y - goal_y) ** 2))) * k_linear
    # print(limitation(linear_speed, 10, 0), limitation(round(angular_speed, 2), 360, -359))
    print(current_yaw, desired_angle_goal)
    return limitation(round(linear_speed, 2), 10, 0), round(angular_speed, 2)


if __name__ == '__main__':
    # Установка целевых координат, максимум (450, 400)
    target_obj = set_goal(350, 400)
    obj = turtle.Turtle('circle', visible=True)
    obj.shape('classic')
    while True:
        moving(obj, control(get_coords(obj), target_obj))
        time.sleep(0.01)
