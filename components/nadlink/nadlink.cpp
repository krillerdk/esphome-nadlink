#include "esphome.h"
#include "nadlink.h"

namespace esphome {
namespace nadlink {

class NADLink : public Component {
 public:
  NADLink() {}

  void setup() override {
    // Configure the NADLink output pin
    pinMode(nadlink_pin_, FLAG_OUTPUT);
    digitalWrite(nadlink_pin_, HIGH);    
  }

  float get_setup_priority() const override {
      return setup_priority::HARDWARE;
  }
    
  void set_nadlink_pin(uint8_t pin) {
      nadlink_pin_ = pin;
      ESP_LOGD(TAG, "NADLink pin set to %d", nadlink_pin_);
  }

  // Public methods for input selection
  void switch_to_tape_1() {
      ESP_LOGD(TAG, "Switching to Tape 1");
      send_command(switch_input_to_tape_1);
  }

  void switch_to_tape_2() {
      ESP_LOGD(TAG, "Switching to Tape 2");
      send_command(switch_input_to_tape_2);
  }
  void switch_to_tuner() {
      ESP_LOGD(TAG, "Switching to Tuner");
      send_command(switch_input_to_tuner);
  }
    
  void switch_to_aux() {
      ESP_LOGD(TAG, "Switching to AUX");
      send_command(switch_input_to_aux);
  }
    
  void switch_to_video() {
      ESP_LOGD(TAG, "Switching to Video");
      send_command(switch_input_to_video);
  }
  void switch_to_cd() {
      ESP_LOGD(TAG, "Switching to CD");
      send_command(switch_input_to_cd);
  }
  void switch_to_disc() {
      ESP_LOGD(TAG, "Switching to Disc");
      send_command(switch_input_to_disc);
  }

  // Volume control functions
  void volume_up() {
      ESP_LOGD(TAG, "Volume Up");
      send_command(increase_volume, false);
  }

  void volume_down() {
      ESP_LOGD(TAG, "Volume Down");
      send_command(decrease_volume, false);
  }
  
  // Toggle mute function
  void toggle_mute() {
      ESP_LOGD(TAG, "Toggling Mute");
      send_command(toggle_mute);
  }
  
  // Power control functions
  void toggle_standby() {
      ESP_LOGD(TAG, "Toggling standby state");
      send_command(toggle_standby);
  }

 protected:
  uint8_t nadlink_pin_{13};  // Default NADLink signal pin
  bool power_is_on_{false};

  // NAD C 740 address
  static constexpr uint8_t nad_c_740_address_1 = 0x87;  // B10000111
  static constexpr uint8_t nad_c_740_address_2 = 0x7C;  // B01111100

  // NAD C740 commands
  static constexpr uint8_t power_on = 0x25;
  static constexpr uint8_t power_off = 0xC8;
  static constexpr uint8_t power_toggle = 0x80;

  static constexpr uint8_t toggle_speaker_a = 0xCE;
  static constexpr uint8_t toggle_speaker_b = 0xCF;

  static constexpr uint8_t switch_input_to_tape_1 = 0x8E;
  static constexpr uint8_t switch_input_to_tape_2 = 0x91;
  static constexpr uint8_t switch_input_to_tuner = 0x82;
  static constexpr uint8_t switch_input_to_aux = 0x9B;
  static constexpr uint8_t switch_input_to_video = 0xC2;
  static constexpr uint8_t switch_input_to_cd = 0x85;
  static constexpr uint8_t switch_input_to_disc = 0x89;

  static constexpr uint8_t increase_volume = 0x88;
  static constexpr uint8_t decrease_volume = 0x8C;
  static constexpr uint8_t toggle_mute = 0x94;

  // Default volume level
  static constexpr float default_volume_level = 1.1;

  // NADLink protocol implementation
  void pulse(int microseconds) {
    // 0V (Logical LOW)
    digitalWrite(nadlink_pin_, LOW);
    delayMicroseconds(microseconds);
  }

  void flat(int microseconds) {
    // +3.3V (Logical HIGH)
    digitalWrite(nadlink_pin_, HIGH);
    delayMicroseconds(microseconds);
  }

  // Preamble
  void command_preamble() {
    pulse(9000);  // 9000 μs pulse
    flat(4500);   // 4500 μs flat
  }

  // Command Terminator
  void command_terminator() {
    pulse(560);   //   560 μs pulse
    flat(42020);  // 42020 μs flat
  }

  // Sends the repeat signal
  void send_repeat() {
    pulse(9000);   //  9000 μs pulse
    flat(2250);    //  2250 μs flat
    pulse(560);    //   560 μs pulse
    flat(98190);   // 98190 μs flat
  }

  void send_one_bit() {
    pulse(560);   //  560 μs pulse
    flat(1690);   // 1690 μs flat
  }

  void send_zero_bit() {
    pulse(560);   // 560 μs pulse
    flat(560);    //  560 μs flat
  }

  void send_byte(uint8_t data_byte) {
    for (uint8_t mask = 0x01; mask > 0; mask <<= 1) {  // iterate through a bit mask
      if (data_byte & mask) {
        send_one_bit();
      } else {
        send_zero_bit();
      }
    }
  }

  void send_byte_and_inverse(uint8_t data_byte) {
    send_byte(data_byte);
    send_byte(~data_byte);
  }

  // Sends a complete command
  void send_command(uint8_t command, bool pause_before_and_after_command = true) {
    int pause_length_in_ms = 250;

    // Pause before command
    if (pause_before_and_after_command) {
      delay(pause_length_in_ms);
    }

    // Send preamble signal
    command_preamble();

    // Send address part 1 and 2
    send_byte(nad_c_740_address_1);
    send_byte(nad_c_740_address_2);

    // Send command and inverted command
    send_byte_and_inverse(command);

    // Send command terminator signal
    command_terminator();

    // Pause after command
    if (pause_before_and_after_command) {
      delay(pause_length_in_ms);
    }
  }

  void change_volume_to_default() {
    // Returns the volume control to default level
    send_command(increase_volume, false);
    for (int i = 0; i < (113 * default_volume_level / 11); ++i) {
      send_repeat();
    }
  }

  void change_volume_to_zero() {
    // Sets the volume to zero
    send_command(decrease_volume, false);
    for (int i = 0; i < (113 * default_volume_level / 11 + 5); ++i) {
      send_repeat();
    }
  }

  void toggle_speakers_a_b() {
    // Toggles the speakers (assumes exactly one is on and one is off)
    send_command(toggle_speaker_a);
    send_command(toggle_speaker_b);
  }

  void turn_on() {
    // Power up
    send_command(power_on);
    // Wait 4s for the amp to power up and turn on the inputs
    delay(4000);
    // Volume to default
    change_volume_to_default();
  }

  void turn_off() {
    // Volume to zero
    change_volume_to_zero();
    // Power down
    send_command(power_off);
  }
};

// Volume Up Button
class NADLinkVolumeUpButton : public Button {
 public:
  explicit NADLinkVolumeUpButton(NADLink *parent) : parent_(parent) {}

 protected:
  void press_action() override { parent_->volume_up(); }
  NADLink *parent_;
};

// Volume Down Button
class NADLinkVolumeDownButton : public Button {
 public:
  explicit NADLinkVolumeDownButton(NADLink *parent) : parent_(parent) {}

 protected:
  void press_action() override { parent_->volume_down(); }
  NADLink *parent_;
};

// Mute Toggle Button
class NADLinkMuteToggleButton : public Button {
 public:
  explicit NADLinkMuteToggleButton(NADLink *parent) : parent_(parent) {}

 protected:
  void press_action() override { parent_->toggle_mute(); }
  NADLink *parent_;
};

// Power Toggle Button
class NADLinkStandbyToggleButton : public Button {
 public:
  explicit NADLinkStandbyToggleButton(NADLink *parent) : parent_(parent) {}

 protected:
  void press_action() override { parent_->toggle_standby(); }
  NADLink *parent_;
};

}  // namespace nadlink
}  // namespace esphome
