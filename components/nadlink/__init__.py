import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_PIN
from esphome.components import button
from esphome import pins

nadlink_ns = cg.esphome_ns.namespace("nadlink")
NadLink = nadlink_ns.class_("NADLink", cg.Component)
VolumeUpButton = nadlink_ns.class_("NADLinkVolumeUpButton", button.Button)
VolumeDownButton = nadlink_ns.class_("NADLinkVolumeDownButton", button.Button)
StandbyButton = nadlink_ns.class_("NADLinkStandbyToggleButton", button.Button)
MuteButton = nadlink_ns.class_("NADLinkMuteToggleButton", button.Button)

CONF_NADLINK_ID = "nadlink_id"
#CONF_PIN = "nadlink_signal_pin"
CONF_VOLUME_UP_BUTTON = "volume_up_button"
CONF_VOLUME_DOWN_BUTTON = "volume_down_button"
CONF_STANDBY_BUTTON = "standby_button"
CONF_MUTE_BUTTON = "mute_button"

# Input selection constants
CONF_TAPE_1 = "tape_1"
CONF_TAPE_2 = "tape_2"
CONF_TUNER = "tuner"
CONF_AUX = "aux"
CONF_VIDEO = "video"
CONF_CD = "cd"
CONF_DISC = "disc"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(NadLink),
        cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_VOLUME_UP_BUTTON): button.BUTTON_SCHEMA.extend({
            cv.GenerateID(): cv.declare_id(VolumeUpButton)
        }),
        cv.Optional(CONF_VOLUME_DOWN_BUTTON): button.BUTTON_SCHEMA.extend({
            cv.GenerateID(): cv.declare_id(VolumeDownButton)
        }),
        cv.Optional(CONF_STANDBY_BUTTON): button.BUTTON_SCHEMA.extend({
            cv.GenerateID(): cv.declare_id(StandbyButton)
        }),
        cv.Optional(CONF_MUTE_BUTTON): button.BUTTON_SCHEMA.extend({
            cv.GenerateID(): cv.declare_id(MuteButton)
        }),
        cv.Optional(CONF_TAPE_1): button.BUTTON_SCHEMA,
        cv.Optional(CONF_TAPE_2): button.BUTTON_SCHEMA,
        cv.Optional(CONF_TUNER): button.BUTTON_SCHEMA,
        cv.Optional(CONF_AUX): button.BUTTON_SCHEMA,
        cv.Optional(CONF_VIDEO): button.BUTTON_SCHEMA,
        cv.Optional(CONF_CD): button.BUTTON_SCHEMA,
        cv.Optional(CONF_DISC): button.BUTTON_SCHEMA,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    # Configure the NADLink pin
    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_nadlink_pin(pin))
    
    # Register buttons
    if CONF_VOLUME_UP_BUTTON in config:
        conf = config[CONF_VOLUME_UP_BUTTON]
        volume_up = cg.new_Pvariable(conf[CONF_ID], var)
        await button.register_button(volume_up, conf)
        
    if CONF_VOLUME_DOWN_BUTTON in config:
        conf = config[CONF_VOLUME_DOWN_BUTTON]
        volume_down = cg.new_Pvariable(conf[CONF_ID], var)
        await button.register_button(volume_down, conf)
        
    if CONF_MUTE_BUTTON in config:
        conf = config[CONF_MUTE_BUTTON]
        mute_toggle = cg.new_Pvariable(conf[CONF_ID], var)
        await button.register_button(mute_toggle, conf)
        
    if CONF_STANDBY_BUTTON in config:
        conf = config[CONF_STANDBY_BUTTON]
        standby_toggle = cg.new_Pvariable(conf[CONF_ID], var)
        await button.register_button(standby_toggle, conf)
        
    # Create simple action buttons for input selection
    input_buttons = {
        CONF_TAPE_1: "switch_to_tape_1",
        CONF_TAPE_2: "switch_to_tape_2",
        CONF_TUNER: "switch_to_tuner",
        CONF_AUX: "switch_to_aux",
        CONF_VIDEO: "switch_to_video",
        CONF_CD: "switch_to_cd",
        CONF_DISC: "switch_to_disc",
    }
    
    for conf_key, method_name in input_buttons.items():
        if conf_key in config:
            conf = config[conf_key]
            action = cg.StructInitializer(
                button.ButtonPressTrigger,
                ("button", var),
            )
            await button.register_button(config[conf_key], var, method_name)
