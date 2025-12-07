# minimal_simulator.py
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import threading
import time

class MinimalSimulator:
    def __init__(self):
        self.store = ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, [0]*1000)
        )
        self.context = ModbusServerContext(slaves=self.store, single=True)
        
        # Pysichal states
        self.mv101_do_open = 0    # PLC writes command (address 200)
        self.mv101_di_zso = 0     # PLC reads status (address 100)
        
        print("=" * 60)
        print("Minimal SWaT Simulator - MV101 Only")
        print("=" * 60)
        print("Modbus Server: 0.0.0.0:502")
        print("\nRegister Mapping:")
        print("  Address 100: MV101_DI_ZSO (PLC reads valve status)")
        print("  Address 200: MV101_DO_Open (PLC writes valve command)")
        print("=" * 60)
    
    def actuator_feedback(self):
        """
        Actuator feedback simulation logic.
        """
        self.mv101_di_zso = self.mv101_do_open
    
    def simulation_loop(self):
        """Main simulation loop running in a separate thread."""
        iteration = 0
        while True:
            # 1. Read command from address 200 (written by PLC)
            try:
                self.mv101_do_open = self.store.getValues(3, 200, count=1)[0]
            except Exception as e:
                print(f"Error reading register 200: {e}")
            
            # 2. Actuator feedback logic
            self.actuator_feedback()
            
            # 3. Write status to address 100 (read by PLC)
            try:
                self.store.setValues(3, 100, [self.mv101_di_zso])
            except Exception as e:
                print(f"Error writing register 100: {e}")
            
            # 4. Logging every 2 seconds
            if iteration % 2 == 0:  # print every 2 seconds
                status = "OPEN" if self.mv101_di_zso == 1 else "CLOSED"
                command = "OPEN" if self.mv101_do_open == 1 else "CLOSE"
                print(f"[{iteration:04d}s] Command(R200)={command:5s} → Status(R100)={status:6s}")
            
            iteration += 1
            time.sleep(1)  # 1 second cycle time
    
    def run(self):
        # Start the simulation loop
        sim_thread = threading.Thread(target=self.simulation_loop, daemon=True)
        sim_thread.start()
        
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'SWaT Simulator'
        identity.ProductCode = 'SIM-MV101'
        identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
        identity.ProductName = 'Minimal Process Simulator'
        identity.ModelName = 'MV101 Testbed'
        identity.MajorMinorRevision = '1.0.0'
        
        # Start Modbus TCP server (blocking call)
        print("\n[INFO] Starting Modbus TCP Server...")
        print("[INFO] Press Ctrl+C to stop\n")
        try:
            StartTcpServer(
                self.context, 
                identity=identity,
                address=("0.0.0.0", 502)
            )
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped by user")

if __name__ == "__main__":
    simulator = MinimalSimulator()
    simulator.run()