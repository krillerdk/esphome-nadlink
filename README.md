# esphome-nadlink
An ESPHome external component that allows controlling NAD devices that have NAD Link ports. 
The idea is to be able to control NAD devices using home-assistant.


This project is based on the following projects:
* https://github.com/gregmatthewcrossley/nad_link
* https://github.com/bitraf/nadlink

The NAD Link protocol uses a 5V signal. Even though ESP32 devices only have 3.3V I/O pins it turns out that a 3.3V signal is enough for the NAD Link devices to accept the signals as valid. It does mean that you can't easily implement a NAD Link receiver on an ESP32, since the inputs are not 5V safe. 
For this (and other) reasons, this code only implements the NAD Link sender part. 

I'm using this with my NAD C740 Receiver, but it should work with just about anything as long as it supports NAD Link and uses the same remote codes.

## Wiring ##
To connect an ESP board to a NAD Link enabled NAD device, you must do the following:

* Wire the signal wire (the middle wire) of the RCA cable to an output pin on the ESP device.
* Wire the gnd wire (the outer wire) of the RCA cable to a ground pin on the ESP device.

You can either do this by cutting a cheap RCA cable and solder it on the ESP, or you can buy an RCA to terminal block adapter.

## Configuration ##

In order to use the component, you need to add the following to your ESPhome device yaml config:
```yaml
external_components:
  - source: github://krillerdk/esphome-nadlink@main
    components: [ nadlink ]

nadlink:
  id: nad_c740
  pin: GPIO16 (
```

By default it will populate buttons for toggling standby state, power on, power off, mute toggle, volume up, volume down, and an input select box that allows you to switch inputs between Tape1, Tape2, Tuner, Aux, Video, CD, and Disc. The values in the select drop-down are currently hardcoded to match the C740. I hope to be able to make the input list and corresponding actions configurable in the future. 

Most of the default buttons can be disabled if you don't want them. This example show how to do that:

```yaml
nadlink:
 id: <device_id>
 pin: GPIO16
 volume_buttons: false # Avoids creating volume up and volume down buttons
 mute_button: false # Avoids creating the mute button
 standby_button: false: Avoids creating the standby button
 power_buttons: false: Avoids creating the power on and power off buttons.
 input_select: false: Skips creation of the input select drop down.
```

If you want to be able to send custom remote commands that the module does not expose (yet), you can either build the buttons yourself using template buttons and lambdas, or you can expose the send_command function as a home-assistant service like this:
```yaml
api:
  actions:
  - action: send_command
    variables:
      command: int
      pause_before_and_after: bool
    then:
      - lambda: |-
          auto nad_component = static_cast<esphome::nadlink::NADLink*>(id(nad_c740));
          nad_component->send_command(static_cast<uint8_t>(command), pause_before_and_after);
```
This exposes the send_command function from the module as a service to home-assistant. This is also usefull for experimentation, or testing whether a certain remote code does what you expect it to. The remote codes needs to be specified as decimal, so power_on (0x25) needs to be specified as 37.

In general, you should be able to set `pause\_before\_and\_after` to false. It's mostly in an attempt to make all bells and whistles from the API available to home-assistant. If you set it to true, it will wait 250 ms before sending your command and 250ms after. It exists only in the API because NAD Link doesn't seem to handle too many commands (except for repeat commands) in rapid succession. 


### Virtual power state ###
Since the ESP device won't know the actual power or standby state of the receiver, it can't represent the correct state in home-assistant, and you can't for example use it in automations that depends on whether the device is turned on or not. To solve that problem I have a Shelly Plug in the outlet that powers the NAD receiver. The shelly plug has a power monitor, and based on that I can tell whether or not the receiver is turned on or is in standby. It turns out that at least the NAD C740 uses ~30W when turned on - no matter if it is playing or not, and ~2W when it's in standby. 
In Home Assistant i've created a threshold helper sensor that is true when the power consumption reported by the Shelly Plug is greater than 5W.
By importing the power consumption from Home Assistant to the ESP device config, i can build a template switch that represents the actual power state of the receiver, using a lambda expression to get the state and calls to the component to turn on and off. 

```yaml
binary_sensor:
  - platform: homeassistant
    id: virtual_power_state
    name: Smartplug power state
    entity_id: binary_sensor.nad_c740_virtual_power_state

switch:
  - platform: template
    name: power state
    id: power
    icon: "mdi:power-standby"
    turn_on_action:
      - lambda: |-
          auto nad_component = static_cast<esphome::nadlink::NADLink*>(id(nad_c740));
          nad_component->turn_on();
    turn_off_action:
      - lambda: |-
          auto nad_component = static_cast<esphome::nadlink::NADLink*>(id(nad_c740));
          nad_component->turn_off();
    restore_mode: DISABLED
    lambda: !lambda |-
      if (id(virtual_power_state).state) {
        return true;
      } else {
        return false;
      }

```    
I could of course have added a power-monitoring relay to the ESP device as well, and have everything done on the ESP, but I didn't want to have the ESP be in charge of the mains power to the recevier while tinkering, and the Shelly works well enough for my purpose. 

# Random thoughts #

The following is of random things that i wanted to mention but did manage to fit in above.

* I don't know the remote codes for operating the tuner, so they or any other codes are not currently supported. Only the ones in the original Arduino implementation has been added.
* Especially due to the added waits around some of the commands, but also because some the commands as they are specified takes a while to signal over the wire, you will get warnings about slow commands in the ESPHome logs. I'm not sure i can do anything about them.
