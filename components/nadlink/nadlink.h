#pragma once

#include "esphome/core/component.h"
#include "esphome/components/button/button.h"

namespace esphome {
namespace nadlink {

class NADLink;

class NADLink : public Component {
 public:
  NADLink();
  void setup() override;

  float get_setup_priority() const override;
  
  void set_nadlink_pin(uint8_t pin);
  
  // Input selection methods
  void switch_to_tape_1();
  void switch_to_tape_2();
  void switch_to_tuner();
  void switch_to_aux();
  void switch_to_video();
  void switch_to_cd();
  void switch_to_disc();
  
  // Volume control methods
  void volume_up();
  void volume_down();
  
  // Mute toggle method
  void toggle_mute();
  
  // Power control method
  void toggle_standby();
  
 protected:
  uint8_t nadlink_pin_{13};
  
    // NADLink protocol methods
  void pulse(int microseconds);
  void flat(int microseconds);
  void command_preamble();
  void command_terminator();
  void send_repeat();
  void send_one_bit();
  void send_zero_bit();
  void send_byte(uint8_t data_byte);
  void send_byte_and_inverse(uint8_t data_byte);
  void send_command(uint8_t command, bool pause_before_and_after_command = true);
  void change_volume_to_default();
  void change_volume_to_zero();
  void toggle_speakers_a_b();
  void turn_on();
  void turn_off();
};

// Button classes for control
class NADLinkVolumeUpButton : public button::Button {
 public:
  explicit NADLinkVolumeUpButton(NADLink *parent);
 protected:
  void press_action() override;
  NADLink *parent_;
};

class NADLinkVolumeDownButton : public button::Button {
 public:
  explicit NADLinkVolumeDownButton(NADLink *parent);
 protected:
  void press_action() override;
  NADLink *parent_;
};

class NADLinkMuteToggleButton : public button::Button {
 public:
  explicit NADLinkMuteToggleButton(NADLink *parent);
 protected:
  void press_action() override;
  NADLink *parent_;
};

class NADLinkStandbyToggleButton : public button::Button {
 public:
  explicit NADLinkPowerToggleButton(NADLink *parent);
 protected:
  void press_action() override;
  NADLink *parent_;
};

}  // namespace nadlink
}  // namespace esphome
