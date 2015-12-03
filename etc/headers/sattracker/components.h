#include "stdio.h"

struct struct_system
{
    uint8_t length              ;//1
    uint8_t ID                  ;//2
    uint8_t output      : 1     ;//3.0
    uint8_t use_gps     : 1     ;//3.1
    uint8_t fast        : 1     ;//3.2
    uint8_t slow        : 1     ;//3.3
    uint8_t flagbyte_2          ;//4 
    float   hdg                 ;//8    
    float   pitch               ;//12
    int8_t  sync                ;//13
    int8_t  drive_x_i           ;//14
    int8_t  drive_z_i           ;//15
    uint8_t ck                  ;//16
} sys = {16,0};

struct struct_position         
{
    uint8_t  length             ;//1
    uint8_t  ID                 ;//2
    uint8_t  flagbyte_1         ;//3
    uint8_t  flagbyte_2         ;//4
    int16_t  hdg                ;//6 // @rule: name=Heading; expr=hdg * 0.1;unit=degrees
    int16_t  pitch              ;//8 // @rule: name=Pitch; expr=pitch * 0.1; unit=degrees       
    uint8_t  ck                 ;//9
} position ={9, 1};

uint8_t* struct_id[]  = {
                           &sys.length,     //ID0
                           &position.length //ID1
                        };  