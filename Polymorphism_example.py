class Light:
    def turn_on(self):
        return "Light Is Now ON.Room Is Bright!"
    
class Fan:
    def turn_on(self):
        return "Fan Is Spinning At The Speed Of 3"
class AC:
    def turn_on(self):
        return "AC Is ON.Temperature Set To 22°C"
def active_device(device):
    print(device.turn_on())
    
my_light=Light()
my_fan=Fan()
my_ac=AC()
print("----Activating Smart Home Devices----")
active_device(my_light)
active_device(my_fan)
active_device(my_ac)