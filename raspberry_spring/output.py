
class OutputService:

    def __init__(self, test: bool=False) -> None:

        self.test = test

        if not self.test:
            from raspberry_pi import RaspberryPiDriver
            self.driver = RaspberryPiDriver()

    def on(self, pin: int) -> None:
        if not self.test:
            self.driver.on(pin)
        else:
            print('Turning on pin {pin}'.format(pin=pin))

    def off(self, pin: int) -> None:
        if not self.test:
            self.driver.off(pin)
        else:
            print('Turning off pin {pin}'.format(pin=pin))

    def clean_up(self):
        if not self.test:
            self.driver.clean_up()
