from psychopy import visual, core, event, sound
from pylsl import StreamOutlet, local_clock
import time
import random

# -------------------------------
# LSL setup example (global)
# -------------------------------
def setup_lsl():
    from pylsl import StreamInfo, StreamOutlet
    info = StreamInfo('BlinkMarkers', 'Markers', 1, 0, 'string', 'myuid12345')
    outlet = StreamOutlet(info)
    return outlet

# -------------------------------
# Utility function to show message
# -------------------------------
def show_message(win, text, wait_key=True, duration=None):
    msg = visual.TextStim(win, text=text, color='white', height=0.08, alignText="center")
    msg.draw()
    win.flip()
    if wait_key:
        event.waitKeys()
    if duration:
        core.wait(duration)

# -------------------------------
# Task functions
# -------------------------------

# Eyes open/closed baseline
def eyes_baseline(win, duration=120, eyes='open', outlet=None):
    if outlet:
        outlet.push_sample([f"{eyes}_baseline_start"], local_clock())
    show_message(win, f"{eyes.capitalize()} baseline. Relax for {duration} seconds.", wait_key=False)
    start_time = time.time()
    while time.time() - start_time < duration:
        core.wait(0.1)  # just wait in small increments
    # Make a 440 Hz tone lasting 0.5 seconds
    beep = sound.Sound('A', secs=0.5)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)  # wait while sound plays
    if outlet:
        outlet.push_sample([f"{eyes}_baseline_done"], local_clock())

# Blink on cue
def blink_on_cue(win, duration=60, interval=4, outlet=None):
    if outlet:
        outlet.push_sample(["Blink_start"], local_clock())
    n_blinks = duration // interval
    start_time = time.time()
    next_blink = start_time + interval
    idx = 0
    while idx < n_blinks:
        if time.time() >= next_blink:
            idx += 1
            show_message(win, f"Blink Now ({idx}/{n_blinks})", wait_key=False, duration=1)
            beep = sound.Sound('A', secs=0.2)   # 'A' = 440 Hz musical note
            beep.play()
            core.wait(1)  # wait while sound plays
            
            if outlet:
                outlet.push_sample([f"Blink_Index:{idx}"], local_clock())
            next_blink += interval
    if outlet:
        outlet.push_sample(["Blink_done"], local_clock())

# Double blink on cue
def double_blink_on_cue(win, duration=30, interval_range=(2,5), outlet=None):
    if outlet:
        outlet.push_sample(["DoubleBlink_start"], local_clock())
    start_time = time.time()
    idx = 0
    while time.time() - start_time < duration:
        interval = random.uniform(*interval_range)
        core.wait(interval)
        idx += 1
        show_message(win, f"Double Blink Now ({idx})", wait_key=False, duration=1)
        beep = sound.Sound('A', secs=0.2)   # 'A' = 440 Hz musical note
        beep.play()
        core.wait(1)  # wait while sound plays
        if outlet:
            outlet.push_sample([f"DoubleBlink_Index:{idx}"], local_clock())
    if outlet:
        outlet.push_sample(["DoubleBlink_done"], local_clock())

# Random voluntary blinks
def random_voluntary_blinks(win, duration=60, outlet=None):
    if outlet:
        outlet.push_sample(["RandomBlink_start"], local_clock())    
    start_time = time.time()
    while time.time() - start_time < duration:
        # randomly show blink prompt every 2-7 sec
        interval = random.uniform(2,7)
        core.wait(interval)
        show_message(win, "Blink Now!", wait_key=False, duration=1)
        beep = sound.Sound('A', secs=0.5).play()  # short beep
        beep.play()
        core.wait(1)  # wait while sound plays

        if outlet:
            outlet.push_sample([f"RandomBlink"], local_clock())
    if outlet:
        outlet.push_sample(["RandomBlink_done"], local_clock())

# Horizontal saccades with moving dot
def horizontal_saccades(win, duration=60, outlet=None):
    msg = visual.TextStim(win, text="Follow the dot left and right until you hear the beep sound.", color='white',  height=0.08, alignText="center")
    msg.draw()
    win.flip()
    core.wait(5)  # instruction display
    
    if outlet:
        outlet.push_sample(["HorizontalSaccades_start"], local_clock())
    
    # # Define moving dot
    # dot = visual.Circle(win, radius=0.05, fillColor='white', lineColor='white')
    # screen_width = win.size[0] / win.size[1]  # normalized units aspect ratio
    # positions = [-0.8 * screen_width, 0.8 * screen_width]  # left and right extremes
    
    # start_time = time.time()
    # pos_index = 0
    
    # while time.time() - start_time < duration:
    #     # Set dot position
    #     dot.pos = (positions[pos_index], 0)  # y=0 keeps it centered vertically
    #     dot.draw()
    #     win.flip()
    #     core.wait(1)  # hold dot for 1 second
        
    #     # Switch left <-> right
    #     pos_index = 1 - pos_index

        # Dot stimulus (in 'norm' units, range -1..1)
    dot = visual.Circle(win, radius=0.05, fillColor='white', lineColor='white', units='norm')
    
    # Left and right positions (x, y)
    positions = [(-0.8, 0), (0.8, 0)]  
    
    start_time = time.time()
    pos_index = 0
    

    while time.time() - start_time < duration:
        # Update dot position
        dot.pos = positions[pos_index]
        dot.draw()
        win.flip()
        core.wait(1)  # hold for 1 sec

        # Switch side
        pos_index = 1 - pos_index
    
    # Beep sound at the end
    beep = sound.Sound('A', secs=0.5)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)  # wait while sound plays
    if outlet:
        outlet.push_sample(["HorizontalSaccades_done"], local_clock())


def vertical_saccades(win, duration=10, outlet=None):
    # Instruction
    msg = visual.TextStim(win, text="Follow the dot up and down until you hear the beep sound.", color='white',  height=0.08, alignText="center")
    msg.draw()
    win.flip()
    core.wait(3)

    if outlet:
        outlet.push_sample(["VerticalSaccades_start"], local_clock())

    # Dot stimulus (in normalized units: -1..+1)
    dot = visual.Circle(win, radius=0.05, fillColor='white', lineColor='white', units='norm')

    # Up and down positions (x, y)
    positions = [(0, 0.8), (0, -0.8)]

    start_time = time.time()
    pos_index = 0

    # Blink-like timing: 200 ms per position
    blink_interval = 0.5  # 0.2 seconds = 200 ms

    while time.time() - start_time < duration:
        # Draw dot
        dot.pos = positions[pos_index]
        dot.draw()

        # Optional: central fixation cross
        fixation = visual.TextStim(win, text="+", color='grey', height=0.05, pos=(0, 0))
        fixation.draw()

        # Flip once per frame
        win.flip()
        core.wait(blink_interval)  # very fast for blink-like rhythm

        # Switch up <-> down
        pos_index = 1 - pos_index

    # Beep at end
    beep = sound.Sound('A', secs=0.5)
    beep.play()
    core.wait(1)

    if outlet:
        outlet.push_sample(["VerticalSaccades_done"], local_clock())

# Eye roll & fixation
def eye_roll_fixation(win, duration=60, outlet=None):
    if outlet:
        outlet.push_sample(["EyeRoll_start"], local_clock())
    msg = visual.TextStim(win, text="Fixate your sight on the center of the screen", color='white',  height=0.08, alignText="center")
    msg.draw()
    win.flip()
    core.wait(5)  # initial fixation
    msg = visual.TextStim(win, text="Roll eyes in circles till you hear the beep sound", color='white',  height=0.08, alignText="center")
    msg.draw()
    win.flip()
    core.wait(duration)
    beep = sound.Sound('A', secs=0.5)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)
    if outlet:
        outlet.push_sample(["EyeRoll_done"], local_clock())

# Jaw clench cycles
def jaw_clench(win, duration=60, outlet=None):
    if outlet:
        outlet.push_sample(["JawClench_start"], local_clock())
    show_message(win, "Clench and release jaw repeatedly till you hear the beep sound.", wait_key=False, duration=duration)
    beep = sound.Sound('A', secs=0.2)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)  # wait while sound plays
    if outlet:
        outlet.push_sample(["JawClench_done"], local_clock())

# Eyebrow raise/frown
def eyebrow_movements(win, duration=60, outlet=None):
    if outlet:
        outlet.push_sample(["EyebrowMovements_start"], local_clock())
    show_message(win, "Raise eyebrows and frown repeatedly till you hear the beep sound.", wait_key=False, duration=duration)
    beep = sound.Sound('A', secs=0.5)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)  # wait while sound plays      
    if outlet:
        outlet.push_sample(["EyebrowMovements_done"], local_clock())

# Head motion
def head_movements(win, duration=60, outlet=None):
    if outlet:
        outlet.push_sample(["HeadMovements_start"], local_clock())
    show_message(win, "Nod your head till you hear the beep sound.", wait_key=False, duration=duration)
    beep = sound.Sound('A', secs=0.5)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)  # wait while sound plays
    if outlet:
        outlet.push_sample(["HeadMovements_done"], local_clock())

# Simulated breathing exercise
def breathing_exercise(win, duration=60, outlet=None):
    if outlet:
        outlet.push_sample(["BreathingExercise_start"], local_clock())
    show_message(win, "Breathe in and out slowly through your mouth till you hear the beep sound.", wait_key=False, duration=duration)
    beep = sound.Sound('A', secs=0.5)   # 'A' = 440 Hz musical note
    beep.play()
    core.wait(1)  # wait while sound plays
    if outlet:
        outlet.push_sample(["BreathingExercise_done"], local_clock())

def microsleep_fixation(win, duration=60, outlet=None):
    # Instruction
    msg = visual.TextStim(win, 
                          text="Keep your eyes on the cross.\n\nOccasionally, follow the dot briefly,\nthen return to the cross until you hear the beep.", 
                          color='white', height=0.08, alignText="center")
    msg.draw()
    win.flip()
    core.wait(5)

    if outlet:
        outlet.push_sample(["MicrosleepFixation_start"], local_clock())

    # Fixation cross
    fixation = visual.TextStim(win, text="+", color='white', height=0.1, pos=(0, 0))

    # Dot for saccades
    dot = visual.Circle(win, radius=0.05, fillColor='white', lineColor='white', units='norm')
    saccade_positions = [(-0.8, 0), (0.8, 0), (0, 0.8), (0, -0.8)]  # L, R, Up, Down

    start_time = time.time()
    next_saccade_time = start_time + random.uniform(5, 10)  # first cue after 5–10s

    while time.time() - start_time < duration:
        now = time.time()

        if now >= next_saccade_time:
            # Show a random saccade target for 1 sec
            pos = random.choice(saccade_positions)
            dot.pos = pos
            dot.draw()
            win.flip()
            core.wait(1)

            # Back to fixation
            fixation.draw()
            win.flip()

            # Schedule next saccade in 5–10s
            next_saccade_time = now + random.uniform(5, 10)
        else:
            # Just fixation
            fixation.draw()
            win.flip()
            core.wait(0.05)

    # Beep at end
    beep = sound.Sound('A', secs=0.5)
    beep.play()
    core.wait(1)

    if outlet:
        outlet.push_sample(["MicrosleepFixation_done"], local_clock())


def pyscho_experiment(win, outlet):
    # ---------------------
    # Psychopy Window
    # ---------------------
    msg = visual.TextStim(win, text="Welcome!\n\nPart 1: Blink once every 5 seconds for 1 minute.\n\nPress any key to begin.", color="white", height=0.08, alignText="center")
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

def main_experiment(win, outlet):
    """
    Main experiment runner with sequential tasks.
    """

    def section_intro(text):
        """Helper: show intro message and wait for keypress."""
        msg = visual.TextStim(win, text=text, color="white", height=0.08, alignText="center")
        msg.draw()
        win.flip()
        event.waitKeys()  # Wait for participant to press a key

    def section_outro(text="Section complete."):
        """Helper: show outro message briefly."""
        msg = visual.TextStim(win, text=text, color="white", height=0.08, alignText="center")
        msg.draw()
        win.flip()
        core.wait(2)

    # -------------------------
    # Sequence of tasks
    # -------------------------

    #1. Eyes open baseline
    section_intro("Part 1: Eyes Close Baseline\n\nRelax with eyes closed for 30 seconds.\n\nPress any key to begin.")
    eyes_baseline(win, duration=30, eyes='Close', outlet=outlet)
    section_outro("Eyes Close Baseline complete.")

    # 2. Blink on cue
    section_intro("Part 2: Blink on cue\n\nBlink every 3 seconds for 90 seconds.\n\nPress any key to begin.")
    blink_on_cue(win, duration=30, interval=3, outlet=outlet)
    section_outro("Blink on cue complete.")

    # 3. Double blink on cue
    section_intro("Part 3: Double Blink\n\nDouble blink whenever prompted for 30 seconds.\n\nPress any key to begin.")
    double_blink_on_cue(win, duration=30, interval_range=(2,5), outlet=outlet)
    section_outro("Double blink section complete.")

    # 4. Random voluntary blinks
    # section_intro("Part 4: Random Blinks\n\nBlink when instructed at unpredictable times for 1 minute.\n\nPress any key to begin.")
    # random_voluntary_blinks(win, duration=60, outlet=outlet)
    # section_outro("Random blink section complete.")

    # 5. Horizontal saccades
    section_intro("Part 5: Horizontal Saccades\n\nShift gaze left and right continuously.\n\nPress any key to begin.")
    horizontal_saccades(win, duration=30, outlet=outlet)
    section_outro("Horizontal saccades complete.")

    # 6. Vertical saccades
    section_intro("Part 6: Vertical Saccades\n\nShift gaze up and down continuously.\n\nPress any key to begin.")
    vertical_saccades(win, duration=30, outlet=outlet)
    section_outro("Vertical saccades complete.")

    section_intro("Rest Baseline\n\nRelax and keep your eyes open for 20 seconds.\n\nPress any key to begin.")
    eyes_baseline(win, duration=20, eyes='open', outlet=outlet)
    section_outro("Rest baseline complete.")
    
    # 7. Eye roll & fixation
    section_intro("Part 7: Eye Roll\n\nRoll your eyes in circles for 30 seconds.\n\nPress any key to begin.")
    eye_roll_fixation(win, duration=30, outlet=outlet)
    section_outro("Eye roll section complete.")

    # 8. Jaw clench cycles
    section_intro("Part 8: Jaw Clench\n\nClench and release your jaw repeatedly for 30 seconds.\n\nPress any key to begin.")
    jaw_clench(win, duration=30, outlet=outlet)
    section_outro("Jaw clench section complete.")

    # 9. Eyebrow raise/frown
    section_intro("Part 9: Eyebrow Movements\n\nRaise and frown your eyebrows repeatedly for 30 seconds.\n\nPress any key to begin.")
    eyebrow_movements(win, duration=30, outlet=outlet)
    section_outro("Eyebrow movements section complete.")

    section_intro("Rest Baseline\n\nRelax and keep your eyes open for 20 seconds.\n\nPress any key to begin.")
    eyes_baseline(win, duration=20, eyes='open', outlet=outlet)
    section_outro("Rest baseline complete.")

    # 10. Head motion
    section_intro("Part 10: Scuba diving simulation Part 1 \n\nNod your head up and down for 30 seconds with continuous feet movement.\n\nPress any key to begin.")
    head_movements(win, duration=30, outlet=outlet)
    section_outro("Simukation of scuba diving section complete.")

    # 11. Simulated breathing exercise
    section_intro("Part 11: Scuba diving simulation Part 2 \n\nBreathing Exercise\n\nBreathe in and out slowly through your mouth for 30 seconds.\n\nPress any key to begin.")
    breathing_exercise(win, duration=30, outlet=outlet)
    section_outro("Breathing exercise section complete.")

    # 12. Microsleep fixation
    section_intro("Part 12: Pilot Simulation : Microsleep Fixation\n\nKeep your eyes on the center cross for 3 minute.\n\nPress any key to begin.")
    microsleep_fixation(win, duration=180, outlet=outlet)
    section_outro("Microsleep fixation section complete.")

    # -------------------------
    # End of experiment
    # -------------------------
    msg = visual.TextStim(win, text="Experiment complete!\n\nThank you for participating.", color="white", height=0.08, alignText="center")
    msg.draw()
    win.flip()
    core.wait(3)