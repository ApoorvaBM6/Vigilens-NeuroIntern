import cv2
import time
import csv
import sys
from pylsl import StreamInfo, StreamOutlet, local_clock   # for high-resolution timestamps


'''def record_video_with_timestamps(
    camera_id=0,
    output_video="output.avi",
    output_timestamps="timestamps.csv",
    fps=30,
    duration=10,
    frame_size=None
):
    # Open camera
    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print("[ERROR] Could not open camera")
        return

    # Try to set FPS (not guaranteed)
    cap.set(cv2.CAP_PROP_FPS, fps)

    # Get frame size if not specified
    if frame_size is None:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)

    # Video writer (MJPG codec → AVI container)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    # Open CSV file for timestamps
    with open(output_timestamps, mode="w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["frame_index", "system_time", "lsl_time"])

        start_time = time.time()
        frame_index = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to grab frame")
                break

            # Write video frame
            writer.write(frame)

            # Log timestamps
            sys_time = time.time()
            lsl_time = local_clock()  # LSL high-res time
            csv_writer.writerow([frame_index, sys_time, lsl_time])

            frame_index += 1

            # Stop after duration seconds
            if sys_time - start_time >= duration:
                break

    # Release resources
    cap.release()
    writer.release()
    print(f"Video saved to {output_video}")
    print(f"Timestamps saved to {output_timestamps}")'''

def video_recording_lsl(camera_id=0, output_video="output.avi", fps=30, frame_size=None, duration=None):
    """Record video and push frame timestamps to LSL."""
    # Open camera
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("[ERROR] Could not open camera", flush=True)
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FPS, fps)

    if frame_size is None:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)

    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    # Create LSL outlet for video timestamps
    info = StreamInfo(name="Collection",
                      type="Video",
                      channel_count=1,
                      nominal_srate=0,  # irregular sampling
                      channel_format='int32',
                      source_id='video_stream_001')
    outlet = StreamOutlet(info)

    start_time = time.time()
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame", flush=True)
            break

        writer.write(frame)

        # Push frame index to LSL with high-resolution timestamp
        ts = local_clock()
        outlet.push_sample([frame_index], ts)

        frame_index += 1

        # Stop after duration if specified
        if duration and (time.time() - start_time) >= duration:
            break

    cap.release()
    writer.release()
    print(f"[INFO] Video saved to {output_video}", flush=True)


def validate_fps(obtained_fps, camera_id=0, num_frames=120):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("[ERROR] Could not open camera")
        return 0

    start = time.time()
    for _ in range(num_frames):
        ret, _ = cap.read()
        if not ret:
            break
    end = time.time()

    cap.release()
    elapsed = end - start
    fps = num_frames / elapsed if elapsed > 0 else 0
    if abs(fps - obtained_fps) > 0.2:
        print(f"[WARNING] Obtained FPS ({obtained_fps:.3f}) differs from camera FPS setting ({fps:.3f})")
        return False, fps
    return True, fps

def obtain_fps_opencv(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("[ERROR] Could not open camera")
        return 0

    # Try to get FPS from camera properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

if __name__ == "__main__":
    import sys
    camera_id = int(sys.argv[1])
    output_video = sys.argv[2]
    provided_fps = float(sys.argv[3])
    print(f"Camera ID: {camera_id}, Output Video: {output_video}, FPS: {provided_fps}", flush=True)
    if provided_fps == None or provided_fps <= 0:
        print("[INFO] No valid FPS provided, attempting to obtain from camera...", flush=True)
        obtained_fps = obtain_fps_opencv(camera_id=0)
        result, calculate_fps = validate_fps(obtained_fps, camera_id=0)
        if result : fps = obtained_fps
        else : fps = calculate_fps
    else:
        fps = provided_fps

    print(f"Using FPS: {fps:.3f}")

    video_recording_lsl(
        camera_id=0,
        output_video=output_video,
        fps=fps
    )
