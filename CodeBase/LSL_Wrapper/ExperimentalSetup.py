import sys
import time
import subprocess
from pylsl import StreamInfo, StreamOutlet, local_clock
from psychopy import event, visual, core
from videoRecorder import obtain_fps_opencv, validate_fps

   
'''def setup_labrecorder(recorder_path, output_filename, stream_filter=""):
    try:
        #cmd = [recorder_path, "--file", output_filename, "--streams", stream_filter]
        cmd = [recorder_path, '"'+output_filename+'"', '"'+stream_filter+'"']
        print("Launching:", " ".join(cmd))
        recorder = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = recorder.communicate(timeout=5)
        print("[LabRecorderCLI stdout]:", out.decode())
        print("[LabRecorderCLI stderr]:", err.decode())
        time.sleep(1)  # give it time to start
        if recorder.poll() is not None:  # process died
            out, err = recorder.communicate()
            print("[ERROR] LabRecorder failed:", err.decode())
            return None
        print(f"LabRecorder started, saving to {output_filename}")
        return recorder
    except Exception as e:
        print(f"[ERROR] Could not start LabRecorder: {e}")
        return None'''

def setup_labrecorder(recorder_path, output_filename, stream_filter=""):
    try:
        cmd = [
            recorder_path,
            output_filename,
            stream_filter
        ]
        print("Launching:", " ".join(cmd))
        recorder = subprocess.Popen(cmd)
        time.sleep(2)  # give it a moment to start
        print(f"LabRecorder started, saving to {output_filename}")
        return recorder
    except Exception as e:
        print(f"[ERROR] Could not start LabRecorder: {e}")
        return None
    
def start_video_subprocess(camera_id=0, output_video="output.avi", fps=30):
    """
    Start the video recording subprocess.

    This launches the same Python script in 'record' mode as a separate process,
    which handles video capture + LSL timestamps independently.
    """
    try: 
        cmd = [
            sys.executable,  # use same Python interpreter
            "videoRecorder.py", # script to run
            str(camera_id),
            output_video,
            str(fps)
        ]
        print("Starting video subprocess:", " ".join(cmd))
        proc = subprocess.Popen(cmd)
        time.sleep(2)  # give it a moment to start
        print(f"Video subprocess started, recording to {output_video}")
        return proc
    except Exception as e:
        print(f"[ERROR] Could not start LabRecorder: {e}")
        return None


def stop_video_subprocess(proc):
    """
    Stop the video recording subprocess cleanly.
    """
    proc.terminate()  # send SIGTERM / terminate signal
    proc.wait()       # wait for it to finish
    print("[INFO] Video subprocess stopped.")


def release_labrecorder(recorder):
    recorder.terminate()
    recorder.wait()
    print("LabRecorder stopped.")

def setup_lsl_marker_stream(stream_name='Collection', stream_type='Markers'):
    info = StreamInfo(name=stream_name, type=stream_type, channel_count=1,
                      nominal_srate=0, channel_format='string',
                      source_id='marker_stream_001')
    outlet = StreamOutlet(info)
    print("LSL Marker stream created.")
    return outlet


def pyscho_experiment(win, outlet):
    # ---------------------
    # Psychopy Window
    # ---------------------
    msg = visual.TextStim(win, text="Welcome!\n\nPart 1: Blink once every 5 seconds for 1 minute.\n\nPress any key to begin.", color="white")
    msg.draw()
    win.flip()
    event.waitKeys()
    print("Key pressed, starting the experiment.")

    duration = 15  # seconds
    blink_interval = 5
    n_blinks = duration // blink_interval
    start_time = time.time()
    next_blink = start_time + blink_interval

    print("Starting experiment loop...")
    idx = 0
    while idx < n_blinks:
            current_time = time.time()
            if current_time >= next_blink:
                idx += 1
                msg.text = f"Blink Now ({idx}/{n_blinks})"
                msg.draw()
                win.flip()
                core.wait(1)
                win.flip()

                # Push LSL marker
                timestamp = local_clock()
                outlet.push_sample([f"Blink_Index:{idx}"], timestamp)
                print(f"[BLINK MARKER INDEX]: {idx} @ {timestamp}")

                next_blink += blink_interval
                core.wait(1)  # short pause after blink cue

    msg.text = "Experiment complete!\nThank you!"
    msg.draw()
    win.flip()
    core.wait(3)



def main():
    print(">>> main() Experimental Program started", flush=True, file=sys.stderr)
    # File paths and parameters
    output_video_file = r"D:\France\ISAE\Internship\CodeBase\EEG_Blink\data\videoRecordingTest1.avi"
    recorder_path = r"D:\France\ISAE\Internship\Tools\LabRecorder-1.16.4-Win_amd64\LabRecorder\LabRecorderCLI.exe"
    #output_xfd_filename = r"D:\France\ISAE\Internship\CodeBase\Experimental_Setup\data\session_fp05_09_001.xdf"
    output_xfd_filename = r"D:\France\ISAE\Internship\CodeBase\EEG_Blink\data\lslRecordingTest1.xdf"
    stream_filter = str("name='Collection'")  # can be empty "" for all streams
    #stream_filter = str("name= 'TestStream'")

    # Setup Webcam
    video_proc = start_video_subprocess(camera_id=0, output_video=output_video_file)
    time.sleep(5)  # Give some time for the webcam to initialize

    # Setup LSL Marker Stream
    outlet = setup_lsl_marker_stream()
    time.sleep(10) # Give some time for stream discovery

    # Setup Psychopy window
    win = visual.Window(size= (1920, 1080), color='black')

    # Start LabRecorder via subprocess
    recorder = setup_labrecorder(recorder_path, output_xfd_filename, stream_filter)

    # Run the psychopy experiment
    pyscho_experiment(win, outlet)
    # Wait a bit to ensure all data is recorded
    time.sleep(10)
    print("Experiment finished, cleaning up...")
 
    # Cleanup
    stop_video_subprocess(video_proc)
    time.sleep(5)  # ensure subprocess has ended
    time.sleep(10)  # after experiment
    release_labrecorder(recorder)
    time.sleep(2) 
    win.close()


if __name__ == "__main__":
    main()

#LabRecorderCLI.exe "D:\France\ISAE\Internship\CodeBase\Experimental_Setup\data\test_recording2.xdf"  "name= 'TestStream'"
