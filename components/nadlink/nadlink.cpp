#include "esphome.h"
#include "nadlink.h"

namespace esphome {
namespace nadlink {

static const char *const TAG = "nadlink";
    
NADLink::NADLink() {}

void NADLink::setup() {
    pin_->setup();
    pin_->pin_mode(esphome::gpio::FLAG_OUTPUT);
    pin_->digital_write(true);
}

void NADLink::dump_config() {
    ESP_LOGCONFIG(TAG, "nadlink:");
    LOG_PIN(" Output pin: ",this->pin_);
    ESP_LOGCONFIG(TAG,  "NAD address 1: %02hhX", nad_c_740_address_1);
    ESP_LOGCONFIG(TAG,  "NAD address 2: %02hhX", nad_c_740_address_2);
}
    
float NADLink::get_setup_priority() const {
    return setup_priority::HARDWARE;
}
    
void NADLink::set_nadlink_pin(GPIOPin *pin) {
    pin_ = pin;
    ESP_LOGD(TAG, "NADLink pin set to %d", pin_);
}

// Public methods for input selection
void NADLink::switch_to_tape_1() {
    ESP_LOGD(TAG, "Switching to Tape 1");
    send_command(switch_input_to_tape_1);
}

void NADLink::switch_to_tape_2() {
    ESP_LOGD(TAG, "Switching to Tape 2");
    send_command(switch_input_to_tape_2);
}
    
void NADLink::switch_to_tuner() {
    ESP_LOGD(TAG, "Switching to Tuner");
    send_command(switch_input_to_tuner);
}
    
void NADLink::switch_to_aux() {
    ESP_LOGD(TAG, "Switching to AUX");
    send_command(switch_input_to_aux);
}
    
void NADLink::switch_to_video() {
    ESP_LOGD(TAG, "Switching to Video");
    send_command(switch_input_to_video);
}

void NADLink::switch_to_cd() {
    ESP_LOGD(TAG, "Switching to CD");
    send_command(switch_input_to_cd);
}
    
void NADLink::switch_to_disc() {
    ESP_LOGD(TAG, "Switching to Disc");
    send_command(switch_input_to_disc);
}

// Volume control functions
void NADLink::volume_up() {
    ESP_LOGD(TAG, "Volume Up");
    send_command(increase_volume, false);
}

void NADLink::volume_down() {
    ESP_LOGD(TAG, "Volume Down");
    send_command(decrease_volume, false);
}
  
// Toggle mute function
void NADLink::toggle_mute() {
    ESP_LOGD(TAG, "Toggling Mute");
    send_command(toggle_mute_cmd);
}
  
// Power control functions
void NADLink::toggle_standby() {
    ESP_LOGD(TAG, "Toggling standby state");
    send_command(toggle_standby_cmd);
}

// NADLink protocol implementation
void NADLink::pulse(int microseconds) {
  // 0V (Logicalfalse)
  pin_->digital_write(false);
  delayMicroseconds(microseconds);
}

void NADLink::flat(int microseconds) {
    // +5.0V (+3.3V) (Logicaltrue)
    pin_->digital_write(true);
    delayMicroseconds(microseconds);
}

// Preamble
void NADLink::command_preamble() {
    ESP_LOGV(TAG, "Sending command preamble");
    pulse(9000);  // 9000 μs pulse
    flat(4500);   // 4500 μs flat
}

// Command Terminator
void NADLink::command_terminator() {
    ESP_LOGV(TAG, "Sending command terminator");
    pulse(560);   //   560 μs pulse
    flat(42020);  // 42020 μs flat
}

// Sends the repeat signal
void NADLink::send_repeat() {
    ESP_LOGV(TAG, "Sending repeat command");
    pulse(9000);   //  9000 μs pulse
    flat(2250);    //  2250 μs flat
    pulse(560);    //   560 μs pulse
    flat(98190);   // 98190 μs flat
}

void NADLink::send_one_bit() {
    pulse(560);   //  560 μs pulse
    flat(1690);   // 1690 μs flat
}

void NADLink::send_zero_bit() {
    pulse(560);   // 560 μs pulse
    flat(560);    //  560 μs flat
}

void NADLink::send_byte(uint8_t data_byte) {
    ESP_LOGVV(TAG, "Sending byte %02hhX", data_byte);
    for (uint8_t mask = 0x01; mask > 0; mask <<= 1) {  // iterate through a bit mask
        if (data_byte & mask) {
            send_one_bit();
        } else {
            send_zero_bit();
        }
    }
}

void NADLink::send_byte_and_inverse(uint8_t data_byte) {
    send_byte(data_byte);
    send_byte(~data_byte);
}

// Sends a complete command
void NADLink::send_command(uint8_t command, bool pause_before_and_after_command) {
    ESP_LOGV(TAG, "Sending commmand with byte value %02hhX", command);
    int pause_length_in_ms = 250;
    
    // Pause before command
    if (pause_before_and_after_command) {
        ESP_LOGV(TAG, "Pausing before commmand");
        delay(pause_length_in_ms);
    }

    // Send preamble signal
    command_preamble();

    ESP_LOGV(TAG, "Sending NAD address");
    // Send address part 1 and 2
    send_byte(nad_c_740_address_1);
    send_byte(nad_c_740_address_2);

    // Send command and inverted command
    send_byte_and_inverse(command);

    // Send command terminator signal
    command_terminator();

    // Pause after command
    if (pause_before_and_after_command) {
        ESP_LOGV(TAG, "Pausing after commmand");
        delay(pause_length_in_ms);
    }
}

void NADLink::change_volume_to_default() {
    // Returns the volume control to default level
    send_command(increase_volume, false);
    for (int i = 0; i < (113 * default_volume_level / 11); ++i) {
        send_repeat();
    }
}

void NADLink::change_volume_to_zero() {
    // Sets the volume to zero
    send_command(decrease_volume, false);
    for (int i = 0; i < (113 * default_volume_level / 11 + 5); ++i) {
        send_repeat();
    }
}

void NADLink::toggle_speakers_a_b() {
    // Toggles the speakers (assumes exactly one is on and one is off)
    send_command(toggle_speaker_a);
    send_command(toggle_speaker_b);
}

void NADLink::turn_on() {
    // Power up
    send_command(power_on);
    // Wait 4s for the amp to power up and turn on the inputs
    delay(4000);
    // Volume to default
    change_volume_to_default();
}

void NADLink::turn_off() {
    // Volume to zero
    change_volume_to_zero();
    // Power down
    send_command(power_off);
}

NADLinkVolumeUpButton::NADLinkVolumeUpButton(NADLink *parent) : parent_(parent) {}

void NADLinkVolumeUpButton::press_action() {
    parent_->volume_up();
}

NADLinkVolumeDownButton::NADLinkVolumeDownButton(NADLink *parent) : parent_(parent) {}

void NADLinkVolumeDownButton::press_action() {
    parent_->volume_down();
}

NADLinkMuteToggleButton::NADLinkMuteToggleButton(NADLink *parent) : parent_(parent) {}

void NADLinkMuteToggleButton::press_action() {
    parent_->toggle_mute();
}

NADLinkStandbyToggleButton::NADLinkStandbyToggleButton(NADLink *parent) : parent_(parent) {}

void NADLinkStandbyToggleButton::press_action() {
    parent_->toggle_standby();
}

NADLinkPowerOnButton::NADLinkPowerOnButton(NADLink *parent) : parent_(parent) {}

void NADLinkPowerOnButton::press_action() {
    parent_->turn_on();
}

NADLinkPowerOffButton::NADLinkPowerOffButton(NADLink *parent) : parent_(parent) {}

void NADLinkPowerOffButton::press_action() {
    parent_->turn_off();
}

NADLinkInputSelect::NADLinkInputSelect(NADLink *parent) : parent_(parent) {
    traits.set_options({"Unknown", "Tape 1", "Tape 2", "Tuner", "Aux", "Video", "CD", "Disc"});
}

/*void NADLinkInputSelect::setup() {
    this->publish_state("Unknown");
    }*/

void NADLinkInputSelect::control(const std::string &value) {
    if (value == "Unknown"){
        ESP_LOGI(TAG, "Dummy value \"Unknown\" provided. No action taken.");
    } else if (value == "Tape 1") {
        parent_->switch_to_tape_1();
    } else if (value == "Tape 2") {
        parent_->switch_to_tape_2();
    } else if (value == "Tuner") {
        parent_->switch_to_tuner();
    } else if (value == "Aux") {
        parent_->switch_to_aux();
    } else if (value == "Video") {
        parent_->switch_to_video();
    } else if (value == "CD") {
        parent_->switch_to_cd();
    } else if (value == "Disc") {
        parent_->switch_to_disc();
    }
    else {
        ESP_LOGE(TAG, "Invalid input selection: %s", value.c_str());
    }
    this->publish_state("Unknown");
}

}  // namespace nadlink
}  // namespace esphome
