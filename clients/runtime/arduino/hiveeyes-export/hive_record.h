#ifndef HIVE_RECORD_H_
#define HIVE_RECORD_H_

#include <Arduino.h>

typedef struct {
  float temperature_outside;
  float humidity_outside;
  float temperature_inside_1;
  float temperature_inside_2;
  float weight;
} Hive_record_type;

#endif /* ifndef HIVE_RECORD_H_ */
