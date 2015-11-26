#include "mbed.h"

struct struct_system
{
    uint8_t length              ;//1
    uint8_t ID                  ;//2
    uint8_t output      : 1     ;//3.0
    uint8_t use_gps     : 1     ;//3.1
    uint8_t flagbyte_2          ;//4
    double  lat_home            ;//12
    double  long_home           ;//20
    int8_t  sync                ;//4
    uint8_t ck                  ;//21
} sys = {21,0};

struct struct_position
{
    uint8_t  length             ;//1
    uint8_t  ID                 ;//2
    uint8_t  flagbyte_1         ;//3
    uint8_t  flagbyte_2         ;//4
    int16_t  hdg                ;//6        // @ rule: name=heading; expr=hdg * 20.1; unit=degrees
    int16_t  pitch              ;//8        // @ rule: name=pitch; expr=pitch * 10; unit=degrees
    uint8_t  ck                 ;//9
} position = {9,1};
