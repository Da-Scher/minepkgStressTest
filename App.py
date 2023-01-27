#

import re, urllib.request, json, subprocess

from threading import Timer

# global(s)
versionlist = []

kill = lambda process: process.terminate()



def run_process(version):
    state = False
    cmd = 'minepkg launch vanilla --minecraft=' + version
    proc = subprocess.Popen(cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True,
                    bufsize=1
                    )
    timer = Timer(30, kill, [ proc ])
    timer.start()
    for line in proc.stdout:
        try:
            if '[Render thread/INFO]: Created: 256x128x0 minecraft:textures/atlas/mob_effects.png-atlas' in line and state == False:
                timer.cancel()
                Timer(5, kill, [ proc ]).start()
                state = True
        except subprocess.CalledProcessError as e:
            print('EXCEPTION:subprocess.CalledProcessError:' + e)
            return False
        except subprocess.SubprocessError as e:
            print('EXCEPTION:subprocess.SubprocessError' + e)
            return False
    
    if proc.poll() == 0:
        return True
    
    if proc.poll() != 0:
        if proc.returncode == -15:
            return True
        else:
            print('unknown returncode: ' + str(proc.returncode))
            return False
        
    print('hello?')
    
    # assume failure
    return False


print('anything?')
# 1. get the version list from the json.
with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
    data = json.load(url)
    versions = json.JSONEncoder().encode(data['versions'])
    version_id = json.loads(versions)
    for idx in range(0, len(version_id)):
        versionlist.append(version_id[idx]['id'])
    print('got our version list')

# 2. populate output file with test.
with open('output', 'w') as output_file:
    process = False
    x = 0
    for version in versionlist:
        # fixing mojang versioning to match with minepkg stanards
        if re.match('^\d+.\d+(?:-[A-Za-z0-9-]*)?$', version):
                if re.match('^\d+.\d+[-]', version):
                    version = re.sub('[-]', '.0-', version)
                elif re.match('^\d+.\d+$', version):
                    version = re.sub('$', '.0', version)
        # now that we have an appropriate version we can construct a minepkg command
        if run_process(version) == True:
            output_file.write( version + ' PASS\n' )
        else:
            output_file.write( version + ' FAIL\n' )

# 3. close file and stop.