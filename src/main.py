"""
Created on 2021-05-05

@author: Oscar Alberto Santos Muñoz

"""

class MicroController:
    
    init_id = 1

    def __init__(self, pin):

        from machine import ADC
        self.id = MicroController.init_id
        self.pin = pin
        self.attn = self.pin.atten(ADC.ATTN_11DB)
        self.width = self.pin.width(ADC.WIDTH_12BIT)
        MicroController.init_id += 1

    def get_id(self):
        """ Return the id assigned to this pin """
        
        return self.id

    def read(self):
        """ Call this method to read the value of the adc pin """

        return self.pin.read()
    
    def get(self, base_url, params):
        """ Call this method to do a get request from your MicroController """

        import urequests
        message = ''
        for i in params:
            message += '{}={}&'.format(i, params[i])
        message = message[:-1]
        url = '{}?{}'.format(base_url, message)
        response = urequests.get(url)

        if response.status_code == 200:
            print('OK')
        
        response.close()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ssid', 'password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
   
def main():

    from machine import Pin, ADC
    from time import sleep
    import urequests
    do_connect()
    esp32 = MicroController(ADC(Pin(35)))

    while True:

        value = esp32.read()

        # do something with the value
        physical_quantity = value*0.08/2   # example
        # end of calculations

        payload = {'esp32_pin_id': esp32.get_id(), \
                    'value_{}'.format(esp32.get_id()): value, \
                    'physical_quantity_{}'.format(esp32.get_id()): physical_quantity}

        esp32.get('http://192.168.1.8:5000/receive', params=payload)

        sleep(1)

if __name__ == '__main__':
    main()