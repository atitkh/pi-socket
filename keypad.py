import RPi.GPIO as GPIO
import time

class Keypad:
    def __init__(self):
        self.L1 = 25
        self.L2 = 8
        self.L3 = 7
        self.L4 = 1

        self.C1 = 12
        self.C2 = 16
        self.C3 = 20
        self.C4 = 21

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(self.C1) == 1:
            return characters[0]
        if GPIO.input(self.C2) == 1:
            return characters[1]
        if GPIO.input(self.C3) == 1:
            return characters[2]
        if GPIO.input(self.C4) == 1:
            return characters[3]
        GPIO.output(line, GPIO.LOW)

    def readKeypad(self):
        try:
            while True:
                # call the readLine function for each row of the keypad
                key = self.readLine(self.L1, ["1","2","3","A"])
                if key:
                    return key
                key = self.readLine(self.L2, ["4","5","6","B"])
                if key:
                    return key
                key = self.readLine(self.L3, ["7","8","9","C"])
                if key:
                    return key
                key = self.readLine(self.L4, ["*","0","#","D"])
                if key:
                    return key
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nApplication stopped!")