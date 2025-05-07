from abc import ABC, abstractmethod
from typing import Union


class Light:
    def __init__(self):
        self.on = False

    def turn_on(self):
        if self.on == True:
            print("The light is already on")
            return
        self.on = True
        print("Light is on")
        return

    def turn_off(self):
        if self.on == False:
            print("The light is already off")
            return
        self.on = False
        print("Light is off")
        return

    def __str__(self):
        return f"Light: state {self.on}"


class Thermostat:
    def __init__(self):
        self.on = False
        self.temperature = 0

    def turn_on(self):
        if self.on == True:
            print("The thermostat is already on")
            return
        self.on = True
        print("Thermostat is on")
        return

    def turn_off(self):
        if self.on == False:
            print("The thermostat is already off")
            return
        self.on = False
        print("Thermostat is off")
        return

    def increase_temperature(self):
        if self.on == False:
            print("The thermostat is off")
            return
        self.temperature += 1
        print("Temperature increased to ", self.temperature)

    def decrease_temperature(self):
        if self.on == False:
            print("The thermostat is off")
            return
        self.temperature -= 1
        print("Temperature decreased to ", self.temperature)

    def __str__(self):
        if self.on == True:
            return f"Thermostat: state {self.on}, temperature {self.temperature}"
        return f"Thermostat: state {self.on}"


class Command(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    def __repr__(self):
        return self.__class__.__name__


class MacroCommand(Command):
    def __init__(self, commands: list[Command]):
        self.commands = commands

    def execute(self):
        for cmd in self.commands:
            cmd.execute()
        return

    def undo(self):
        for cmd in reversed(self.commands):
            cmd.undo()
        return


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()


class ThermostatOnCommand(Command):
    def __init__(self, thermostat: Thermostat):
        self.thermostat = thermostat

    def execute(self):
        self.thermostat.turn_on()

    def undo(self):
        self.thermostat.turn_off()


class ThermostatOffCommand(Command):
    def __init__(self, thermostat: Thermostat):
        self.thermostat = thermostat

    def execute(self):
        self.thermostat.turn_off()

    def undo(self):
        self.thermostat.turn_on()


class ThermostatIncreaseTemperatureCommand(Command):
    def __init__(self, thermostat: Thermostat):
        self.thermostat = thermostat

    def execute(self):
        self.thermostat.increase_temperature()

    def undo(self):
        self.thermostat.decrease_temperature()


class ThermostatDecreaseTemperatureCommand(Command):
    def __init__(self, thermostat: Thermostat):
        self.thermostat = thermostat

    def execute(self):
        self.thermostat.decrease_temperature()

    def undo(self):
        self.thermostat.increase_temperature()


class RemoteControl:
    def __init__(self):
        self.history: list[Command] = []
        self.undo_stack: list[Command] = []
        self.slot_stack: dict[int, Union[Command, None]] = {}

    def create_slot(self):
        new_slot = (max(self.slot_stack) if self.slot_stack else 0) + 1
        self.slot_stack[new_slot] = None
        return new_slot

    def list_slot_stack(self):
        if not self.slot_stack:
            print("Empty slot stack")
            return
        print("Slot Stack:\n")
        for slot, cmd in self.slot_stack.items():
            print(f"Slot: {slot}; Command: {cmd}")

    def set_command_to_slot(self, slot: int, command: Command):
        if slot not in self.slot_stack:
            print(f"Slot {slot} not found")
            return
        self.slot_stack[slot] = command

    def press_button(self, command: Command):
        if command is None:
            print("Command is empty")
            return
        self.history.append(command)
        self.undo_stack.clear()
        command.execute()
        return

    def press_slot_button(self, slot: int):
        if slot not in self.slot_stack:
            print(f"Slot {slot} not found")
            return
        if self.slot_stack[slot] == None:
            print("Slot is empty")
            return
        self.press_button(self.slot_stack[slot])

    def undo_last_command(self):
        if not self.history:
            print("No commands to undo")
            return
        last = self.history.pop()
        self.undo_stack.append(last)
        last.undo()
        return

    def redo_last_command(self):
        if not self.undo_stack:
            print("No commands to redo")
            return
        last = self.undo_stack.pop()
        self.history.append(last)
        last.execute()
        return

    def get_commands(self):
        print(f"history: {self.history}\nundo_stack: {self.undo_stack}")
        return


# light = Light()
# thermostat = Thermostat()
# remote = RemoteControl()
# light_on = LightOnCommand(light)
# light_off = LightOffCommand(light)
# thermostat_on = ThermostatOnCommand(thermostat)
# thermostat_off = ThermostatOffCommand(thermostat)
# remote.press_button(light_on)
# remote.press_button(light_off)
# remote.undo_last_command()
# remote.redo_last_command()
# remote.press_button(thermostat_on)
# remote.get_commands()
# remote.undo_last_command()
# remote.undo_last_command()
# remote.get_commands()

# macro = MacroCommand([light_on, light_on, thermostat_on, thermostat_off])
# remote.press_button(macro)
# remote.get_commands()
# remote.undo_last_command()

# slot_stack = {1: "test", 2: "test"}
# slot_stack_null = {}

# remote.create_slot()
# remote.create_slot()
# remote.create_slot()
# remote.set_command_to_slot(1, light_on)
# remote.set_command_to_slot(2, thermostat_on)
# remote.list_slot_stack()
# remote.press_slot_button(1)
# remote.undo_last_command()
# remote.redo_last_command()
# remote.press_slot_button(3)
# remote.press_button(remote.slot_stack[3])
