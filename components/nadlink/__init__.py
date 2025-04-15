import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID
from esphome import pins

nadlink_ns = cg.esphome_ns.namespace("nadlink")
NadLink = nadlink_ns.class_("NadLink", cg.Component)

CONF_NADLINK_SIGNAL_PIN = "nadlink_signal_pin"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(NadLink),
        cv.Required(CONF_NADLINK_SIGNAL_PIN): pins.gpio_output_pin_schema,
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    pin = await cg.gpio_pin_expression(config[CONF_NADLINK_SIGNAL_PIN])
    cg.add(var.set_nadlink_signal_pin(pin))
