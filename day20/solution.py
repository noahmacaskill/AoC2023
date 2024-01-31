from abc import ABC, abstractmethod
from collections import deque
import math

INPUT = 'input'
BROADCASTER = 'broadcaster'
LOW_PULSE = True
HIGH_PULSE = False

PART1 = False

class Module(ABC):
    """
    Parent class representing a module
    """
    pulse_receive_queue = deque()
    high_pulses, low_pulses = 0, 0
    rx_src_module = None
    high_src_pulses = []

    def __init__(self, name, dest_modules) -> None:
        self.name = name
        self.dest_modules = dest_modules

    """
    A dictionary of all the modules in the form (name (str): module (Module))
    """
    @classmethod
    def set_modules(cls, modules):
        cls.modules = modules

    """
    This is the module that connects to the rx module.
    Given that this module is a conjunction module, it sends a low pulse to rx only when it has received high pulses from all of its input modules.
    These high pulses arrive in a cyclical nature, thus, each time one arrives it is recorded.
    """
    @classmethod
    def set_rx_src_module(cls, rx_src_module):
        cls.rx_src_module = rx_src_module


    """
    Receives pulses in the order defined by the pulse_receive_queue.
    Keeps track of high pulses arrive to the rx_src_module
    """
    @classmethod
    def receive_pulses(cls):
        cls.high_src_pulses = []
        while cls.pulse_receive_queue:
            dest_module, pulse, src_module = cls.pulse_receive_queue.popleft()
            if dest_module == cls.rx_src_module and pulse == HIGH_PULSE:
                cls.high_src_pulses.append(src_module)
            
            dest_module = modules.get(dest_module, None)

            if dest_module is None:
                continue
            elif type(dest_module) is ConjunctionModule:
                dest_module.receive_pulse(pulse, src_module)
            else:
                dest_module.receive_pulse(pulse)

    """
    Pushes button to trigger a low pulse to the broadcaster module
    """
    @classmethod
    def push_button(cls):
        cls.pulse_receive_queue.append((BROADCASTER, LOW_PULSE, None))
        cls.low_pulses += 1
        cls.receive_pulses()

    """
    Pulse reception is defined in child classes
    """
    @abstractmethod
    def receive_pulse(self, pulse: bool):
        pass

    """
    Sends pulse to all destination modules
    """
    def send_pulse(self, pulse: bool):
        for module in self.dest_modules:
            if pulse == LOW_PULSE:
                Module.low_pulses += 1
            else:
                Module.high_pulses += 1

            Module.pulse_receive_queue.append((module, pulse, self.name))

class FlipFlopModule(Module):
    """
    Flip Flop modules are initally off (i.e. sends low pulses)
    """
    def __init__(self, name, dest_modules) -> None:
        super().__init__(name, dest_modules)
        self.pulse = LOW_PULSE
    
    """
    Flip Flop modules are activated by low pulses. They always send the opposite pulse to their last activated instance
    """
    def receive_pulse(self, pulse: bool):
        if pulse == LOW_PULSE:
            self.pulse = not self.pulse
            self.send_pulse(self.pulse)

class ConjunctionModule(Module):
    """
    Source modules and the previous pulse they sent must be remembered by Conjugation Modules
    """
    def __init__(self, name, dest_modules) -> None:
        super().__init__(name, dest_modules)
        self.src_modules = {}

    """
    Append a source module. Low pulses are initally remembered for each source module.
    """
    def append_src_module(self, module):
        self.src_modules[module] = LOW_PULSE

    """
    Conjunction modules send a low pulse only when all source modules have sent a high pulse, else send a high pulse
    """
    def receive_pulse(self, pulse: bool, src: str):
        self.src_modules[src] = pulse
        
        if all(pulse == HIGH_PULSE for pulse in self.src_modules.values()):
            self.send_pulse(LOW_PULSE)
        else:
            self.send_pulse(HIGH_PULSE)

class BroadcastModule(Module):
    def __init__(self, name, dest_modules) -> None:
        super().__init__(name, dest_modules)

    """
    Broadcast module broadcasts the pulse it has received
    """
    def receive_pulse(self, pulse: bool):
        self.send_pulse(pulse)

def parse_module(text: str) -> (str, Module):
    """
    Parses plain text into a module

    Parameters:
    text (str): Raw text

    Returns:
    (str, Module):
        str: module name
        Module: module
    """
    name, dest_modules = text.split(" -> ")
    dest_modules = dest_modules.split(', ')
    
    if name[0] == '%':
        return (name[1:], FlipFlopModule(name[1:], dest_modules))
    elif name[0] == '&':
        return (name[1:], ConjunctionModule(name[1:], dest_modules))
    else: # Broadcaster
        return (name, BroadcastModule(name[1:], dest_modules))

# Parse modules
modules = {}
with open(INPUT) as f:
    for line in f:
        line = line.strip()
        name, module = parse_module(line)
        modules[name] = module

# Identify source modules of conjunction modules
for name, module in modules.items():
    for dest_module in module.dest_modules:
        if type(modules.get(dest_module, None)) is ConjunctionModule:
            modules[dest_module].append_src_module(name)

Module.set_modules(modules)

if PART1:
    for i in range(1000):
        Module.push_button()

    print(f"ANSWER: {Module.low_pulses*Module.high_pulses}")
else: # Part 2
    # Identify rx source module
    src_module = None
    for name, module in modules.items():
        if 'rx' in module.dest_modules:
            src_module = name
    
    Module.set_rx_src_module(src_module)

    # Identify feeder modules into rx source module
    feeder_modules = []
    for name, module in modules.items():
        if src_module in module.dest_modules:
            feeder_modules.append(name)

    iterations = 0
    cycles = []
    while feeder_modules:
        Module.push_button()
        iterations += 1

        # Note the cyclical nature of the feeder modules
        for module in Module.high_src_pulses:
            cycles.append(iterations)
            feeder_modules.remove(module)
    
    # LCM of the cycle lenghts is the number of iterations until a low pulse is sent to rx
    print(f"ANSWER: {math.lcm(*cycles)}")
