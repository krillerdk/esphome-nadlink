import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button, select
from esphome.const import (
    CONF_ID,
    CONF_PIN,
    CONF_INPUT,
    CONF_ICON,
    CONF_NAME,
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

    # Helper function to create a component with default icons and names
    def create_default_component(comp_type, conf, parent_var, component_class, register_func):
        if comp_type in config:
            comp_conf = config[comp_type]
            comp_var = cg.new_Pvariable(comp_conf[CONF_ID], parent_var)
            return register_func(comp_var, comp_conf)
        else:
            # Auto-generate ID safely
            comp_var = cg.new_Pvariable(cg.generate_name(f"{config[CONF_ID].id}_{comp_type}"), parent_var)
            default_conf = {
                CONF_NAME: DEFAULT_NAMES.get(comp_type, f"NAD {comp_type.replace('_', ' ').title()}"),
                CONF_ICON: DEFAULT_ICONS.get(comp_type, "mdi:audio"),
            }
            return register_func(comp_var, default_conf)
    
    # Create and register volume buttons if enabled
    if config[CONF_VOLUME_BUTTONS]:
        # Volume Up button
        await create_default_component(
            CONF_VOLUME_UP, 
            config, 
            var, 
            NADLinkVolumeUpButton, 
            button.register_button
        )
        
        # Volume Down button
        await create_default_component(
            CONF_VOLUME_DOWN, 
            config, 
            var, 
            NADLinkVolumeDownButton, 
            button.register_button
        )

    # Toggle Mute button if enabled
    if config[CONF_MUTE_BUTTON]:
        await create_default_component(
            CONF_TOGGLE_MUTE, 
            config, 
            var, 
            NADLinkMuteToggleButton, 
            button.register_button
        )
    
    # Toggle Standby button if enabled
    if config[CONF_STANDBY_BUTTON]:
        await create_default_component(
            CONF_TOGGLE_STANDBY, 
            config, 
            var, 
            NADLinkStandbyToggleButton, 
            button.register_button
        )
    
    # Power buttons if enabled
    if config[CONF_POWER_BUTTONS]:
        # Power On button
        await create_default_component(
            CONF_POWER_ON, 
            config, 
            var, 
            NADLinkPowerOnButton, 
            button.register_button
        )
        
        # Power Off button
        await create_default_component(
            CONF_POWER_OFF, 
            config, 
            var, 
            NADLinkPowerOffButton, 
            button.register_button
        )
    
    # Input Select if enabled
    if config[CONF_INPUT_SELECT]:
        await create_default_component(
            CONF_INPUT, 
            config, 
            var, 
            NADLinkInputSelect, 
            select.register_select
        )
