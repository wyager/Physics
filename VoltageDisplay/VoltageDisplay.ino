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
  uint32_t raw = analogRead(1);
  uint32_t potVoltage = (raw * 5000) / 1024;
  uint32_t outVoltage = (raw * 1500) / 1024;
  
  displayString(0,0,"Est. output:");
  displayNumber(12,0,4,outVoltage);
  displayString(16,0,"V");
    
  displayString(0,1,"Pot voltage:");
  displayNumber(12,1,4,potVoltage);
  displayString(16,1,"mV");
  
  displayString(0,3,"Raw ADC:");
  displayNumber(8,3,4,raw);
//  displayNumber(4,1,4,raw);
//  counter++;
//  displayNumber(0,2,6,counter);
}

void displayString(int x, int y, char* str){
  for(int i=0; str[i] != 0; i++){
    lcd.setCursor(x+i,y);
    lcd.print(str[i]);
  }
}

void displayNumber(int x, int y, int width, int number){
  for(int xpos = x + width - 1; xpos >= x; xpos--){
    lcd.setCursor(xpos,y);
    lcd.print(number % 10);
    number /= 10;
  }
}

