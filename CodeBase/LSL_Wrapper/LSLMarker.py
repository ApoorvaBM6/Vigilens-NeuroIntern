import keyboard
from pylsl import StreamInfo, StreamOutlet, local_clock
import time

class LSLMarkerPusher:
    def __init__(self, stream_name='Markers', stream_type='Collection'):
        self.info = StreamInfo(name=stream_name, type=stream_type, channel_count=1,
                               nominal_srate=0, channel_format='string',
                               source_id='marker_stream_001')
        self.outlet = StreamOutlet(self.info)

    def push_marker(self, marker):
        timestamp = local_clock()
        self.outlet.push_sample([marker], timestamp)
        print(f"[MARKER] {marker} @ {timestamp}")


if __name__ == "__main__":
    marker_pusher = LSLMarkerPusher()

    print("Press 'b' to send a blink marker. Press 'esc' to quit.")

    while True:
        if keyboard.is_pressed('b'):
            marker_pusher.push_marker("blink")
            time.sleep(0.3)  # prevent multiple triggers for one press
        elif keyboard.is_pressed('esc'):
            print("Exiting...")
            break