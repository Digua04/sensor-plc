# PLC to Sensor

Minimal SWaT process simulator for MV101 valve control testbed.

## Description

This simulator implements a simple Modbus TCP server that simulates:
- MV101 valve actuator
- Valve feedback status

Used for testing Micro820 PLC communication.

## Requirements
```bash
pip install pymodbus
```

## Usage
```bash
python MV101.py
```

## Modbus Register Map

| Address | Tag           | Type  | Description              |
|---------|---------------|-------|--------------------------|
| 100     | MV101_DI_ZSO  | Read  | Valve open status (0/1) |
| 200     | MV101_DO_Open | Write | Valve open command (0/1)|

## Configuration

- **IP**: 0.0.0.0 (listens on all interfaces)
- **Port**: 502
- **Protocol**: Modbus TCP

## Network Setup

- Simulator IP: 192.168.1.100
- PLC IP: 192.168.1.10
- Subnet: 255.255.255.0

## Testing

Use Modbus Poll or pymodbus client to test:
```python
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.1.100', port=502)
client.connect()
result = client.read_holding_registers(100, 1)
print(result.registers)
client.close()
```

## License

MIT License