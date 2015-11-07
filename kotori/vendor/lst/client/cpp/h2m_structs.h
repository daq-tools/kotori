// -*- coding: utf-8 -*-
// (c) 2014-2015 Hydro 2 Motion Developers, h2m@hm.edu

// target: Mbed
//#include "mbed.h"

// target: PC
#include "stdint.h"


// Program variable
//----------------------------------------------------------------------------------------------

typedef struct struct_program         // added 06.03.2014 C.L.
{
    /*
    struct_program()
    : length(13), ID(0)
    {}
    */
    uint8_t  length = 13;        //  1 Length of struct (byte)
    uint8_t  ID = 0;             //  2 Struct ID
    uint8_t  send_ser        :1; //w 3.0 FlagByte 1
    uint8_t  cfg_loaded      :1; //w 3.1
    uint8_t  clamped         :1; //w 3.2
    uint8_t  gps_input       :1; //w 3.3
    uint8_t  check_input     :1; //w 3.4
    uint8_t  gps_akt         :1; //w 3.5
    uint8_t  base_clock      :1; //w 3.6
    uint8_t  do_O2_IN        :1; //w 3.7
    uint8_t  do_O2_OUT       :1; //w 4.0
    uint8_t  do_O2_ALL       :1; //w 4.1
    uint8_t  do_S_ALL        :1; //w 4.2
    uint8_t  do_T_ALL        :1; //w 4.3
    uint8_t  do_C_ALL        :1; //w 4.4
    uint8_t  do_M_ALL        :1; //w 4.5
    char     gps_data          ; //w  5
    uint8_t  ser_sync          ; //w  6
    uint8_t  ser_input_pos     ; //w  7
    uint8_t  gps_sync          ; //w  8
    uint8_t  gps_payload_pos   ; //w  9
    uint8_t  send_internet     ; //w 10
    uint16_t xbee_reset_count  ; //w 12
    uint8_t  ck;                 //  13 checksum
} Tstruct_program;

// REQUEST
//----------------------------------------------------------------------------------------------

typedef struct struct_request
{
    /*
    struct_request()
    : length(9), ID(1)
    {}
    */
    uint8_t  length = 9;      //  1 Length of struct (byte)
    uint8_t  ID = 1;          //  2 Struct ID
    uint8_t akt         : 1;  //r 3.0
    uint8_t save_config : 1;  //r 3.1
    uint8_t read_config : 1;  //r 3.2
    uint8_t send_w      : 1;  //r 3.3
    uint8_t set_acc     : 1;  //r 3.4
    uint8_t internet_s  : 1;  //r 3.5
    uint8_t ser         : 1;  //r 3.6
    uint8_t s7          : 1;  //r 3.7
    uint8_t s8          : 1;  //r 4.0
    uint8_t s9          : 1;  //r 4.1
    uint8_t s10         : 1;  //r 4.2
    uint8_t s11         : 1;  //r 4.3
    uint8_t s12         : 1;  //r 4.4
    uint8_t s13         : 1;  //r 4.5
    uint8_t s14         : 1;  //r 4.6
    uint8_t s15         : 1;  //r 4.7
    uint32_t send_ID;         //r 8
    uint8_t  ck;              //  9 checksum
} Tstruct_request;

// CAP
//----------------------------------------------------------------------------------------------

typedef struct struct_cap_r
{
    struct_cap_r()
    : length(5), ID(2)
    {}
    uint8_t  length = 5;            //  1 Length of struct (byte)
    uint8_t  ID = 2;                //  2 Struct ID
    uint16_t voltage_act;       //r 4 Actual CAP Voltage
    uint8_t  ck;                //  5 checksum
} Tstruct_cap_r;

typedef struct struct_cap_w
{
    struct_cap_w()
    : length(15), ID(3)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    uint16_t voltage_low;       //w 4 Switch to full current
    uint16_t voltage_mid;       //w 6 Switch to medium current
    uint16_t voltage_max;       //w 8 Stopp loading
    uint16_t voltage_load;      //w 10 Start loading
    uint16_t voltage_d_max;     //w 12 Stop loading reduce Voltage (CAP down)
    uint16_t voltage_d_load;    //w 14 Start loading (CAP down)
    uint8_t  ck;                //  15 checksum
} Tstruct_cap_w;

// FC
//----------------------------------------------------------------------------------------------

typedef struct struct_fuelcell_r
{
    struct_fuelcell_r()
    : length(11), ID(4)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    uint16_t current_act;       //r 4
    uint16_t current_req;       //r 6
    uint16_t voltage_act;       //r 8
    uint16_t voltage_req;       //r 10
    uint8_t  ck;                //  11 checksum
} Tstruct_fuelcell_r;

typedef struct struct_fuelcell_w
{
    struct_fuelcell_w()
    : length(19), ID(5)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    uint16_t temp_max;          //w 4
    uint16_t voltage_max;       //w 6
    uint16_t voltage_low;       //w 8 minimum current
    uint16_t voltage_mid;       //w 10 medium current
    uint16_t voltage_high;      //w 12 high current
    uint16_t current_low;       //w 14 minimum current
    uint16_t current_mid;       //w 16 medium current
    uint16_t current_high;      //w 18 high current
    uint8_t  ck;                //  19 checksum
} Tstruct_fuelcell_w;

// H2O
//----------------------------------------------------------------------------------------------

typedef struct struct_h2o_r
{
    struct_h2o_r()
    : length(23), ID(6)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    short    fan_up_count;      //r 4 add
    short    fan_pwm;           //r 6
    uint16_t fan_pwm_act;       //r 8                       (not found!!!)
    short    pump_up_count;     //r 10 add
    short    pump_pwm;          //r 12
    uint16_t pump_pwm_act;      //r 14                      (not found!!!)
    short    temp_out;          //r 16
    uint16_t lambda;            //r 18
    short    lambda_delta;      //r 20
    short    lambda_delta_sum;  //r 22
    uint8_t  ck;                //  23 checksum
} Tstruct_h2o_r;

typedef struct struct_h2o_w
{
    struct_h2o_w()
    : length(29), ID(7)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    char     fan_override  : 1; //w 3.0
    char     pump_override : 1; //w 3.1
    char     FlagByte2;         //w 4
    uint16_t fan_over_pwm;      //w 6 name
    uint16_t fan_p;             //w 8
    uint16_t fan_i;             //w 10
    uint16_t fan_thr;           //w 12
    short    fan_up;            //w 14 add
    uint16_t pump_over_pwm;     //w 16 name
    uint16_t pump_min;          //w 18
    uint16_t pump_p;            //w 20
    uint16_t pump_i;            //w 22
    short    pump_up;           //w 24 add
    uint16_t lambda_min;        //w 26
    uint16_t lambda_max;        //w 28
    uint8_t  ck;                //  29 checksum
} Tstruct_h2o_w;

// MOSFET
//----------------------------------------------------------------------------------------------

typedef struct struct_mosfet_r
{
    struct_mosfet_r()
    : length(11), ID(8)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    short    current_delta;     //r 4      (not found!!!)
    uint16_t pwm;               //r 6
    uint16_t pwm_act;           //r 8      (not found!!!)
    short    temp_act;          //r 10
    uint8_t  ck;                //  11 checksum
} Tstruct_mosfet_r;

typedef struct struct_mosfet_w
{
    struct_mosfet_w()
    : length(16), ID(9)
    {}
    uint8_t  length;            //   1 Length of struct (byte)
    uint8_t  ID;                //   2 Struct ID
    uint16_t i;                 //w  4 Ki integral added
    uint16_t temp_max;          //w  6
    uint16_t load_cur_min;      //w  8
    uint16_t load_pwm_min;      //w 10
    uint16_t load_pwm_max;      //w 12
    uint16_t reload_v_min;      //w 14
    uint8_t  volt2amp;          //w 15
    uint8_t  ck;                //  16 checksum
} Tstruct_mosfet_w;

// O2
//----------------------------------------------------------------------------------------------

typedef struct struct_o2_r
{
    struct_o2_r()
    : length(43), ID(10)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    char     pump_on        : 1;//r 3.0
    char     pump_dual      : 1;//r 3.1
    char     flag_byte2;        //r 4
    char     pump_up_count1;    //r 5
    char     pump_up_count2;    //r 6
    uint16_t air_needed;        //r 8
    short    delta_t;           //r 10
    uint16_t pump_load;         //r 12
    uint16_t pump_load_act;     //r 14
    uint16_t pump_need;         //r 16
    uint16_t pump_min_req;      //r 18 name
    uint16_t pump_real_req;     //r 20
    uint16_t pump_pwm_1;        //r 22
    uint16_t pump_pwm_2;        //r 24
    short    rh_out_delta;      //r 26
    uint16_t rh_in;             //r 28
    uint16_t rh_out;            //r 30
    uint16_t temp_in;           //r 32
    uint16_t temp_out;          //r 34 added
    uint16_t temp_calc;         //r 36
    uint16_t water_extracted;   //r 38
    uint16_t water_in;          //r 40
    uint16_t water_out;         //r 42
    uint8_t  ck;                //  43 checksum
} Tstruct_o2_r;


typedef struct struct_o2_w
{
    struct_o2_w()
    : length(35), ID(11)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    bool     pump_override;     //w 3
    char     pump_up;           //w 4
    uint16_t lambda_min;        //w 6
    short    ml_to_perc_a;      //w 8
    short    ml_to_perc_bx1;    //w 10
    short    ml_to_perc_cx2;    //w 12
    short    ml_to_perc_dx3;    //w 14
    uint16_t pump_min;          //w 16
    uint16_t pump_over_load;    //w 18
    uint16_t pump_dual_on;      //w 20
    uint16_t pump_dual_off;     //w 22
    uint16_t rh_out_soll;       //w 24
    uint16_t rh_out_p;          //w 26
    uint16_t air_2_current;     //w 28
    uint16_t water_created;     //w 30
    uint16_t air_flow_min;      //w 32
    uint16_t air_flow_max;      //w 34
    uint8_t  ck;                //  35 checksum
} Tstruct_o2_w;


// SENSORS (formerly SWITCH)
//----------------------------------------------------------------------------------------------

typedef struct struct_sensors_r
{
    struct_sensors_r()
    : length(45), ID(12)
    {}
    uint8_t  length;        //   1 Length of struct (byte)
    uint8_t  ID;            //   2 Struct ID
    char capdown : 1;       //r  3.0
    char drive   : 1;       //r  3.1
    char master  : 1;       //r  3.2
    char safety  : 1;       //r  3.3
    char Flag_Byte_2;       //r  4
    uint16_t h2_analog;     //r  6
    uint16_t fc_voltage;    //r  8
    uint16_t cap_voltage;   //r 10
    uint16_t fc_current;    //r 12
    uint16_t cap_current;   //r 14
    uint16_t safety_V;      //r 16
    short    mosfet_temp;   //r 18
    short    h2o_temp_out;  //r 20
    uint16_t o2_temp_in;    //r 22
    uint16_t o2_temp_out;   //r 24
    uint16_t o2_rh_in;      //r 26
    uint16_t o2_rh_out;     //r 28
    uint16_t AUX1;          //r 30
    uint16_t AUX2;          //r 32
    short    acc_x_raw;     //r 34
    short    acc_y_raw;     //r 36
    short    acc_z_raw;     //r 38
    short    acc_x;         //r 40
    short    acc_y;         //r 42
    short    acc_z;         //r 44
    uint8_t  ck;            //  45 checksum
} Tstruct_sensors_r;

typedef struct struct_sensors_w
{
    struct_sensors_w()
    : length(65), ID(13)
    {}
    uint8_t  length;                //   1 Length of struct (byte)
    uint8_t  ID;                    //   2 Struct ID
    uint16_t h2o_temp_out_elow;     //w  4 Lower Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t h2o_temp_out_ehigh;    //w  6 Upper Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t h2o_temp_out_evalue;   //w  8 Error Temperature Value          added 19.02.2014 C.L.
    uint16_t fc_voltage_elow;       //w 10 Lower Voltage Sensor Limit   added 19.02.2014 C.L.
    uint16_t fc_voltage_ehigh;      //w 12 Upper Voltage Sensor Limit   added 19.02.2014 C.L.
    uint16_t fc_voltage_evalue;     //w 14 Error Voltage Value          added 19.02.2014 C.L.
    uint16_t fc_current_elow;       //w 16 Lower A Sensor Limit   added 19.02.2014 C.L.
    uint16_t fc_current_ehigh;      //w 18 Upper A Sensor Limit   added 19.02.2014 C.L.
    uint16_t fc_current_evalue;     //w 20 Error A Value          added 19.02.2014 C.L.
    uint16_t mosfet_temp_elow;      //w 22 Lower Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t mosfet_temp_ehigh;     //w 24 Upper Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t mosfet_temp_evalue;    //w 26 Error Temperature Value          added 19.02.2014 C.L.
    uint16_t o2_rh_in_evalue;       //w 28 Error RH Value          added 19.02.2014 C.L.
    uint16_t o2_rh_out_evalue;      //w 30 Error RH Value          added 19.02.2014 C.L.
    uint16_t o2_temp_in_elow;       //w 32 Lower Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t o2_temp_in_ehigh;      //w 34 Upper Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t o2_temp_in_evalue;     //w 36 Error Temperature Value          added 19.02.2014 C.L.
    uint16_t o2_temp_out_elow;      //w 38 Lower Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t o2_temp_out_ehigh;     //w 40 Upper Temperature Sensor Limit   added 19.02.2014 C.L.
    uint16_t o2_temp_out_evalue;    //w 42 Error Temperature Value          added 19.02.2014 C.L.
    uint16_t cap_voltage_elow;      //w 44 Lower Voltage Sensor Limit   added 19.02.2014 C.L.
    uint16_t cap_voltage_ehigh;     //w 46 Upper Voltage Sensor Limit   added 19.02.2014 C.L.
    uint16_t cap_voltage_evalue;    //w 48 Error Voltage Value          added 19.02.2014 C.L.
    uint16_t safety_vmin;           //w 50 Lower Voltage Limit Safty Accu
    uint16_t h2_ehigh;              //w 52 Max H2 Level
    uint16_t sys_cur_ehigh;         //w 54 Max Current to Engine
    int16_t acc_x_off;              //w 56 ACC_X_Offset
    int16_t acc_y_off;              //w 58 Acc_Y_Offset
    int16_t acc_z_off;              //w 60 Acc_Z_Offset
    uint16_t aux_1;                 //w 62 Aux 1 multi
    uint16_t aux_2;                 //w 64 Aux 2 multi
    uint8_t ck;                     //w 65 checksum
} Tstruct_sensors_w;

// SYSTEM
//----------------------------------------------------------------------------------------------

typedef struct struct_system_r
{
    struct_system_r()
    : length(15), ID(14)
    {}
    uint8_t  length;        //  1 Length of struct (byte)
    uint8_t  ID;            //  2 Struct ID
    char cap_d_load        : 1; //r 3.0 Flag Byte 1
    char cap_d_load_reset  : 1; //r 3.1
    char cap_load          : 1; //r 3.2
    char cap_load_reset    : 1; //r 3.3
    char cap_voltage_reset : 1; //r 3.4
    char fuelcell          : 1; //r 3.5
    char fc_overtemp       : 1; //r 3.6
    char fc_overvoltage    : 1; //r 3.7
    char load              : 1; //r 4.0 Flag Byte 2
    char load_act          : 1; //r 4.1
    char load_reset        : 1; //r 4.2
    char mos_overcur       : 1; //r 4.3
    char mos_overtemp      : 1; //r 4.4
    char run               : 1; //r 4.5
    char run_over          : 1; //r 4.6 added C.L.
    char temp              : 1; //r 4.7
    char reload_ready      : 1; //r 5.0 Flag Byte 3
    char purge;                 //r 6   Flag Byte 4
    uint16_t count;             //r 8
    uint16_t send_count;        //r 10
    uint16_t current_out;       //r 12
    uint16_t h2_purge         ; //w 14
    uint8_t  ck;                //  15 checksum
} Tstruct_system_r;

typedef struct struct_system_w
{
    struct_system_w()
    : length(23), ID(15)
    {}
    uint8_t  length;        //  1 Length of struct (byte)
    uint8_t  ID;            //  2 Struct ID
    bool     serial_on;     //  3 Send on X-Bee
    bool     ethernet_on;   //  4 Ethernet Schnittstelle
    bool     internet_on;   //  5 Send UDP Paket
    uint8_t  send_frq;      //  6
    uint16_t purge_auto;    //  8
    int32_t  gps_home_x;    // 12
    int32_t  gps_home_y;    // 16
    int32_t  gps_home_z;    // 20
    uint8_t  H2_purge;      // 21 Manual H2 Purge
    uint8_t  version;       // 22
    uint8_t  ck;            // 23 checksum
} Tstruct_system_w;


// ERROR
//----------------------------------------------------------------------------------------------

typedef struct struct_error_r
{
    struct_error_r()
    : length(7), ID(16)
    {}
    uint8_t  length;    //  1 Length of struct (byte)
    uint8_t  ID;        //  2 Struct ID
    char o2_in        : 1;  //r 3.0
    char o2_out       : 1;  //r 3.1
    char mosfet_temp  : 1;  //r 3.2
    char fc_voltage   : 1;  //r 3.3
    char cap_voltage  : 1;  //r 3.4
    char fc_current   : 1;  //r 3.5
    char h2o_temp_out : 1;  //r 3.6
    char safety_v     : 1;  //r 3.7
    char h2           : 1;  //r 4.0 !!!
    char sys_cur      : 1;  //r 4.1 !!!
    char t_1          : 1;  //r 4.2
    char t_2          : 1;  //r 4.3
    char t_3          : 1;  //r 4.4
    char t_4          : 1;  //r 4.5
    char t_5_0        : 1;  //r 4.6
    char t_5_1        : 1;  //r 4.7
    char t_6          : 1;  //r 5.0
    char t_7          : 1;  //r 5.1
    char t_8          : 1;  //r 5.2
    char o_1          : 1;  //r 5.3
    char o_2          : 1;  //r 5.4
    char o_3          : 1;  //r 5.5
    char o_4          : 1;  //r 5.6
    char o_5          : 1;  //r 5.7
    char o_6          : 1;  //r 6.0
    char o_7          : 1;  //r 6.1
    uint8_t  ck;            //  7 checksum
} Tstruct_error_r;

// GPS
//----------------------------------------------------------------------------------------------

typedef struct struct_gps_r         // added 06.03.2014 C.L.
{
    struct_gps_r()
    : length(19), ID(18)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    uint8_t  akt;               //r 3
    uint8_t  sats_used;         //r 4
     int32_t position_x;        //r 8
     int32_t position_y;        //r 12
     int32_t position_z;        //r 16
    uint16_t v_rms;             //r 18 typ change
     uint8_t ck;                //  19 checksum
} Tstruct_gps_r;


typedef struct struct_gps_w         // added 06.03.2014 C.L.
{
    struct_gps_w()
    : length(63), ID(19),Header1(0xB5),Header2(0x62),
      ID_1(0x01), ID_2(0x06), gps_length(0x34), fill(0x00)
    {}
    uint8_t  length;            //  1 Length of struct (byte)
    uint8_t  ID;                //  2 Struct ID
    uint8_t  Header1;           //  3
    uint8_t  Header2;           //  4
    uint8_t  ID_1;              //  5
    uint8_t  ID_2;              //  6
    uint8_t  gps_length;        //  7
    uint8_t  fill;              //  8
    uint32_t TOW;               //r 12
    int32_t  fTOW;              //r 16
    int16_t  week;              //r 18
    uint8_t  fix;               //r 19
    uint8_t  flags;             //r 20
     int32_t position_x;        //r 24
     int32_t position_y;        //r 28
     int32_t position_z;        //r 32
    uint32_t position_accuracy; //r 36
     int32_t velocity_x;        //r 40
     int32_t velocity_y;        //r 44
     int32_t velocity_z;        //r 48
    uint32_t velocity_accuracy; //r 52
    uint16_t pdop;              //r 54
    uint8_t  resl;              //r 55
    uint8_t  numSV;             //r 56
    uint32_t res2;              //r 60
    uint8_t  gps_cs_1;          //r 61
    uint8_t  gps_cs_2;          //r 62
    uint8_t  ck;                //  63 checksum
} Tstruct_gps_w;





// Compress Bools http://www.tutorialspoint.com/cprogramming/c_bit_fields.htm done in struct error


