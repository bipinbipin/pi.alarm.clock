import gaugette.gpio
import gaugette.switch

SW_PIN = 5
gpio = gaugette.gpio.GPIO()
sw = gaugette.switch.Switch(gpio, SW_PIN)
last_state = sw.get_state()
while True:
    state = sw.get_state()
    if state != last_state:
        print("switch %d" % state)
        last_state = state