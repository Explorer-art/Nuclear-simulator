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

fuel = 250
reactive = 0
reactor_temperature = 0
xenon = 0
turbine_temperature = 0
reactor_pressure = 0
maximum_retarders_rods = 11
power = 0
radiation_level = 0

retarders_rods = 0
previous_retarders_rods = 0
pump = 0

maximum_reactor_pressure = 100

explosion = False

layout = [
	[sg.Text("СУЗ")],
	[sg.Spin([sz for sz in range(0, 11)], font=("Helvetica 18"), change_submits=True, key="retarders_rods")],
	[sg.Text("ГЦН")],
	[sg.Spin([sz for sz in range(0, 101)], font=("Helvetica 18"), change_submits=True, key="pump")],
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

def emergency_protection():
	global retarders_rods

	retarders_rods = 0

def parameters(retarders_rods, pump, reactive, reactor_temperature, turbine_temperature, reactor_pressure, power, radiation_level):
	print("Реактивность: " + str(reactive))
	print("Температура реактора: " + str(reactor_temperature))
	print("Температура турбины: " + str(turbine_temperature))
	print("Давление в реакторе: " + str(reactor_pressure))
	print("СУЗ подняты на: " + str(retarders_rods))
	print("Мощность ГЦН: " + str(round(pump / 2 * 100, 2)) + "%")
	print("Мощность реактора: " + str(power) + " МВт")
	print("Уровень заражения: " + str(radiation_level))

def calc():
	global explosion, retarders_rods, previous_retarders_rods, pump, reactive, reactor_temperature, xenon, turbine_temperature, reactor_pressure, radiation_level, power

	p = 0

	while explosion == False:
		if reactor_temperature < 0:
			reactor_temperature = 0
			continue

		if retarders_rods == 0:
			ex = 1
		if retarders_rods == 1:
			ex = 250
		elif retarders_rods == 2:
			ex = 150
		elif retarders_rods == 3:
			ex = 100
		elif retarders_rods == 4:
			ex = 75
		elif retarders_rods == 5:
			ex = 50
		elif retarders_rods == 6:
			ex = 30
		elif retarders_rods == 7:
			ex = 20
		elif retarders_rods == 8:
			ex = 10
		elif retarders_rods == 9:
			ex = 5
		elif retarders_rods == 10:
			ex = 2

		if retarders_rods >= maximum_retarders_rods:
			reactive = (reactor_temperature + fuel) / ex
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
			if reactor_temperature <= retarders_rods * 100 and retarders_rods != maximum_retarders_rods:
				reactive = fuel / ex + reactor_temperature / fuel
				reactor_temperature += reactive
		elif p == 2:
			if reactor_temperature > 0 and reactor_temperature >= retarders_rods * 100 and retarders_rods != maximum_retarders_rods:
				reactive = fuel / ex + reactor_temperature / fuel
				reactor_temperature -= reactive

		previous_retarders_rods = retarders_rods

		if reactor_temperature > 0:
			xenon += 1
			xenon -= reactor_temperature / 750

		if xenon > 1000 and reactor_temperature > 0:
			if reactor_temperature < 100:
				p = reactor_temperature
			else:
				p = 100

			if retarders_rods == 0:
				reactor_temperature -= p
			else:
				reactor_temperature -= p / retarders_rods
				print(p / retarders_rods)

		turbine_temperature = reactor_temperature / 25 * pump
		reactor_temperature -= turbine_temperature
		reactor_pressure = reactor_temperature / 15
		power = turbine_temperature * 10

		parameters(retarders_rods, pump, round(reactive, 2), round(reactor_temperature, 2), round(turbine_temperature, 2), round(reactor_pressure, 2), round(power, 2), round(radiation_level, 2))

		if reactor_pressure > maximum_reactor_pressure:
			explosion = True

			radiation_level = reactor_pressure * 10

			parameters(retarders_rods, pump, round(reactive, 2), round(reactor_temperature, 2), round(turbine_temperature, 2), round(reactor_pressure, 2), round(power, 2), round(radiation_level, 2))

			print("")
			print("Взрыв!")
			print("")

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

		if float(values["pump"]) <= 100 and float(values["pump"]) != pump:
			pump = float(values["pump"]) * 0.02
	elif event == "АЗ-5":
		emergency_protection()

window.close()