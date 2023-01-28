# Thread override necessary to run seperate threads and get information from them.

from threading import Thread, Timer
import subprocess

kill = lambda process: process.terminate()

class testThread(Thread):
    def __init__(self, version):
        
        Thread.__init__(self)
        
        self.state = None
        self.vers = version
        
    def run(self):
        cmd = 'minepkg launch vanilla --minecraft=' + str(self.vers)
        proc = subprocess.Popen(cmd,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        shell=True,
                        universal_newlines=True,
                        bufsize=1
                        )
        timer = Timer(30, kill, [ proc ])
        timer.start()
        shortcut = False
        for line in proc.stdout:
            try:
                if '[Render thread/INFO]: Created: 256x128x0 minecraft:textures/atlas/mob_effects.png-atlas' in line and shortcut == False:
                    timer.cancel()
                    Timer(5, kill, [ proc ]).start()
                    shortcut = True
                    self.state = f'{str(self.vers)} {str("PASS")}\n'
                if '[Sound Library Loader/INFO]: Sound engine started' in line and shortcut == False:
                    timer.cancel()
                    Timer(5, kill, [ proc ]).start()
                    shortcut = True
                    self.state = f'{str(self.vers)} {str("PASS")}\n'
                if '[Client thread/INFO]: Created: 256x128 textures/mob_effect-atlas' in line and shortcut == False:
                    timer.cancel()
                    Timer(5, kill, [ proc ]).start()
                    shortcut = True
                    self.state = f'{str(self.vers)} {str("PASS")}\n'
            except subprocess.CalledProcessError as e:
                print('EXCEPTION FROM minepkgStressTest::subprocess.CalledProcessError:' + e)
                timer.cancel()
                self.state = f'{str(self.vers)} {str("FAIL")}\n'
            except subprocess.SubprocessError as e:
                print('EXCEPTION FROM minepkgStressTest::subprocess.SubprocessError' + e)
                timer.cancel()
                self.state = f'{str(self.vers)} {str("FAIL")}\n'

        if proc.poll() == 0:
            self.state = f'{str(self.vers)} {str("PASS")}\n'

        if proc.poll() != 0:
            if proc.returncode == -15:
                self.state = f'{str(self.vers)} {str("PASS")}\n'
            else:
                print('unknown returncode: ' + str(proc.returncode))
                self.state = f'{str(self.vers)} {str("FAIL")}\n'