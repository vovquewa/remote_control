import flet as ft

# import sys
# from pathlib import Path

# sys.path.append(str(Path(__file__).resolve().parent.parent))  # Добавляет src/
# import os

# print("PYTHONPATH:", os.getenv("PYTHONPATH"))
from core.command import (
    Light,
    Thermostat,
    RemoteControl,
    LightOnCommand,
    LightOffCommand,
    ThermostatOnCommand,
    ThermostatOffCommand,
)


def main(page: ft.Page):
    page.title = "Пульт управления"
    page.window_width = 400
    page.window_height = 600
    page.scroll = "AUTO"

    history = ft.Text(value="История действий:", selectable=True)
    history_log = ft.Column()

    light = Light()
    thermostat = Thermostat()
    remote = RemoteControl()
    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)
    thermostat_on = ThermostatOnCommand(thermostat)
    thermostat_off = ThermostatOffCommand(thermostat)

    remote.create_slot()
    remote.create_slot()
    remote.create_slot()
    remote.create_slot()
    remote.set_command_to_slot(1, light_on)
    remote.set_command_to_slot(2, thermostat_on)
    remote.set_command_to_slot(3, light_off)
    remote.set_command_to_slot(4, thermostat_off)
    remote.list_slot_stack()

    thermostat_icon = ft.Icon(name=ft.icons.ALARM_OFF, color=ft.colors.RED)
    light_icon = ft.Icon(name=ft.icons.LIGHT_MODE, color=ft.colors.RED)

    def update_icons():
        light_icon.color = ft.colors.GREEN if light.on else ft.colors.RED
        thermostat_icon.name = ft.icons.ALARM if thermostat.on else ft.icons.ALARM_OFF
        thermostat_icon.color = ft.colors.GREEN if thermostat.on else ft.colors.RED
        light_icon.update()
        thermostat_icon.update()

    def log_action(text):
        history_log.controls.append(ft.Text(text))
        update_icons()
        page.update()

    def on_light_on_click(e):
        remote.press_slot_button(1)
        print(light.on)
        log_action("Свет включен")

    def on_light_off_click(e):
        remote.press_slot_button(3)
        print(light.on)
        log_action("Свет выключен")

    def on_thermo_on_click(e):
        remote.press_slot_button(2)
        log_action("Термостат включен")

    def on_thermo_off_click(e):
        remote.press_slot_button(4)
        log_action("Термостат выключен")

    def on_undo(e):
        remote.undo_last_command()
        log_action("⮪ Undo нажат")

    def on_redo(e):
        remote.redo_last_command()
        log_action("⮫ Redo нажат")

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Пульт управления", size=24, weight="bold", text_align="CENTER"
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Свет ON", on_click=on_light_on_click),
                        ft.ElevatedButton("Свет OFF", on_click=on_light_off_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Термостат ON", on_click=on_thermo_on_click),
                        ft.ElevatedButton(
                            "Термостат OFF", on_click=on_thermo_off_click
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.UNDO, on_click=on_undo),
                        ft.IconButton(icon=ft.icons.REDO, on_click=on_redo),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        thermostat_icon,
                        light_icon,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                history,
                history_log,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Вот это ключ
        )
    )


# ft.app(target=main)


def run_app():
    ft.app(target=main)
