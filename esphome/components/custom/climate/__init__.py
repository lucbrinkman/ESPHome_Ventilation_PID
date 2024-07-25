import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate_LB
from esphome.const import CONF_ID, CONF_LAMBDA
from .. import custom_ns

CustomClimateConstructor = custom_ns.class_("CustomClimateConstructor")
CONF_CLIMATES = "climates"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(CustomClimateConstructor),
        cv.Required(CONF_LAMBDA): cv.returning_lambda,
        cv.Required(CONF_CLIMATES): cv.ensure_list(climate_LB.CLIMATE_SCHEMA),
    }
)


async def to_code(config):
    template_ = await cg.process_lambda(
        config[CONF_LAMBDA],
        [],
        return_type=cg.std_vector.template(climate_LB.Climate.operator("ptr")),
    )

    rhs = CustomClimateConstructor(template_)
    custom = cg.variable(config[CONF_ID], rhs)
    for i, conf in enumerate(config[CONF_CLIMATES]):
        rhs = custom.Pget_climate(i)
        await climate_LB.register_climate(rhs, conf)
