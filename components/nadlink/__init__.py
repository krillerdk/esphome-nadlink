import random
import string
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button, select
from esphome.const import (
    CONF_ID,
    CONF_PIN,
    CONF_INPUT,
)
from esphome import pins



#DEPENDENCIES = ["gpio"]
AUTO_LOAD = ["button", "select"]

# Create namespace for component
nadlink_ns = cg.esphome_ns.namespace("nadlink")
NADLink = nadlink_ns.class_("NADLink", cg.Component)

# Button classes
NADLinkVolumeUpButton = nadlink_ns.class_("NADLinkVolumeUpButton", button.Button)
NADLinkVolumeDownButton = nadlink_ns.class_("NADLinkVolumeDownButton", button.Button)
NADLinkMuteToggleButton = nadlink_ns.class_("NADLinkMuteToggleButton", button.Button)
NADLinkStandbyToggleButton = nadlink_ns.class_("NADLinkStandbyToggleButton", button.Button)
NADLinkPowerOnButton = nadlink_ns.class_("NADLinkPowerOnButton", button.Button)
NADLinkPowerOffButton = nadlink_ns.class_("NADLinkPowerOffButton", button.Button)

# Select class
NADLinkInputSelect = nadlink_ns.class_("NADLinkInputSelect", select.Select)

# Configuration constants
CONF_VOLUME_UP = "volume_up"
CONF_VOLUME_DOWN = "volume_down"
CONF_TOGGLE_MUTE = "toggle_mute"
CONF_TOGGLE_STANDBY = "toggle_standby"
CONF_POWER_ON = "power_on"
CONF_POWER_OFF = "power_off"

# Disable options
CONF_VOLUME_BUTTONS = "volume_buttons"
CONF_MUTE_BUTTON = "mute_button"
CONF_STANDBY_BUTTON = "standby_button" 
CONF_POWER_BUTTONS = "power_buttons"
CONF_INPUT_SELECT = "input_select"

# Default icons and names
DEFAULT_ICONS = {
    CONF_VOLUME_UP: "mdi:volume-plus",
    CONF_VOLUME_DOWN: "mdi:volume-minus",
    CONF_TOGGLE_MUTE: "mdi:volume-mute",
    CONF_TOGGLE_STANDBY: "mdi:power-sleep",
    CONF_POWER_ON: "mdi:power-on",
    CONF_POWER_OFF: "mdi:power-off",
    CONF_INPUT: "mdi:audio-input-rca",
}

DEFAULT_NAMES = {
    CONF_VOLUME_UP: "NAD Volume Up",
    CONF_VOLUME_DOWN: "NAD Volume Down",
    CONF_TOGGLE_MUTE: "NAD Mute Toggle",
    CONF_TOGGLE_STANDBY: "NAD Standby Toggle",
    CONF_POWER_ON: "NAD Power On",
    CONF_POWER_OFF: "NAD Power Off",
    CONF_INPUT: "NAD Input Source",
}

# Schema for the component
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(NADLink),
    cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
    
    # Component enable/disable flags (all enabled by default)
    cv.Optional(CONF_VOLUME_BUTTONS, default=True): cv.boolean,
    cv.Optional(CONF_MUTE_BUTTON, default=True): cv.boolean,
    cv.Optional(CONF_STANDBY_BUTTON, default=True): cv.boolean,
    cv.Optional(CONF_POWER_BUTTONS, default=True): cv.boolean,
    cv.Optional(CONF_INPUT_SELECT, default=True): cv.boolean,
    
    # Optional button customization schemas
    cv.Optional(CONF_VOLUME_UP): button.BUTTON_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkVolumeUpButton),
    }),
    cv.Optional(CONF_VOLUME_DOWN): button.BUTTON_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkVolumeDownButton),
    }),
    cv.Optional(CONF_TOGGLE_MUTE): button.BUTTON_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkMuteToggleButton),
    }),
    cv.Optional(CONF_TOGGLE_STANDBY): button.BUTTON_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkStandbyToggleButton),
    }),
    cv.Optional(CONF_POWER_ON): button.BUTTON_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkPowerOnButton),
    }),
    cv.Optional(CONF_POWER_OFF): button.BUTTON_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkPowerOffButton),
    }),
    
    # Optional input select customization schema
    cv.Optional(CONF_INPUT): select.SELECT_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(NADLinkInputSelect),
    }),
}).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    # Create the main component
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    # Configure the NADLink pin
    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_nadlink_pin(pin))
    
    # Generate a random string to append to our IDs to make them unique
    def generate_random_suffix():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # Volume buttons
    if config[CONF_VOLUME_BUTTONS]:
        # Volume Up button
        if CONF_VOLUME_UP in config:
            vol_up = cg.new_Pvariable(config[CONF_VOLUME_UP][CONF_ID], var)
            await button.register_button(vol_up, config[CONF_VOLUME_UP])
        else:
            # Create a unique ID string (not an ID object)
            vol_up_id_str = f"{config[CONF_ID].id}_volume_up_{generate_random_suffix()}"
            # Register this string directly with CORE.id
            vol_up_id = cg.id(vol_up_id_str)
            vol_up = cg.new_Pvariable(vol_up_id, var)
            cg.add(vol_up.set_name(DEFAULT_NAMES[CONF_VOLUME_UP]))
            cg.add(vol_up.set_icon(DEFAULT_ICONS[CONF_VOLUME_UP]))
            await button.register_button(vol_up, {})
        
        # Volume Down button
        if CONF_VOLUME_DOWN in config:
            vol_down = cg.new_Pvariable(config[CONF_VOLUME_DOWN][CONF_ID], var)
            await button.register_button(vol_down, config[CONF_VOLUME_DOWN])
        else:
            vol_down_id_str = f"{config[CONF_ID].id}_volume_down_{generate_random_suffix()}"
            vol_down_id = cg.id(vol_down_id_str)
            vol_down = cg.new_Pvariable(vol_down_id, var)
            cg.add(vol_down.set_name(DEFAULT_NAMES[CONF_VOLUME_DOWN]))
            cg.add(vol_down.set_icon(DEFAULT_ICONS[CONF_VOLUME_DOWN]))
            await button.register_button(vol_down, {})
    
    # Mute button
    if config[CONF_MUTE_BUTTON]:
        if CONF_TOGGLE_MUTE in config:
            mute = cg.new_Pvariable(config[CONF_TOGGLE_MUTE][CONF_ID], var)
            await button.register_button(mute, config[CONF_TOGGLE_MUTE])
        else:
            mute_id_str = f"{config[CONF_ID].id}_mute_toggle_{generate_random_suffix()}"
            mute_id = cg.id(mute_id_str)
            mute = cg.new_Pvariable(mute_id, var)
            cg.add(mute.set_name(DEFAULT_NAMES[CONF_TOGGLE_MUTE]))
            cg.add(mute.set_icon(DEFAULT_ICONS[CONF_TOGGLE_MUTE]))
            await button.register_button(mute, {})
    
    # Standby button
    if config[CONF_STANDBY_BUTTON]:
        if CONF_TOGGLE_STANDBY in config:
            standby = cg.new_Pvariable(config[CONF_TOGGLE_STANDBY][CONF_ID], var)
            await button.register_button(standby, config[CONF_TOGGLE_STANDBY])
        else:
            standby_id_str = f"{config[CONF_ID].id}_standby_toggle_{generate_random_suffix()}"
            standby_id = cg.id(standby_id_str)
            standby = cg.new_Pvariable(standby_id, var)
            cg.add(standby.set_name(DEFAULT_NAMES[CONF_TOGGLE_STANDBY]))
            cg.add(standby.set_icon(DEFAULT_ICONS[CONF_TOGGLE_STANDBY]))
            await button.register_button(standby, {})
    
    # Power buttons
    if config[CONF_POWER_BUTTONS]:
        # Power On button
        if CONF_POWER_ON in config:
            power_on = cg.new_Pvariable(config[CONF_POWER_ON][CONF_ID], var)
            await button.register_button(power_on, config[CONF_POWER_ON])
        else:
            power_on_id_str = f"{config[CONF_ID].id}_power_on_{generate_random_suffix()}"
            power_on_id = cg.id(power_on_id_str)
            power_on = cg.new_Pvariable(power_on_id, var)
            cg.add(power_on.set_name(DEFAULT_NAMES[CONF_POWER_ON]))
            cg.add(power_on.set_icon(DEFAULT_ICONS[CONF_POWER_ON]))
            await button.register_button(power_on, {})
        
        # Power Off button
        if CONF_POWER_OFF in config:
            power_off = cg.new_Pvariable(config[CONF_POWER_OFF][CONF_ID], var)
            await button.register_button(power_off, config[CONF_POWER_OFF])
        else:
            power_off_id_str = f"{config[CONF_ID].id}_power_off_{generate_random_suffix()}"
            power_off_id = cg.id(power_off_id_str)
            power_off = cg.new_Pvariable(power_off_id, var)
            cg.add(power_off.set_name(DEFAULT_NAMES[CONF_POWER_OFF]))
            cg.add(power_off.set_icon(DEFAULT_ICONS[CONF_POWER_OFF]))
            await button.register_button(power_off, {})
    
    # Input Select
    if config[CONF_INPUT_SELECT]:
        if CONF_INPUT in config:
            input_select = cg.new_Pvariable(config[CONF_INPUT][CONF_ID], var)
            await select.register_select(input_select, config[CONF_INPUT])
        else:
            input_id_str = f"{config[CONF_ID].id}_input_{generate_random_suffix()}"
            input_id = cg.id(input_id_str)
            input_select = cg.new_Pvariable(input_id, var)
            cg.add(input_select.set_name(DEFAULT_NAMES[CONF_INPUT]))
            cg.add(input_select.set_icon(DEFAULT_ICONS[CONF_INPUT]))
            await select.register_select(input_select, {})
