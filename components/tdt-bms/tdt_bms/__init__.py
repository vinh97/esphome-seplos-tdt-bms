import esphome.codegen as cg
from esphome.components import tdt_modbus
import esphome.config_validation as cv
from esphome.const import CONF_ID

AUTO_LOAD = ["tdt_modbus", "binary_sensor", "sensor", "text_sensor"]
CODEOWNERS = ["@syssi"]
MULTI_CONF = True

CONF_TDT_BMS_ID = "tdt_bms_id"
CONF_OVERRIDE_CELL_COUNT = "override_cell_count"

DEFAULT_PROTOCOL_VERSION = 0x20
DEFAULT_ADDRESS = 0x00

tdt_bms_ns = cg.esphome_ns.namespace("tdt_bms")
TDTBms = tdt_bms_ns.class_("TDTBms", cg.PollingComponent, tdt_modbus.TDTModbusDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(TDTBms),
            cv.Optional(CONF_OVERRIDE_CELL_COUNT, default=0): cv.int_range(
                min=0, max=16
            ),
        }
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(
        tdt_modbus.tdt_modbus_device_schema(DEFAULT_PROTOCOL_VERSION, DEFAULT_ADDRESS)
    )
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await tdt_modbus.register_tdt_modbus_device(var, config)

    cg.add(var.set_override_cell_count(config[CONF_OVERRIDE_CELL_COUNT]))
