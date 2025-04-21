import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button, select
from esphome.const import (
    CONF_ID,
    CONF_PIN,
    CONF_INPUT,
    CONF_NAME,
    CONF_ICON,
    CONF_OPTIONS,
    CONF_DISABLED_BY_DEFAULT,
)
from esphome import pins

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
CONF_ADDRESS1 = "address1"
CONF_ADDRESS2 = "address2"
CONF_MAX_VOLUME = "max_assumed_volume"
CONF_DEFAULT_VOLUME = "default_volume"

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

# Default IDs for auto-generated entities
CONF_VOLUME_UP_ID = "volume_up_id"
CONF_VOLUME_DOWN_ID = "volume_down_id"
CONF_TOGGLE_MUTE_ID = "toggle_mute_id"
CONF_TOGGLE_STANDBY_ID = "toggle_standby_id"
CONF_POWER_ON_ID = "power_on_id"
CONF_POWER_OFF_ID = "power_off_id"
CONF_INPUT_ID = "input_id"

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

DEFAULT_INPUTS = ["Unknown", "Tape 1", "Tape 2", "Tuner", "Aux", "Video", "CD", "Disc"]

DEFAULT_NAD_ADDREESS = [ 0x87, 0x7C ]

# Schema for the component
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(NADLink),
    cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
    cv.Optional(CONF_ADDRESS1): cv.hex_int,
    cv.Optional(CONF_ADDRESS2): cv.hex_int,
    cv.Optional(CONF_MAX_VOLUME): cv.int_,
    cv.Optional(CONF_DEFAULT_VOLUME): cv.int_,

    # Component enable/disable flags (all enabled by default)
    cv.Optional(CONF_VOLUME_BUTTONS, default=True): cv.boolean,
    cv.Optional(CONF_MUTE_BUTTON, default=True): cv.boolean,
    cv.Optional(CONF_STANDBY_BUTTON, default=True): cv.boolean,
    cv.Optional(CONF_POWER_BUTTONS, default=True): cv.boolean,
    cv.Optional(CONF_INPUT_SELECT, default=True): cv.boolean,
    
    # Auto-generated button IDs (can be referenced in YAML)
    cv.Optional(CONF_VOLUME_UP_ID): cv.declare_id(NADLinkVolumeUpButton),
    cv.Optional(CONF_VOLUME_DOWN_ID): cv.declare_id(NADLinkVolumeDownButton),
    cv.Optional(CONF_TOGGLE_MUTE_ID): cv.declare_id(NADLinkMuteToggleButton),
    cv.Optional(CONF_TOGGLE_STANDBY_ID): cv.declare_id(NADLinkStandbyToggleButton),
    cv.Optional(CONF_POWER_ON_ID): cv.declare_id(NADLinkPowerOnButton),
    cv.Optional(CONF_POWER_OFF_ID): cv.declare_id(NADLinkPowerOffButton),
    cv.Optional(CONF_INPUT_ID): cv.declare_id(NADLinkInputSelect),
    
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

    # Set the NAD protocol address if specified
    if CONF_ADDRESS1 and CONF_ADDRESS2 in config:
        await cg.set_nad_address(CONF_ADDRESS1, CONF_ADDRESS2)

    # Volume level defaults
    if CONF_MAX_VOLUME in config:
        await cg.set_max_assumed_volume(CONF_MAX_VOLUME)
    if CONF_DEFAULT_VOLUME in config:
        await cg.set_default_volume(CONF_DEFAULT_VOLUME)
        
    # Volume buttons
    if config[CONF_VOLUME_BUTTONS]:
        # Volume Up button
        if CONF_VOLUME_UP in config:
            vol_up = cg.new_Pvariable(config[CONF_VOLUME_UP][CONF_ID], var)
            await button.register_button(vol_up, config[CONF_VOLUME_UP])
        else:
            # Use either user-provided ID or generate a default one
            vol_up_id = config.get(CONF_VOLUME_UP_ID, None)
            if vol_up_id is None:
                vol_up_id = cv.declare_id(NADLinkVolumeUpButton)(f"{config[CONF_ID].id}_volume_up")
            vol_up = cg.new_Pvariable(vol_up_id, var)
            cg.add(vol_up.set_name(DEFAULT_NAMES[CONF_VOLUME_UP]))
            cg.add(vol_up.set_icon(DEFAULT_ICONS[CONF_VOLUME_UP]))
            await button.register_button(vol_up, {
                CONF_ID: vol_up_id,
                CONF_NAME: DEFAULT_NAMES[CONF_VOLUME_UP],
                CONF_ICON: DEFAULT_ICONS[CONF_VOLUME_UP],
                CONF_DISABLED_BY_DEFAULT: False
            })
        
        # Volume Down button
        if CONF_VOLUME_DOWN in config:
            vol_down = cg.new_Pvariable(config[CONF_VOLUME_DOWN][CONF_ID], var)
            await button.register_button(vol_down, config[CONF_VOLUME_DOWN])
        else:
            vol_down_id = config.get(CONF_VOLUME_DOWN_ID, None)
            if vol_down_id is None:
                vol_down_id = cv.declare_id(NADLinkVolumeDownButton)(f"{config[CONF_ID].id}_volume_down")
            vol_down = cg.new_Pvariable(vol_down_id, var)
            cg.add(vol_down.set_name(DEFAULT_NAMES[CONF_VOLUME_DOWN]))
            cg.add(vol_down.set_icon(DEFAULT_ICONS[CONF_VOLUME_DOWN]))
            await button.register_button(vol_down, {
                CONF_ID: vol_down_id,
                CONF_NAME: DEFAULT_NAMES[CONF_VOLUME_DOWN],
                CONF_ICON: DEFAULT_ICONS[CONF_VOLUME_DOWN],
                CONF_DISABLED_BY_DEFAULT: False
            })
    
    # Mute button
    if config[CONF_MUTE_BUTTON]:
        if CONF_TOGGLE_MUTE in config:
            mute = cg.new_Pvariable(config[CONF_TOGGLE_MUTE][CONF_ID], var)
            await button.register_button(mute, config[CONF_TOGGLE_MUTE])
        else:
            mute_id = config.get(CONF_TOGGLE_MUTE_ID, None)
            if mute_id is None:
                mute_id = cv.declare_id(NADLinkMuteToggleButton)(f"{config[CONF_ID].id}_mute_toggle")
            mute = cg.new_Pvariable(mute_id, var)
            cg.add(mute.set_name(DEFAULT_NAMES[CONF_TOGGLE_MUTE]))
            cg.add(mute.set_icon(DEFAULT_ICONS[CONF_TOGGLE_MUTE]))
            await button.register_button(mute, {
                CONF_ID: mute_id,
                CONF_NAME: DEFAULT_NAMES[CONF_TOGGLE_MUTE],
                CONF_DISABLED_BY_DEFAULT: False
            })
    
    # Standby button
    if config[CONF_STANDBY_BUTTON]:
        if CONF_TOGGLE_STANDBY in config:
            standby = cg.new_Pvariable(config[CONF_TOGGLE_STANDBY][CONF_ID], var)
            await button.register_button(standby, config[CONF_TOGGLE_STANDBY])
        else:
            standby_id = config.get(CONF_TOGGLE_STANDBY_ID, None)
            if standby_id is None:
                standby_id = cv.declare_id(NADLinkStandbyToggleButton)(f"{config[CONF_ID].id}_standby_toggle")
            standby = cg.new_Pvariable(standby_id, var)
            cg.add(standby.set_name(DEFAULT_NAMES[CONF_TOGGLE_STANDBY]))
            cg.add(standby.set_icon(DEFAULT_ICONS[CONF_TOGGLE_STANDBY]))
            await button.register_button(standby, {
                CONF_ID: standby_id,
                CONF_NAME: DEFAULT_NAMES[CONF_TOGGLE_STANDBY],
                CONF_ICON: DEFAULT_ICONS[CONF_TOGGLE_STANDBY],
                CONF_DISABLED_BY_DEFAULT: False
            })
    
    # Power buttons
    if config[CONF_POWER_BUTTONS]:
        # Power On button
        if CONF_POWER_ON in config:
            power_on = cg.new_Pvariable(config[CONF_POWER_ON][CONF_ID], var)
            await button.register_button(power_on, config[CONF_POWER_ON])
        else:
            power_on_id = config.get(CONF_POWER_ON_ID, None)
            if power_on_id is None:
                power_on_id = cv.declare_id(NADLinkPowerOnButton)(f"{config[CONF_ID].id}_power_on")
            power_on = cg.new_Pvariable(power_on_id, var)
            cg.add(power_on.set_name(DEFAULT_NAMES[CONF_POWER_ON]))
            cg.add(power_on.set_icon(DEFAULT_ICONS[CONF_POWER_ON]))
            await button.register_button(power_on, {
                CONF_ID: power_on_id,
                CONF_NAME: DEFAULT_NAMES[CONF_POWER_ON],
                CONF_ICON: DEFAULT_ICONS[CONF_POWER_ON],
                CONF_DISABLED_BY_DEFAULT: False
            })
        
        # Power Off button
        if CONF_POWER_OFF in config:
            power_off = cg.new_Pvariable(config[CONF_POWER_OFF][CONF_ID], var)
            await button.register_button(power_off, config[CONF_POWER_OFF])
        else:
            power_off_id = config.get(CONF_POWER_OFF_ID, None)
            if power_off_id is None:
                power_off_id = cv.declare_id(NADLinkPowerOffButton)(f"{config[CONF_ID].id}_power_off")
            power_off = cg.new_Pvariable(power_off_id, var)
            cg.add(power_off.set_name(DEFAULT_NAMES[CONF_POWER_OFF]))
            cg.add(power_off.set_icon(DEFAULT_ICONS[CONF_POWER_OFF]))
            await button.register_button(power_off, {
                CONF_ID: power_off_id,
                CONF_NAME: DEFAULT_NAMES[CONF_POWER_OFF],
                CONF_ICON: DEFAULT_ICONS[CONF_POWER_OFF],
                CONF_DISABLED_BY_DEFAULT: False
            })
    
    # Input Select
    if config[CONF_INPUT_SELECT]:
        if CONF_INPUT in config:
            input_select = cg.new_Pvariable(config[CONF_INPUT][CONF_ID], var)
            await select.register_select(
                input_select,
                config[CONF_INPUT],
                options=config[CONF_INPUT][CONF_OPTIONS]
            )
        else:
            input_id = config.get(CONF_INPUT_ID, None)
            if input_id is None:
                input_id = cv.declare_id(NADLinkInputSelect)(f"{config[CONF_ID].id}_input")
            input_select = cg.new_Pvariable(input_id, var)
            cg.add(input_select.set_name(DEFAULT_NAMES[CONF_INPUT]))
            cg.add(input_select.set_icon(DEFAULT_ICONS[CONF_INPUT]))
            cg.add(input_select.traits.set_options(DEFAULT_INPUTS))
            await select.register_select(
                input_select,
                {
                    CONF_ID:  input_id,
                    CONF_NAME: DEFAULT_NAMES[CONF_INPUT],
                    CONF_ICON: DEFAULT_ICONS[CONF_INPUT],
                    CONF_DISABLED_BY_DEFAULT: False
                },
                options=DEFAULT_INPUTS
            )
