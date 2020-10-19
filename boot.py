# boot.py define all functions required keep imports inside functions
# does this save memory?, not that im going to use it all or anything
def webrepl_start():
    import webrepl
    webrepl.start()


def wifi_connect(mode=0):
    import network
    import utime
    wlan = network.WLAN(network.STA_IF)

    def print_ip():
        print("WLAN is connected.")
        print("IP          = {0}".format(wlan.ifconfig()[0]))
        print("Subnet Mask = {0}".format(wlan.ifconfig()[1]))
        print("DNS         = {0}".format(wlan.ifconfig()[2]))
        print("Gateway     = {0}".format(wlan.ifconfig()[3]))

    if mode == 0:
        ssid = "" # put yours here
	passwd = "" # likewise
        timeout = 0
        if not wlan.isconnected():
            print("Trying to Connect.", end="")
            wlan.active(True)
            wlan.connect(ssid, passwd)
            while not wlan.isconnected():
                utime.sleep(3)
                print(".", end="")
                timeout += 1
                if timeout == 5:
                    print("WLAN is taking a long time, maybe it's unavailable?")
            print_ip()
        else:
            print_ip()
    
    elif mode == 1:
        return wlan.isconnected()


def get_time():
    from machine import RTC
    rtc = RTC()
    t = rtc.datetime()
    print("Current time: {:02}:{:02}:{:02} {}/{}/{}".format(t[4], t[5], t[6], t[2], t[1], t[0]))


def set_time():
    import ntptime
    from machine import RTC
    rtc = RTC()
    if wifi_connect(mode=1):
        ntptime.settime()
        temp = list(rtc.datetime())
        temp[4] += 10
        if temp[4] >= 24:
            temp[4] -= 24
        rtc.datetime(temp)
        print("Internet time set.")
        get_time()
    else:
        print("Couldn't set time, no network.")


def readfile(filename):
    file = open(filename, "r")
    print(file.read())
    file.close()


webrepl_start()
wifi_connect()
set_time()
