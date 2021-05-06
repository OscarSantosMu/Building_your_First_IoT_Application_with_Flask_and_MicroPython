from machine import Pin, ADC
from time import sleep

adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)     # default configuration ADC.ATTN_0DB
adc.width(ADC.WIDTH_10BIT)   # default configuration ADC.WIDTH_12BIT

while True:
  pot_value = adc.read()
  print(pot_value)
  sleep(0.1)