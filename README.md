# Modbus TCP Slave (RTU 시뮬레이션)

이 프로젝트는 Python으로 구현된 Modbus TCP 슬레이브(서버)입니다. RTU(RS-485) 환경을 시뮬레이션하며, ModbusPal 등으로 테스트할 수 있습니다.

## 주요 기능
- Modbus TCP Slave 역할 (slave_id=1, port=502)
- 32bit float/dint 데이터 Little Endian(하위 워드 우선) 지원
- config.yaml 기반 센서 맵 구성

## 데이터 맵
| 항목                 | 주소 (1-based) | 데이터 타입                | 레지스터 개수 | 비고                        |
|----------------------|----------------|---------------------------|---------------|-----------------------------|
| Sensor 1 Value      | 40001 - 40002  | 32bit Float               | 2             | Little Endian (하위 워드 우선) |
| Sensor 1 Error Code | 40003 - 40004  | 32bit Signed Int (DINT)   | 2             | Little Endian (하위 워드 우선) |
| Sensor 2 Value      | 40005 - 40006  | 32bit Float               | 2             | Little Endian (하위 워드 우선) |
| Sensor 2 Error Code | 40007 - 40008  | 32bit Signed Int (DINT)   | 2             | Little Endian (하위 워드 우선) |

## 설치 및 실행
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python modbus_slave.py
```

## config.yaml 예시
```yaml
slave_id: 1
port: 1502
sensors:
  - name: Sensor 1 Value
    address: 40001
    type: float
    registers: 2
    comment: Little Endian (하위 워드 우선)
  - name: Sensor 1 Error Code
    address: 40003
    type: dint
    registers: 2
    comment: Little Endian (하위 워드 우선)
  - name: Sensor 2 Value
    address: 40005
    type: float
    registers: 2
    comment: Little Endian (하위 워드 우선)
  - name: Sensor 2 Error Code
    address: 40007
    type: dint
    registers: 2
    comment: Little Endian (하위 워드 우선)
```

## ModbusPal 테스트 방법
1. ModbusPal에서 TCP 마스터로 연결 (IP: 서버 IP, Port: 1502)
2. 슬레이브 ID: 1
3. Holding Register 40001~40008 읽기
4. 값이 정상적으로 표시되는지 확인

---
## 실행 방법
```ssh
source venv/bin/activate

python modbus_slave.py 
        or 
python modbus_slave_rtu.py

```
