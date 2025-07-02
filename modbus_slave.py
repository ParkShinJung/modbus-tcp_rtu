import yaml
from pymodbus.server.startstop import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder, Endian
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# config.yaml 로드
def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# 센서 데이터 초기값 (테스트용)
def get_initial_sensor_data():
    return {
        'Sensor 1 Value': 12.34,
        'Sensor 1 Error Code': 0,
        'Sensor 2 Value': 56.78,
        'Sensor 2 Error Code': 0,
    }

def build_registers(config, sensor_data):
    # address가 0-based로 직접 들어오므로 base_addr 필요 없음
    max_addr = 0
    for sensor in config['sensors']:
        end_addr = sensor['address'] + sensor['registers'] - 1
        if end_addr > max_addr:
            max_addr = end_addr
    # 전체 레지스터 배열 생성
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
    # Modbus 데이터 블록 생성
    block = ModbusSequentialDataBlock(0, registers)
    store = ModbusSlaveContext(hr=block)
    context = ModbusServerContext(slaves={config['slave_id']: store}, single=False)
    logging.info(f"Starting Modbus TCP Slave on port {config['port']} (slave_id={config['slave_id']})")
    StartTcpServer(context, address=("0.0.0.0", config['port']))

if __name__ == '__main__':
    main() 