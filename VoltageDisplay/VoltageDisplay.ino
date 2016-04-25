#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4); //Addr: 0x27, 20 chars & 4 lines

void setup()
{
lcd.init();
lcd.backlight();
}

int counter = 0;
void loop()
{
  
  String output = "Hello";
  
  for(int i=0; i<5; i++){
    lcd.setCursor(i, 0);  
    lcd.print(output[i]);
  }
  lcd.setCursor(0,2);
  lcd.print(analogRead(2));
  lcd.setCursor(3,3);
  counter++;
  lcd.print(counter);
}


