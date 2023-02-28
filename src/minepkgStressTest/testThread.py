# Thread override necessary to run seperate threads and get information from them.

from threading import Thread, Timer
import subprocess

kill = lambda process: process.terminate()

class testThread(Thread):
    def __init__(self, version):
        
        Thread.__init__(self)
        
        self.state = False
        self.vers = version
        
    def run(self):
        print(self.vers)
        cmd = 'minepkg launch vanilla --minecraft=' + str(self.vers)
        proc = subprocess.Popen(
                        cmd,
                        text=True,
                        stdout=subprocess.PIPE,
                        shell=True,
                        universal_newlines=True,
                        bufsize=1,
                        )
        timer = Timer(30, kill, [ proc ])
        timer.start()
        shortcut = False
        for line in proc.stdout:
            print(line)
            try:
                if '[Render thread/INFO]: Created: 256x128x0 minecraft:textures/atlas/mob_effects.png-atlas' in line and not shortcut:
                    timer.cancel()
                    timer = Timer(5, kill, [ proc ])
                    timer.start()
                    shortcut = True
                    self.state = True
                if '[Sound Library Loader/INFO]: Sound engine started' in line and not shortcut:
                    timer.cancel()
                    timer = Timer(5, kill, [ proc ])
                    timer.start()
                    shortcut = True
                    self.state = True
                if '[Client thread/INFO]: Created: 256x128 textures/mob_effect-atlas' in line and not shortcut:
                    timer.cancel()
                    timer = Timer(5, kill, [ proc ])
                    timer.start()
                    shortcut = True
                    self.state = True
                if '[CLIENT] [INFO] Found animation info for: textures/items/compass.txt' in line and not shortcut:
                    timer.cancel()
                    timer = Timer(5, kill, [ proc ])
                    timer.start()
                    shortcut = True
                    self.state = True
                if 'Turning of ImageIO disk-caching' in line and not shortcut:
                    timer.cancel()
                    timer = Timer(5, kill, [ proc ])
                    timer.start()
                    shortcut = True
                    self.state = True
                if 'Initializing LWJGL OpenAL' in line and not shortcut:
                    timer.cancel()
                    timer = Timer(5, kill, [ proc ])
                    timer.start()
                    shortcut = True
                    self.state = True
                    
            except subprocess.CalledProcessError as e:
                print('EXCEPTION FROM minepkgStressTest::subprocess.CalledProcessError:' + e)
                timer.cancel()
                self.state = False
            except subprocess.SubprocessError as e:
                print('EXCEPTION FROM minepkgStressTest::subprocess.SubprocessError' + e)
                timer.cancel()
                self.state = False

        if proc.poll() == 0:
            self.state = True

        if proc.poll() != 0:
            if proc.returncode == -15:
                self.state = True
            elif proc.returncode == 1:
                self.state = True
            else:
                print('unknown returncode: ' + str(proc.returncode))
                self.state = False