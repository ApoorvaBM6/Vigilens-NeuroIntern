from subprocess import PIPE, Popen
import os
import debugpy
import time
        
class LabRecorderCLI():
    '''Process based interface for LabRecorder
        
    Example::
              
        cmd = 'C:\\tools\\lsl\\LabRecorder\\LabRecorderCLI.exe'
        filename = os.path.join(os.path.expanduser('~'), 'Desktop\\untitled.xdf')                
        streams = "type='EEG' type='Markers'"
        streams = "type='dfg'"
        lr = LabRecorderCLI(cmd)
        lr.start_recording(filename, streams)
        print('Start recording')
        time.sleep(5)
        print('Stop recording')    
        lr.stop_recording()
        
    '''
    def __init__(self, cmd) -> None:
        if not os.path.exists(cmd):
            raise FileNotFoundError
        self.cmd = cmd
        
    def start_recording(self, filename:str, streams: str) -> None:

        #stream_list = json.loads(streams)
        #stream_arg = f'{s}' for s in streams if isinstance(s, (str, tuple, list))
        cmd = ' '.join((self.cmd, filename, streams))
        self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)   
        peek =  self.process.stdout.peek()
        if b'matched no stream' in peek:
            raise ConnectionError(peek.decode().strip())
        # except json.JSONDecodeError:

        #     raise ValueError("Invalid JSON format for streams argument" + str(streams))

    def stop_recording(self) -> None:
        if hasattr(self, 'process'):       
            o, e = self.process.communicate(b'\n')
            if self.process.poll() != 0:
                raise ConnectionError(o + e)            
    
# cmd = 'D:\\France\\ISAE\\Internship\\Tools\\LabRecorder-1.16.4-Win_amd64\\LabRecorder\\LabRecorderCLI.exe'
# filename = os.path.join(os.path.expanduser('~'), 'Desktop\\untitled.xdf')                
# streams = "type='EEG' type='Markers'"
# lr = LabRecorderCLI(cmd)
# lr.start_recording(filename, streams)
# print('Start recording')
# time.sleep(5)
# print('Stop recording')    
# lr.stop_recording()