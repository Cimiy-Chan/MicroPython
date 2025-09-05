from machine import Pin
from time import sleep

__version__ = '1.0.3'
__author__ = 'Teeraphat Kullanankanjana, modified by CimiyChan'


class KeypadException(Exception):
    """
    Exception class for keypad-related errors.
    """
    pass


class Keypad:
    def __init__(self, row_pins, column_pins, keys):
        """
        Initialize the keypad object.

        Args:
            row_pins (list): List of row pins.
            column_pins (list): List of column pins.
            keys (list): 2D list representing the key layout.

        Raises:
            KeypadException: If pins or keys are not properly defined.
        """
        if not all(isinstance(pin, Pin) for pin in row_pins):
            raise KeypadException("Row pins must be instances of Pin.")

        if not all(isinstance(pin, Pin) for pin in column_pins):
            raise KeypadException("Column pins must be instances of Pin.")

        if not isinstance(keys, list) or not all(isinstance(row, list) for row in keys):
            raise KeypadException("Keys must be a 2D list.")

        self.row_pins = row_pins
        self.column_pins = column_pins
        self.keys = keys

        for pin in self.row_pins:
            pin.init(Pin.IN, Pin.PULL_UP)

        for pin in self.column_pins:
            pin.init(Pin.OUT)

        if len(self.row_pins) != len(self.keys) or len(self.column_pins) != len(self.keys[0]):
            raise KeypadException("Number of row/column pins does not match the key layout size.")

    def read_keypad(self):
        """
        Read the keypad and return the pressed key.

        Returns:
            str or None: Pressed key or None if no key is pressed.

        Raises:
            KeypadException: If pins or keys are not properly defined.
        """
        if not self.column_pins:
            raise KeypadException("No column pins defined.")

        if not self.row_pins:
            raise KeypadException("No row pins defined.")

        if not self.keys:
            raise KeypadException("No key layout defined.")

        for col_pin in self.column_pins:
            col_pin.value(0)  # Set column pin to LOW
            for i, row_pin in enumerate(self.row_pins):
                if not row_pin.value():  # If row pin reads LOW
                    key_pressed = self.keys[i][self.column_pins.index(col_pin)]
                    col_pin.value(1)  # Set column pin back to HIGH
                    return key_pressed
            col_pin.value(1)  # Set column pin back to HIGH
        return None  # Return None if no key is pressed

    def read_keypad_char(self):
        """
        Wait for keypad press and return a key value:
        :return: Key char value. Should be '0' to '9', 'A' to 'D', '*', '#'
        """
        keypad_val = None

        while keypad_val == None:
            keypad_val = self.read_keypad()
            sleep(0.1)
            if keypad_val != None:
                return keypad_val

    def read_keypad_string(self, end_char = '#', end_str ='**00'):
        """
        Wait for keypad press a string of char until the 'end' char or a end string is pressed.
        :return:
        """

        keypad_val = None
        default_end_str = '**00'
        keypad_str = ''
        while keypad_val != end_char and keypad_str != default_end_str:
            keypad_val = self.read_keypad_char()
            keypad_str +=keypad_val
            sleep(0.1)
        if (keypad_str == default_end_str):
            return keypad_str
        else:
            return keypad_str[:len(keypad_str)-1]


#Debug entry point
if __name__ == '__main__':
    # Define GPIO pins for rows
    column_pins = [Pin(0), Pin(1), Pin(2), Pin(3)]

    # Define GPIO pins for columns
    row_pins = [Pin(4), Pin(5), Pin(6), Pin(7)]

    # Define keypad layout
    keys = [
        ['D', 'C', 'B', 'A'],
        ['#', '9', '6', '3'],
        ['0', '8', '5', '2'],
        ['*', '7', '4', '1']]
    obj_keypad = Keypad(row_pins, column_pins, keys)

    while True:
        print(f'Please press keys and end with #')
        keypad_str = obj_keypad.read_keypad_string()
        print (f'String: {keypad_str}')
        if keypad_str == '**00':
            print (f'End application...')
            break

    """
    while True:
        keypad_val = obj_keypad.read_keypad_char()
        print (f'Read keypad value: {keypad_val}')
        sleep(0.2)
        if (keypad_val == '*'):
            print ('End application...')
            break
    """
