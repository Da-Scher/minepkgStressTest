#   Dakota Schaeffer
#       This script test runs every version of minecraft using minepkg 
#

import re, urllib.request, json, sys, math

import testThread

# global(s)
# the version list needs to be known everywhere
versionlist = []

bigversionlist = []

# "constant(s)"
# number of threads to use
THREADCOUNT = 1

#Binary search mode control
BSMODE = True

def returnDate(version):
    return version['releaseTime']

def cleanVersion(version):
    if re.match('^\d+.\d+(?:-[A-Za-z0-9-]*)?$', version):
        if re.match('^\d+.\d+[-]', version):
            version = re.sub('[-]', '.0-', version)
        elif re.match('^\d+.\d+$', version):
            version = re.sub('$', '.0', version)
    return version

# 1. get the version list from the json.
with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
    data = json.load(url)
    versions = json.JSONEncoder().encode(data['versions'])
    version_id = json.loads(versions)
    if BSMODE:
        for idx in range(0, len(version_id)):
            #populate version list
            bigversionlist.append(version_id[idx])
        #sort by date
        #the json may be sorted by date already, but to be safe 
        bigversionlist.sort(key=returnDate)
        #print(bigversionlist[0])
        for idx in range (0, len(bigversionlist)):
            versionlist.append([bigversionlist[idx]['id'], False])
            
    else:
        for idx in range(0, len(version_id)):
            versionlist[idx] = ([version_id[idx]['id'], False])

# 2. populate output file with test.
with open('output', 'w') as output_file:
    process = False
    idx = 0
    if BSMODE:
        running = True
        x2      = len(versionlist) - 1
        x1      = 0
        dx      = 0
        x       = 0
        while running:
            if x2 == x1 or dx == 1:
                version = versionlist[x1][0]
                cleanVersion(version)
                test = testThread.testThread(version)
                test.start()
                test.join()
                versionlist[x1] = [versionlist[x1][0], test.state]
                print('last root!')
                print(f"x1 = {x1}: x2 = {x2}")
                break
            elif x2 < x1:
                print('tree broke!')
                print(f"x1 = {x1}: x2 = {x2}")
                break
            else:
                dx = x2 - x1
                x  = dx//2 + x1
                print(f"x1 = {x1}: x2 = {x2}\nx={x}")
                version = versionlist[x][0]
                cleanVersion(version)
                test = testThread.testThread(version)
                test.start()
                test.join()
                versionlist[x] = [versionlist[x][0], test.state]
                if test.state == False:
                    x1 = x
                if test.state == True:
                    for idx in range(x, len(versionlist)):
                        versionlist[idx] = [versionlist[idx][0], True]
                    x2 = x
        for idx in range(0, len(versionlist)):
            if versionlist[idx][1] == True:
                output_file.write(f"{versionlist[idx][0]} PASS\n")
            else:
                output_file.write(f"{versionlist[idx][0]} FAIL\n")
                
                
                

    else:   
        while idx < len(versionlist):
                exit
                threads = []
                # fixing mojang versioning to match with minepkg stanards
                for thread in range(0, THREADCOUNT):
                    version = versionlist[idx]
                    #  if re.match('^\d+.\d+(?:-[A-Za-z0-9-]*)?$', version):
                    #         if re.match('^\d+.\d+[-]', version):
                    #             version = re.sub('[-]', '.0-', version)
                    #         elif re.match('^\d+.\d+$', version):
                    #             version = re.sub('$', '.0', version)
                    idx += 1
                    # now that we have an appropriate version we can construct a minepkg command
                    threads.append(testThread.testThread(version))
                    threads[thread].start()
                for thread in threads:
                    print(thread.is_alive())
                    if not thread.is_alive():
                        version = versionlist[idx]
                        if re.match('^\d+.\d+(?:-[A-Za-z0-9-]*)?$', version):
                            if re.match('^\d+.\d+[-]', version):
                                version = re.sub('[-]', '.0-', version)
                            elif re.match('^\d+.\d+$', version):
                                version = re.sub('$', '.0', version)
                        idx += 1
                        threads[thread] = testThread.testThread(version)
                        threads[thread].start()
                for thread in threads:
                    thread.join()
                    output_file.write(thread.state)
