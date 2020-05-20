#include "hive_record.h"

enum alignment {LEFT, RIGHT, CENTER};

Hive_record_type hive_data[1];
#include "hiveeyes_client.h"


void setup() {

  WiFiClient client;

  // Obtain weather information.
  //obtain_wx_data(client, "weather");

  // Obtain hive information.
  obtain_hiveeyes_data(client);

  DisplayWeather();
}

// This will never run.
void loop() {
}

void DisplayWeather() {                 
  //DrawHeadingSection();
  //DrawMainWeatherSection(172, 70);
  //DrawForecastSection(233, 15);
  //DisplayPrecipitationSection(233, 82);
  DrawHiveSection(233, 82);
}

void DrawHiveSection(int x, int y) {
  //u8g2Fonts.setFont(FONT(u8g2_font_helvB14));
  //drawString(x - 25, y - 22, String(hive_data[0].temperature_inside_1, 1) + "°C", CENTER);
  //u8g2Fonts.setFont(FONT(u8g2_font_helvB12));
  //drawString(x + 30, y - 22, String(hive_data[0].humidity_outside, 0) + "%", CENTER);
  //u8g2Fonts.setFont(FONT(u8g2_font_helvB10));
}
