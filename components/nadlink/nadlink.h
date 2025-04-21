#pragma once

#include "esphome/core/component.h"
#include "esphome/components/button/button.h"
#include "esphome/components/select/select.h"

namespace esphome {
namespace nadlink {

class NADLink : public Component {
public:
    NADLink();
    void setup() override;
    void dump_config() override;
    
    float get_setup_priority() const override;
  
    void set_nadlink_pin(GPIOPin *pin);

    void set_default_volume(int volume);
    void set_max_assumed_volume(int volume);

    void set_nad_address(uint8_t address1, uint8_t address2);
    
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

    // Allow exposing this as a service. Should probably be a wrapper class that takes of typecasting from int to char.
    void send_command(uint8_t command, bool pause_before_and_after_command = true);

    void turn_on();
    void turn_off();
    
protected:

    GPIOPin *pin_{nullptr};

    // NAD C 740 address
    uint8_t nad_address_1   = 0x87;  // B10000111
    uint8_t nad_address_2   = 0x7C;  // B01111100

    // NAD C740 commands
    static constexpr uint8_t power_on               = 0x25;
    static constexpr uint8_t power_off              = 0xC8;
    static constexpr uint8_t toggle_standby_cmd     = 0x80;

    static constexpr uint8_t toggle_speaker_a       = 0xCE;
    static constexpr uint8_t toggle_speaker_b       = 0xCF;

    static constexpr uint8_t switch_input_to_tape_1 = 0x8E;
    static constexpr uint8_t switch_input_to_tape_2 = 0x91;
    static constexpr uint8_t switch_input_to_tuner  = 0x82;
    static constexpr uint8_t switch_input_to_aux    = 0x9B;
    static constexpr uint8_t switch_input_to_video  = 0xC2;
    static constexpr uint8_t switch_input_to_cd     = 0x85;
    static constexpr uint8_t switch_input_to_disc   = 0x89;

    static constexpr uint8_t increase_volume        = 0x88;
    static constexpr uint8_t decrease_volume        = 0x8C;
    static constexpr uint8_t toggle_mute_cmd        = 0x94;

    // Default volume level (in steps) when turning on
    int default_volume_level = 6; 
    // Max volume (in steps) to assume when turning to zero.
    int max_volume = 20;
        
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
    void change_volume_to_default();
    void change_volume_to_zero();
    void toggle_speakers_a_b();
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
    explicit NADLinkStandbyToggleButton(NADLink *parent);
protected:
    void press_action() override;
    NADLink *parent_;
};

class NADLinkPowerOnButton : public button::Button {
public:
    explicit NADLinkPowerOnButton(NADLink *parent_);
protected:
    void press_action() override;
    NADLink *parent_;
};

class NADLinkPowerOffButton : public button::Button {
public:
    explicit NADLinkPowerOffButton(NADLink *parent_);
protected:
    void press_action() override;
    NADLink *parent_;
};

class NADLinkInputSelect : public select::Select {
public:
    explicit NADLinkInputSelect(NADLink *parent);
protected:
    NADLink *parent_;
    void control(const std::string &value) override;
};

}  // namespace nadlink
}  // namespace esphome
