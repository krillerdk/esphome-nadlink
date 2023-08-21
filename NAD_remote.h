/*
Controls the NAD C740 Receiver via NADLink

Based on this project: https://github.com/bitraf/nadlink/

NEC IR Protocal info here:
https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol
https://www.sbprojects.net/knowledge/ir/nec.php

*/

#include "esphome.h"

//class NADRemote {

const int nadlink_signal_pin = 27;

// global variables to track the input and speaker status
// bool power_is_on = false;
// bool power_is_on = true;
// (there is only a toggle command for speaker, so we have
// to keep track of their states)
// bool speaker_a_on = true;
// bool speaker_b_on = false;

// NAD C 740 address
// The (8 bit) address is transferred using pulse distance encoding
// with the least signficant bit going first over the wire.
// Afterwards, the bitwise negation is sent. Note: This is where
// NAD diverges slightly from the NEC spec. NAD does not send
// exactly the inverted address as the second unsigned char. Instead,
// typically **1 or 2 bits are not inverted**. This is not a problem,
// since it is included in the .ir files available at the NAD website.
byte nad_c_740_address_1 = 0x87; // B10000111
byte nad_c_740_address_2 = 0x7C; // B01111100    Note: not the exact inverse of the previous line! See above for explanation.

// NAD C740 commands
byte power_on = 0x25;
byte power_off = 0xC8;
byte power_toggle = 0x80;

byte toggle_speaker_a = 0xCE;
byte toggle_speaker_b = 0xCF;

byte switch_input_to_tape_1 = 0x8E;
byte switch_input_to_tape_2 = 0x91;
byte switch_input_to_tuner = 0x82;
byte switch_input_to_aux = 0x9B;
byte switch_input_to_video = 0xC2;
byte switch_input_to_cd = 0x85;
byte switch_input_to_disc = 0x89;

byte volume_increase = 0x88;
byte volume_decrease = 0x8C;
byte mute_toggle = 0x94;

// Default Volume
float default_volume_level = 1.1; // standard volume control position (on a scale of 0 to 11, 2 is more than enough)

// Funtion prototypes (where neccesary)
void send_command(byte command, bool pause_before_and_aftercommand = true);
static void send_repeat();


void volume_up(unsigned int steps = 1) {
  send_command(volume_increase, true);
  for (int i = 1; steps > i; i++) {
    send_repeat();
  }
}

void volume_down(unsigned int steps = 1) {
  send_command(volume_decrease, true);
  for (int i = 1; steps > i; i++) {
    send_repeat();
  }
}

// The NAD Link uses a slightly modified version of the NEC remote control protocol,
// where 0V represents pulse, and +5V represents flat.

// Pulse
void pulse(int microseconds){
  // 0V (Logical HIGH)
  digitalWrite(nadlink_signal_pin, LOW);
  delayMicroseconds(microseconds);
}

// Flat
void flat(unsigned long microseconds){
  // Pin 27 +3.3V (Logical LOW)
  digitalWrite(nadlink_signal_pin, HIGH);
  delayMicroseconds(microseconds);
}

// Preamble
void command_preamble(){
  pulse(9000); // 9000 μs pulse
  flat(4500);  // 4500 μs flat
}

// Command Terminator
void command_terminator(){
  pulse(560);  //   560 μs pulse
  flat(42020); // 42020 μs flat
}

// sends the repeat signal
static void send_repeat(){
  pulse(9000); //  9000 μs pulse
  flat(2250);  //  2250 μs flat
  pulse(560);  //   560 μs pulse
  flat(98190); // 98190 μs flat
}

void send_one_bit(){
  pulse(560); //  560 μs pulse
  flat(1690); // 1690 μs flat
}

void send_zero_bit(){
  pulse(560); // 560 μs pulse
  flat(560);  //  560 μs flat
}

void send_byte(byte data_byte){
  for (byte mask = B00000001; mask > 0; mask <<= 1)  { // iterate through a bit mask
    if (data_byte & mask) {
      send_one_bit();
    }
    else {
      send_zero_bit();
    }
  }
}

void send_byte_and_inverse(byte data_byte){
  send_byte(data_byte);
  send_byte(~data_byte);
}

// sends a complete command
// (with preample, two address bytess,
// two command bytes and the terminator)
void send_command(byte command, bool pause_before_and_after_command){
  int pause_length_in_ms = 250;
  // pause (running commands too close together seems to cause them to get ignored)
  if (pause_before_and_after_command){
    delayMicroseconds(1000 * pause_length_in_ms);
  }

  // send preamble signal
  command_preamble();

  // send address part 1 and 2
  send_byte(nad_c_740_address_1);
  send_byte(nad_c_740_address_2);

  // send command and inverted command
  send_byte_and_inverse(command);

  // send command terminator signal
  command_terminator();

  if (pause_before_and_after_command){
    delayMicroseconds(1000 * pause_length_in_ms);
  }
}

class NADPowerToggle : public  Component, public Switch {
  public:
    float get_setup_priority() const override {
      return esphome::setup_priority::IO;
    }
    // Initializing function (runs once on power-up)
    void setup() override {
      pinMode(nadlink_signal_pin, OUTPUT);
    }

    void write_state(bool state) override {
      send_command(power_toggle, false);
      publish_state(false);
    } 
};


class NADVolumeUp : public Component, public BinaryOutput {
  public:
    float get_setup_priority() const override {
      return esphome::setup_priority::IO;
    }

    void setup() override {
      pinMode(nadlink_signal_pin, OUTPUT);
    }

    void write_state(bool state) override {
      if (state) {
        volume_up(1);
      }
    }
};


class NADVolumeDown : public Component, public BinaryOutput {
  public:
    float get_setup_priority() const override {
      return esphome::setup_priority::IO;
    }

    void setup() override {
      pinMode(nadlink_signal_pin, OUTPUT);
    }

    void write_state(bool state) override {
      if (state){
	volume_down(1);
      }
    }
};


/*
  void toggle_mute()
  {
    send_command(mute_toggle, false);
  }


  void change_volume_to_default(){
    // sets the volume to the specified volume
    // on a scall from 0 to 11, 11 being the loudest
    // Assumes volume has been set to zero first.
    send_command(volume_increase, false);
    for (int i = 0; i < (113 * default_volume_level / 11); ++i)
    {
      // 113 repeats of the volume command
      // is just over a full rotation of the
      // volume dial on my NAD C740
      send_repeat();
    }
  }

  void change_volume_to_zero(){
    // (assumes volume is currently at 0)
    // returns the volume control
    // to zero (no matter what position it was in before)
    send_command(volume_decrease, false);
    //  for(int i = 0; i < (113*default_volume_level/11+5); ++i) {
    for (int i = 0; i < 113; ++i)
    {
      // 113 repeats of the volume command
      // is just over a full rotation of the
      // volume dial on my NAD C740
      send_repeat();
    }
  }

  void toggle_speakers_a_b()
  {
    // toggles the speakers
    // assumes exactly one is on and one is off
    send_command(toggle_speaker_a,true);
    send_command(toggle_speaker_b,true);
  }

  void switch_using(byte input_switch_command)
  {
    // mute
    send_command(mute_toggle, true);
    // switch speakers
    toggle_speakers_a_b();
    // switch to passed input
    send_command(input_switch_command,true);
    // unmute
    send_command(mute_toggle, true);
  }
  */
  void turn_on(){
    // power up
    send_command(power_on, false);
  }

  void switch_to_cd(){
    send_command(switch_input_to_cd, false);
  }

  void switch_to_video()
  {
    send_command(switch_input_to_video, false);
  }

  void switch_to_aux()
  {
    send_command(switch_input_to_aux,false);
  }

  void turn_off()
  {
    send_command(power_off,false);
  }

