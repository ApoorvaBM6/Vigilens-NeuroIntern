from pylsl import StreamInfo, StreamOutlet
import time

# Create a dummy LSL stream called "TestStream"
info = StreamInfo('Collection', 'Markers', 1, 100, 'float32', 'test123')
outlet = StreamOutlet(info)

print("Dummy LSL stream started. Press Ctrl+C to stop.")
while True:
    outlet.push_sample([0.0])
    time.sleep(0.01)  # 100 Hz