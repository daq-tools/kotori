#include "stdio.h"

struct struct_system
{
    uint8_t  length              ;//1
    uint8_t  ID                  ;//2
    uint8_t  flag1       : 1     ;//3.0
    uint8_t  flag2       : 1     ;//3.1
    uint8_t  flag3       : 1     ;//3.2
    uint8_t  flag4       : 1     ;//3.3
    uint8_t  flag5       : 1     ;//3.4
    uint8_t  flag6       : 1     ;//3.5
    uint8_t  flag7       : 1     ;//3.6
    uint8_t  flag8       : 1     ;//3.7
    uint8_t  flag9       : 1     ;//3.0
    uint8_t  flag0       : 1     ;//4.1
    uint8_t  flagA       : 1     ;//4.2
    uint8_t  flagB       : 1     ;//4.3
    uint8_t  flagC       : 1     ;//4.4
    uint8_t  flagD       : 1     ;//4.5
    uint8_t  flagE       : 1     ;//4.6
    uint8_t  flagF       : 1     ;//4.7 
    uint8_t  Amax                ;//5    
    uint8_t  RPsmax              ;//6
    uint8_t  PWMmax              ;//7  @rule: name=Max.PWM; expr=1200+PWMmax*3; unit=ys
    uint8_t  PWMmin              ;//8  @rule: name=Min.PWM; expr=1200+PWMmin*3; unit=yss
    uint8_t  t_max               ;//10 @rule: name=Max.Temperatur; expr=t_max; unit=degrees
    int16_t  open2               ;//12
    int16_t  open3               ;//14
    int16_t  open4               ;//16
    float    open5               ;//20
    float    open6               ;//24
    uint8_t  ck                  ;//25
} sys = {25,0};

struct struct_measure        
{
    uint8_t  length              ;//1
    uint8_t  ID                  ;//2
    uint8_t  flag1       : 1     ;//3.0
    uint8_t  flag2       : 1     ;//3.1
    uint8_t  flag3       : 1     ;//3.2
    uint8_t  flag4       : 1     ;//3.3
    uint8_t  flag5       : 1     ;//3.4
    uint8_t  flag6       : 1     ;//3.5
    uint8_t  flag7       : 1     ;//3.6
    uint8_t  flag8       : 1     ;//3.7
    uint8_t  flag9       : 1     ;//3.0
    uint8_t  flag0       : 1     ;//4.1
    uint8_t  flagA       : 1     ;//4.2
    uint8_t  flagB       : 1     ;//4.3
    uint8_t  flagC       : 1     ;//4.4
    uint8_t  flagD       : 1     ;//4.5
    uint8_t  flagE       : 1     ;//4.6
    uint8_t  flagF       : 1     ;//4.7 
    int16_t  rps                 ;//6   @rule: name=RPM; expr=rps*60; unit=1/min
    int16_t  thrust              ;//8   @rule: name=F_Thrust; expr=thrust/100; unit=N
    int16_t  torque              ;//10  @rule: name=M_Torque; expr=torque/1000; unit=Nm  
    uint16_t voltage             ;//12  @rule: name=Volt; expr=voltage/1000; unit=V
    uint16_t current             ;//14  @rule: name=Current; expr=current/1000; unit=V
    uint16_t power_in            ;//16  @rule: name=Power_In; expr=power_in/100; unit=W
    uint16_t power_out           ;//18  @rule: name=Power_Out; expr=power_out/100; unit=W
    uint16_t eta_full            ;//20  @rule: name=effectivity; expr=effectivity/10; unit=%
    int16_t  thrust_eff          ;//22  @rule: name=Thrust/W; expr=thrust_eff/100; unit=mN/W
    int16_t  pres_1              ;//24  @rule: name=Pressure; expr=pres_1/100; unit=mbar
    int16_t  pres_2              ;//26  @rule: name=Pressure; expr=pres_2/100; unit=mbar
    int16_t  v_prop              ;//28  @rule: name=Propeller_Windspeed; expr=v_prop/10; unit=m/s
    int16_t  v_tunnel            ;//30  @rule: name=Tunnel_Windspeed; expr=v_tunnel/10; unit=m/s
    int16_t  temp_1              ;//32  @rule: name=Temperatur_1; expr=temp_1/10; unit=degrees
    int16_t  temp_2              ;//34  @rule: name=Temperatur_2; expr=temp_2/10; unit=degrees
    int16_t  pwm_act             ;//36  @rule: name=PWM_Output; expr=pwm_act; unit=degrees           
    uint8_t  ck                  ;//37
} measure ={37, 1};

uint8_t* struct_id[]  = {
                           &sys.length,     //ID0
                           &measure.length //ID1
                        };  