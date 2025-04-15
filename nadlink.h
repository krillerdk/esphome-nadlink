#pragma once

#include "esphome/core/component.h"
#include "esphome/core/gpio/gpio.h"

#include "esphome/components/switch/switch.h"
#include "esphome/components/button/button.h"
#include "esphome/components/sensor/sensor.h"


namespace esphome {
namespace nadlink {

enum class NadCommand : uint8_t {
  POWER_TOGGLE = 0x0C,
  VOL_UP       = 0x10,
  VOL_DOWN     = 0x11,
  MUTE_TOGGLE  = 0x0D,
  INPUT_CD     = 0x45,
  INPUT_VIDEO1 = 0x46,
  INPUT_VIDEO2 = 0x47,
  INPUT_TUNER  = 0x44,
  INPUT_DISC   = 0x43,
  INPUT_TAPE1  = 0x41,
  INPUT_TAPE2  = 0x40,
};

    
class NadLink : public Component {
 public:
  void setup() override;
  void set_nadlink_signal_pin( *GPIOPin pin ) { nadlink_signal_pin = pin; }
  void volume_up_press();
  void volume_down_press();
  void set_standby(bool state);
  void send_command(uint8_t command);

  GPIOPin *nadlink_signal_pin;

 private:

  void send_start_bit();
  void send_bit(bool bit);
  void send_one();
  void send_zero();
  void send_stop_bit();
  void send_byte(uint8_t byte);

  bool power_is_on = false;

  const uint8_t nad_c_740_address_1 = 0x87;
  const uint8_t nad_c_740_address_2 = 0x7C;

};

class VolumeUpButton : public button::Button {
 public:
  VolumeUpButton(NadLink *parent) : parent_(parent) {}
  void press_action() { parent_->volume_up_press(); }

 protected:
  NadLink *parent_;
};

class VolumeDownButton : public button::Button {
 public:
  VolumeDownButton(NadLink *parent) : parent_(parent) {}
  void press_action() {
      parent_->volume_down_press();
  }

 protected:
  NadLink *parent_;
};

class StandbySwitch : public switch_::Switch {
 public:
  StandbySwitch(NadLink *parent) : parent_(parent) {}
  void write_state(bool state) {
    parent_->set_standby(state);
    //publish_state(state);
  }

 protected:
  NadLink *parent_;
};

}  // namespace nadlink
}  // namespace esphome
