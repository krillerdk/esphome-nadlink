#include "nadlink.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace nadlink {

 static const char* TAG = "nadlink"
    

    
void NadLink::setup() {
  nadlink_signal_pin->setup();
  //nadlink_signal_pin->pin_mode(OUTPUT);
  nadlink_signal_pin->digital_write(false);
}

void NadLink::volume_up_press() {
  ESP_LOGD(TAG, "Volume Up");
  send_command(NadCommand::VOL_UP);  // Volume up command
}

void NadLink::volume_down_press() {
  ESP_LOGD(TAG, "Volume Down");
  send_command(NadCommand::VOL_DOWN);  // Volume down command
}

void NadLink::standby_toggle() {
  ESP_LOGD(TAG, "Toggle standby");
  send_command(NadCommand::POWER_TOGGLE);  // Power toggle
}

void NadLink::send_command(uint8_t command) {
  send_start_bit();

  send_byte(nad_c_740_address_1);
  send_byte(nad_c_740_address_2);
  send_byte(command);
  send_byte(~command);

  send_stop_bit();

  ESP_LOGD(TAG, "Sent command 0x%02X", command);
}

void NadLink::send_start_bit() {
  nadlink_signal_pin->digital_write(true);
  delayMicroseconds(9000);
  nadlink_signal_pin->digital_write(false);
  delayMicroseconds(4500);
}

void NadLink::send_bit(bool bit) {
  if (bit)
    send_one();
  else
    send_zero();
}

void NadLink::send_one() {
  nadlink_signal_pin->digital_write(true);
  delayMicroseconds(560);
  nadlink_signal_pin->digital_write(false);
  delayMicroseconds(1690);
}

void NadLink::send_zero() {
  nadlink_signal_pin->digital_write(true);
  delayMicroseconds(560);
  nadlink_signal_pin->digital_write(false);
  delayMicroseconds(560);
}

void NadLink::send_byte(uint8_t byte) {
  for (int i = 0; i < 8; i++) {
    send_bit(byte & 0x01);
    byte >>= 1;
  }
}

void NadLink::send_stop_bit() {
  nadlink_signal_pin->digital_write(true);
  delayMicroseconds(560);
  nadlink_signal_pin->digital_write(false);
}

}  // namespace nadlink
}  // namespace esphome
