## Stacking IGBTs:

### Different voltages across IGBTs in Off state can overload

Put a several megohm resistor across each IGBT. This should be lower than IGBT's actual off resistance. This will help spread the voltage evenly.

### IGBTs switch on at different times, leading to overvoltage on slow ones.

Use a snubber circuit across each IGBT. An RC snubber uses a capacitor to "absorb" the sudden increase in voltage across the slow IGBT. Effectively, it lowers the resistance temporarily while the voltage is rising. Look into RDC snubbers.

### 



## Driving:

Use opto-isolators for voltage differences?