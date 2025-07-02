import yaml
from pymodbus.server.startstop import StartSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder, Endian
import logging

logging.basicConfig(level=logging.INFO)

def load_config(path='config_rtu.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_initial_sensor_data():
    return {
        'Sensor 1 Value': 12.34,
        'Sensor 1 Error Code': 0,
        'Sensor 2 Value': 56.78,
        'Sensor 2 Error Code': 0,
    }

def build_registers(config, sensor_data):
    max_addr = 0
    for sensor in config['sensors']:
        end_addr = sensor['address'] + sensor['registers'] - 1
        if end_addr > max_addr:
            max_addr = end_addr
    registers = [0] * (max_addr + 1)
    for sensor in config['sensors']:
        name = sensor['name']
        addr = sensor['address']
        value = sensor_data.get(name, 0)
        builder = BinaryPayloadBuilder(byteorder=Endian.LITTLE, wordorder=Endian.LITTLE)
        if sensor['type'] == 'float':
            builder.add_32bit_float(float(value))
        elif sensor['type'] == 'dint':
            builder.add_32bit_int(int(value))
        payload = builder.to_registers()
        for i in range(sensor['registers']):
            registers[addr + i] = payload[i]
    print("[DEBUG] Registers after build:", registers)
    return registers

def main():
    config = load_config()
    sensor_data = get_initial_sensor_data()
    registers = build_registers(config, sensor_data)
    print("[DEBUG] Registers before server start:", registers)
    block = ModbusSequentialDataBlock(0, registers)
    store = ModbusSlaveContext(hr=block)
    context = ModbusServerContext(slaves={config['slave_id']: store}, single=False)
    logging.info(f"Starting Modbus RTU Slave on {config['serial_port']} (slave_id={config['slave_id']})")
    StartSerialServer(
        context,
        port=config['serial_port'],
        baudrate=config['baudrate'],
        parity=config['parity'],
        stopbits=config['stopbits'],
        bytesize=config['bytesize'],
        timeout=1
    )

if __name__ == '__main__':
    main() 