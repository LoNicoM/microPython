# main.py
# sequence of events


# imports
import socket
from umqtt.simple import MQTTClient
from utime import sleep

server_name = "serv.lon.home"
unique_id = "garage_door"
username = "" # put it here
passwd = "" # put yours here
subs = ["garage/door", "garage/light"]
server_ip = ""


def mqtt_callback(sub, mesg):
    if sub == bytearray(subs[0]) and mesg == b"SuperSecure!":
        print("Accessing Maglocks...")
        blink_led(5, 0.1, 2)
        button_press(4)
    if sub == bytearray(subs[1]) and mesg == b"on":
        print("Turning Light on!")
        blink_led(3, 0.1, 2)
        switch_pin(5, 1)
    if sub == bytearray(subs[1]) and mesg == b"off":
        print("Turning Light off!")
        blink_led(2, 0.1, 2)
        switch_pin(5)


def lookup_server():
    global server_ip
    server_ip = socket.getaddrinfo(server_name, 1883)[0][-1][0]


def blink_led(flashes=5, speed=0.25, led=1):
    from machine import Pin
    from machine import Signal
    from time import sleep
    pin = 16 if led == 1 else 2
    led = Pin(pin, Pin.OUT)
    led = Signal(led, invert=True)
    for i in range(flashes):
        led.on()
        sleep(speed)
        led.off()
        sleep(speed)


def button_press(gpio_pin):
    from machine import Pin
    from utime import sleep
    button = Pin(gpio_pin, Pin.OUT)
    button.on()
    sleep(1)
    button.off()


def switch_pin(gpio_pin, state=0):
    from machine import Pin
    switch = Pin(gpio_pin, Pin.OUT)
    if state == 1:
        switch.on()
    else:
        switch.off()


def main_loop():
    loop_counter = 0
    retry_count = 0
    # TODO; Implement task list
    # tasks = []
    #
    # def task_handler(task):
    #     if task == "pub_status()":
    #         MQTTClient.publish("garage/door/status", Pin.)

    while True:
        try:
            print("Looking up {}...".format(server_name), end="")
            while True:
                try:
                    lookup_server()
                    print("success...{}".format(server_ip))
                    break
                except OSError:
                    print(".", end="")
                    sleep(10)
                    continue

            while True:
                try:
                    client = MQTTClient(unique_id, server_ip, user=username, password=passwd)
                    client.set_callback(mqtt_callback)
                    client.connect()
                    print("Connected to {}".format(server_name))
                    blink_led(3, 0.05, 1)  # indicate connection was success
                    print("Subscribing to...")
                    for item in subs:
                        print(item)
                        client.subscribe(item)
                    print("Done...entering tasking loop.")

                    while True:
                        if loop_counter == 10:
                            blink_led(1, 0.05, 2)  # short blink led to confirm connection active
                            loop_counter = 0
                        client.check_msg()
                        loop_counter += 1
                        sleep(1)  # check for new messages every second approx.

                except OSError:
                    if retry_count == 5:
                        raise OSError
                    print("Not Connected..retrying")
                    blink_led(1, 1, 2)  # long blink to indicate not connected
                    retry_count += 1
                    sleep(9)
                    continue

        except OSError:
            print("Server not responding, looking up ip...")
            retry_count = 0
            continue


main_loop()
