import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID
from esphome.components import button
from esphome import pins

nadlink_ns = cg.esphome_ns.namespace("nadlink")
NadLink = nadlink_ns.class_("NadLink", cg.Component)
VolumeUpButton = nadlink_ns.class_("VolumeUpButton", button.Button)
VolumeDownButton = nadlink_ns.class_("VolumeDownButton", button.Button)
StandbyButton = nadlink_ns.class_("StandbyButton", button.Button)

CONF_NADLINK_SIGNAL_PIN = "nadlink_signal_pin"
CONF_VOLUME_UP_BUTTON = "volume_up_button"
CONF_VOLUME_DOWN_BUTTON = "volume_down_button"
CONF_STANDBY_BUTTON = "standby_button"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(NadLink),
        cv.Required(CONF_NADLINK_SIGNAL_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_VOLUME_UP_BUTTON): button.BUTTON_SCHEMA,
        cv.Optional(CONF_VOLUME_DOWN_BUTTON): button.BUTTON_SCHEMA,
        cv.Optional(CONF_STANDBY_BUTTON): button.BUTTON_SCHEMA,
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    pin = await cg.gpio_pin_expression(config[CONF_NADLINK_SIGNAL_PIN])
    cg.add(var.set_nadlink_signal_pin(pin))

    if CONF_VOLUME_UP_BUTTON in config:
        btn = await button.new_button(config[CONF_VOLUME_UP_BUTTON])
        cg.add(VolumeUpButton(var).set_parent(btn))
        cg.add(var.add_subcomponent(btn))

    if CONF_VOLUME_DOWN_BUTTON in config:
        btn = await button.new_button(config[CONF_VOLUME_DOWN_BUTTON])
        cg.add(VolumeDownButton(var).set_parent(btn))
        cg.add(var.add_subcomponent(btn))

    if CONF_STANDBY_BUTTON in config:
        sw = await button.new_button(config[CONF_STANDBY_BUTTON])
        cg.add(StandbyButton(var).set_parent(sw))
        cg.add(var.add_subcomponent(sw))
