#ifndef HIVEEYES_CLIENT_H_
#define HIVEEYES_CLIENT_H_

#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

bool decode_data(WiFiClient& json) {

  // Allocate the JsonDocument
  DynamicJsonDocument doc(35 * 1024);

  // Deserialize the JSON document.
  DeserializationError error = deserializeJson(doc, json);

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return false;
  }

  // Convert to JsonObject.
  //JsonObject root = doc.as<JsonObject>();

  // Get the first element of the array.
  JsonObject first = doc[0];

  // Decode data.
  hive_data[0].temperature_outside    = first["temperature.0x77.i2c:0"];
  hive_data[0].humidity_outside       = first["humidity.0x77.i2c:0"];
  hive_data[0].temperature_inside_1   = first["temperature.28ff641d8fc3944f.onewire:0"];
  hive_data[0].temperature_inside_2   = first["temperature.28ff641d8fdf18c1.onewire:0"];
  hive_data[0].weight                 = first["weight.0"];

  return true;
}

bool obtain_hiveeyes_data(WiFiClient& client) {

  // Define URI.
  // https://getkotori.org/docs/handbook/export/
  HTTPClient http;
  String server = "swarm.hiveeyes.org";

  // TODO: Improve Kotori by requesting only last reading.
  String uri = "/api-notls/hiveeyes/testdrive/area-38/fipy-workbench-01/data.json?from=2020-05-20T00:00:00&to=2020-05-20T00:01:00";

  // Make HTTP request.
  //http.begin(uri, test_root_ca); // HTTPS example connection
  bool success;
  http.begin(client, server, 80, uri);
  int httpCode = http.GET();
  if (httpCode == HTTP_CODE_OK) {
    if (!decode_data(http.getStream())) return false;
    success = true;

  } else {
    Serial.printf("Connection failed, error: %s", http.errorToString(httpCode).c_str());
    success = false;
  }

  client.stop();
  http.end();
  return success;
}

#endif /* ifndef HIVEEYES_CLIENT_H_ */
