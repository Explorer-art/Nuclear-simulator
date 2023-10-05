#!usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
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

explosion = False

layout = [
	[sg.Text("СУЗ")],
	[sg.Spin([sz for sz in range(0, 11)], font=("Helvetica 18"), change_submits=True, key="retarders_rods")],
	[sg.Text("ГЦН")],
	[sg.Spin([sz for sz in range(0, 11)], font=("Helvetica 18"), change_submits=True, key="pump")],
	[sg.Button("Изменить")],
	[sg.Button("АЗ-5")]
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

def emergency_protection():
	global retarders_rods, previous_retarders_rods

	retarders_rods = 0
	previous_retarders_rods = 0

def parameters(retarders_rods, pump, reactive, reactor_temperature, turbine_temperature, reactor_pressure, power, radiation_level, money):
	print("Реактивность: " + str(reactive))
	print("Температура реактора: " + str(reactor_temperature))
	print("Температура турбины: " + str(turbine_temperature))
	print("Давление в реакторе: " + str(reactor_pressure))
	print("СУЗ подняты на: " + str(retarders_rods))
	print("Мощность ГЦН: " + str(des_2_10(pump) / 10 * 100) + "%")
	print("Мощность реактора: " + str(power) + " МВт")
	print("Уровень заражения: " + str(radiation_level))
	print("")
	print("Деньги: " + str(money) + "₽")

def calc():
	global tick, explosion, retarders_rods, previous_retarders_rods, pump, reactive, reactor_temperature, xenon, turbine_temperature, reactor_pressure, radiation_level, power, money

	p = 0

	i = 0

	while explosion == False:
		i += 1

		if i > 10:
			i = 0

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

		if retarders_rods > 7:
			reactive = fuel / ex + reactor_temperature / fuel
			reactor_temperature += reactive

		if retarders_rods == 0:
			p = 0
		elif retarders_rods > previous_retarders_rods:
			p = 1
		elif retarders_rods < previous_retarders_rods:
			p = 2

		if p == 0:
			if reactor_temperature > 0:
				reactive = fuel / ex + reactor_temperature / fuel
				reactor_temperature -= reactive + maximum_retarders_rods
		elif p == 1:
			if reactor_temperature <= retarders_rods * 150 and retarders_rods <= 7:
				reactive = fuel / ex + reactor_temperature / fuel
				reactor_temperature += reactive
		elif p == 2:
			if reactor_temperature > 0 and reactor_temperature >= retarders_rods * 150 and retarders_rods <= 7:
				reactive = fuel / ex + reactor_temperature / fuel
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

		if reactor_temperature <= des_2_10(pump) and i == pump:
			i = 0

			turbine_temperature = reactor_temperature
			reactor_temperature -= turbine_temperature
		elif i == pump:
			i = 0
			
			turbine_temperature = reactor_temperature / 5 + des_2_10(pump)
			reactor_temperature -= turbine_temperature

		if reactor_temperature < 0:
			reactor_temperature = 0
			continue

		reactor_pressure = reactor_temperature / 15
		power = turbine_temperature * 2
		money += power * 100

		parameters(retarders_rods, pump, round(reactive, 2), round(reactor_temperature, 2), round(turbine_temperature, 2), round(reactor_pressure, 2), round(power, 2), round(radiation_level, 2), round(money, 2))

		if reactor_pressure > maximum_reactor_pressure:
			explosion = True

			radiation_level = reactor_pressure * 10

			parameters(retarders_rods, pump, round(reactive, 2), round(reactor_temperature, 2), round(turbine_temperature, 2), round(reactor_pressure, 2), round(power, 2), round(radiation_level, 2), round(money, 2))

			print("")
			print("Взрыв!")
			print("")
		else:
			time.sleep(tick)

			os.system("cls")

window = sg.Window("БЩТ", layout, size=(500, 250), grab_anywhere=False, finalize=True)

threading.Thread(target=calc).start()

while True:
	event, values = window.read()

	if event == sg.WIN_CLOSED:
		break

	if event == "Изменить":
		if float(values["retarders_rods"]) < maximum_retarders_rods and float(values["retarders_rods"]) != retarders_rods:
			time.sleep(5)
			retarders_rods = float(values["retarders_rods"])

		if float(values["pump"]) <= 10:
			pump = int(values["pump"])
			pump = des_10_2(pump)
	elif event == "АЗ-5":
		emergency_protection()

window.close()