#!usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import threading
import PySimpleGUI as sg

AUTHOR = "Truzme_"
VERSION = 1.0

tick = 1

fuel = 500
reactive = 0
reactor_temperature = 0
xenon = 0
turbine_temperature = 0
reactor_pressure = 0
maximum_retarders_rods = 11
power = 0
radiation_level = 0
money = 0

retarders_rods = 0
previous_retarders_rods = 0
pump = 0

maximum_reactor_pressure = 150

pressure_relief = False # Система сброса давления
emergency_cooling = False # САОР
emergency_cooling_volume = 100
fire_extinguishing_system = False

pump_check = True
pressure_relief_check = True
emergency_cooling_check = True
fire_extinguishing_system_check = True

fire = False
explosion = False
meltdown = False

layout = [
	[sg.Text("СУЗ")],
	[sg.Spin([sz for sz in range(0, 11)], font=("Helvetica 18"), change_submits=True, key="retarders_rods")],
	[sg.Text("ГЦН")],
	[sg.Spin([sz for sz in range(0, 11)], font=("Helvetica 18"), change_submits=True, key="pump")],
	[sg.Button("Изменить")],
	[sg.Button("АЗ-5")],
	[sg.Button("САОР")],
	[sg.Button("Система сброса давления")],
	[sg.Button("Система пожаротушения")],
	[sg.Button("Починить ГЦН (500000 ₽)")],
	[sg.Button("Починить САОР (150000 ₽)")],
	[sg.Button("Починить клапан (150000 ₽)")],
	[sg.Button("Починить систему пожаротушения (150000 ₽)")],
	[sg.Button("Восстановить жидкий азот (500000 ₽)")]
]

def banner():
	global VERSION

	print("====================================================")
	print("Симулятор Атомной Электростанции")
	print("")
	print("Автор: " + AUTHOR)
	print("Версия: " + str(VERSION))
	print("====================================================")

def des_10_2(value):
	if value == 0:
		value = -1
	elif value == 1:
		value = 11
	elif value == 2:
		value = 10
	elif value == 3:
		value = 9
	elif value == 4:
		value = 8
	elif value == 5:
		value = 7
	elif value == 6:
		value = 6
	elif value == 7:
		value = 5
	elif value == 8:
		value = 4
	elif value == 9:
		value = 3
	elif value == 10:
		value = 2

	return value

def des_2_10(value):
	if value == -1:
		value = 0
	elif value == 11:
		value = 1
	elif value == 10:
		value = 2
	elif value == 9:
		value = 3
	elif value == 8:
		value = 4
	elif value == 7:
		value = 5
	elif value == 6:
		value = 6
	elif value == 5:
		value = 7
	elif value == 4:
		value = 8
	elif value == 3:
		value = 9
	elif value == 2:
		value = 10

	return value

def emergency_protection(): # АЗ-5
	global meltdown, retarders_rods, previous_retarders_rods

	if meltdown == False:
		retarders_rods = 0
		previous_retarders_rods = 0

def parameters(retarders_rods, pump, fire, reactive, reactor_temperature, turbine_temperature, pump_check, emergency_cooling_check, pressure_relief_check, fire_extinguishing_system_check, reactor_pressure, emergency_cooling, emergency_cooling_volume, pressure_relief, fire_extinguishing_system, power, radiation_level, money):
	print("Показатели:")
	print("")
	print("Температура реактора: " + str(reactor_temperature) + " °C (1500 °C)")
	print("Температура турбины: " + str(turbine_temperature) + " °C")
	print("Давление в реакторе: " + str(reactor_pressure) + " Па (150 Па)")
	print("Реактивность: " + str(reactive))
	print("СУЗ подняты на: " + str(retarders_rods))
	print("Мощность ГЦН: " + str(des_2_10(pump) / 10 * 100) + "%")
	print("САОР: " + str(emergency_cooling))
	print("Жидкий азот: " + str(emergency_cooling_volume))
	print("Система сброса давления: " + str(pressure_relief))
	print("Система пожаротушения: " + str(fire_extinguishing_system))
	print("Мощность реактора: " + str(power) + " МВт")
	print("Уровень заражения: " + str(radiation_level))
	print("")
	print("")
	print("Состояние:")
	print("")
	print("ГЦН: " + str(pump_check))
	print("САОР: " + str(emergency_cooling_check))
	print("Клапан сброса давления: " + str(pressure_relief_check))
	print("Система пожаротушения: " + str(fire_extinguishing_system_check))
	print("")
	print("")
	print("Деньги: " + str(money) + "₽")

	if fire == True:
		print("")
		print("==========")
		print("Пожар!")
		print("==========")

def calc():
	global tick, explosion, meltdown, fire, pump_check, emergency_cooling_check, retarders_rods, previous_retarders_rods, pressure_relief, emergency_cooling, emergency_cooling_volume, fire_extinguishing_system, fire_extinguishing_system_check, pump, reactive, reactor_temperature, xenon, turbine_temperature, reactor_pressure, radiation_level, power, money

	p = 0

	x = 0

	i = 0

	while explosion == False:
		i += 1

		if i > 10:
			i = 0

		if money > 0:
			chance = random.randint(0, 200)

			if chance == 200:
				pump_check = False

			chance = random.randint(0, 200)

			if chance == 200:
				emergency_cooling_check = False

			chance = random.randint(0, 200)

			if chance == 200:
				pressure_relief = False

			chance = random.randint(0, 200)

			if chance == 200:
				fire_extinguishing_system_check = False

			chance = random.randint(0, 150)

			if chance == 150:
				fire = True

		if reactor_temperature < 0:
			reactor_temperature = 0
			continue

		if retarders_rods == 0:
			ex = 1
		if retarders_rods == 1:
			ex = 100
		elif retarders_rods == 2:
			ex = 50
		elif retarders_rods == 3:
			ex = 10
		elif retarders_rods == 4:
			ex = 15
		elif retarders_rods == 5:
			ex = 6
		elif retarders_rods == 6:
			ex = 5
		elif retarders_rods == 7:
			ex = 4
		elif retarders_rods == 8:
			ex = 3
		elif retarders_rods == 9:
			ex = 2
		elif retarders_rods == 10:
			ex = 1

		if retarders_rods == 0:
			p = 0
		elif retarders_rods > previous_retarders_rods:
			p = 1
		elif retarders_rods < previous_retarders_rods:
			p = 2

		if p == 0:
			if reactor_temperature > 0:
				reactive = fuel / ex
				reactor_temperature -= reactive + maximum_retarders_rods
		elif p == 1:
			if retarders_rods > 7:
				reactive = fuel / ex + reactor_temperature / fuel
				reactor_temperature += reactive
			else:
				reactive = fuel / ex
				reactor_temperature += reactive
		elif p == 2:
			if reactor_temperature > 0:
				if retarders_rods > 7:
					reactive = fuel / ex + reactor_temperature / fuel
					reactor_temperature -= reactive
				else:
					reactive = fuel / ex
					reactor_temperature -= reactive

		previous_retarders_rods = retarders_rods

		if reactor_temperature > 0:
			xenon += 1
			xenon -= reactor_temperature / 500

		if xenon > 1000 and reactor_temperature > 0:
			if reactor_temperature < 100:
				p = reactor_temperature
			else:
				p = 100

			if retarders_rods == 0:
				reactor_temperature -= p
			else:
				reactor_temperature -= p / retarders_rods

		if fire_extinguishing_system == True:
			fire = False

		if fire == True:
			if reactor_temperature > 0:
				reactor_temperature += (reactor_temperature / 15) + 15
				reactor_pressure += 15
			else:
				reactor_pressure += 15

		if emergency_cooling == True and emergency_cooling_volume > 0:
			emergency_cooling_volume -= 1
			reactor_temperature -= 150

		if reactor_temperature > 1500 and meltdown == False:
			if x == 15:
				meltdown = True
			else:
				x += 1
		elif reactor_temperature <= 1500 and x > 0 and meltdown == False:
			x -= 1

		if meltdown == True and des_2_10(pump) > 0:
			turbine_temperature = (reactor_temperature / 5 + des_2_10(pump)) / 2
		elif des_2_10(pump) > 0:
			turbine_temperature = reactor_temperature / 5 + des_2_10(pump)

		if reactor_temperature <= des_2_10(pump) and i == pump:
			i = 0

			reactor_temperature -= turbine_temperature
		elif i == pump:
			i = 0

			if meltdown == True:
				reactor_temperature -= des_2_10(pump) * 15 / 2
			else:
				reactor_temperature -= des_2_10(pump) * 15

		if reactor_temperature < 0:
			reactor_temperature = 0
			continue

		if pump_check == False and turbine_temperature > 0:
			if turbine_temperature < 50:
				turbine_temperature -= turbine_temperature
			else:
				turbine_temperature -= 50

		reactor_pressure = reactor_temperature / 20
		power = turbine_temperature * 5
		money += power * 10

		if pressure_relief == True and reactor_pressure > 0:
			if reactor_pressure < 25:
				reactor_pressure -= reactor_pressure
			else:
				reactor_pressure -= 50
				
			radiation_level += 1

		parameters(retarders_rods, pump, fire, round(reactive, 2), round(reactor_temperature, 2), round(turbine_temperature, 2), pump_check, emergency_cooling_check, pressure_relief_check, fire_extinguishing_system_check, round(reactor_pressure, 2), emergency_cooling, emergency_cooling_volume, pressure_relief, fire_extinguishing_system, round(power, 2), round(radiation_level, 2), round(money, 2))

		if reactor_pressure > maximum_reactor_pressure:
			explosion = True

			os.system("cls")

			radiation_level = reactor_pressure * 10

			parameters(retarders_rods, pump, fire, round(reactive, 2), round(reactor_temperature, 2), round(turbine_temperature, 2), pump_check, emergency_cooling_check, pressure_relief_check, fire_extinguishing_system_check, round(reactor_pressure, 2), emergency_cooling, emergency_cooling_volume, pressure_relief, fire_extinguishing_system, round(power, 2), round(radiation_level, 2), round(money, 2))

			print("")
			print("Взрыв!")
			print("")
		else:
			time.sleep(tick)

			os.system("cls")

banner()

time.sleep(5)

os.system("cls")

window = sg.Window("БЩТ", layout, size=(500, 465), grab_anywhere=False, finalize=True)

threading.Thread(target=calc).start()

while True:
	event, values = window.read()

	if event == sg.WIN_CLOSED:
		break

	if event == "Изменить":
		if float(values["retarders_rods"]) < maximum_retarders_rods and float(values["retarders_rods"]) != retarders_rods and meltdown == False:
			time.sleep(2)
			retarders_rods = float(values["retarders_rods"])

		if float(values["pump"]) <= 10 and pump_check == True:
			pump = int(values["pump"])
			pump = des_10_2(pump)
	elif event == "АЗ-5":
		emergency_protection()
	elif event == "САОР":
		if emergency_cooling_check == True:
			if emergency_cooling == False:
				emergency_cooling = True
			else:
				emergency_cooling = False
	elif event == "Система сброса давления":
		if pressure_relief_check == True:
			if pressure_relief == False:
				pressure_relief = True
			else:
				pressure_relief = False
	elif event == "Система пожаротушения":
		if fire_extinguishing_system_check == True:
			if fire_extinguishing_system == False:
				fire_extinguishing_system = True
			else:
				fire_extinguishing_system = False
	elif event == "Починить ГЦН (500000 ₽)":
		if pump_check == False:
			if money >= 500000:
				money -= 500000
				pump_check = True
	elif event == "Починить САОР (150000 ₽)":
		if emergency_cooling_check == False:
			if money >= 250000:
				money -= 250000
				emergency_cooling_check = True
	elif event == "Починить клапан (150000 ₽)":
		if pressure_relief_check == False:
			if money >= 150000:
				money -= 150000
				pressure_relief_check = True
	elif event == "Починить систему пожаротушения (150000 ₽)":
		if fire_extinguishing_system_check == False:
			if money >= 150000:
				money -= 150000
				fire_extinguishing_system_check = True
	elif event == "Восстановить жидкий азот (500000 ₽)":
		if emergency_cooling_volume < 100:
			if money >= 500000:
				money -= 500000
				emergency_cooling_volume += 100 - emergency_cooling_volume

window.close()