#   Dakota Schaeffer
#       This script test runs every version of minecraft using minepkg 
#

import re, urllib.request, json, sys

import testThread

# global(s)
# the version list needs to be known everywhere
versionlist = []

# "constant(s)"
# number of threads to use
THREADCOUNT = 1



# 1. get the version list from the json.
with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
    data = json.load(url)
    versions = json.JSONEncoder().encode(data['versions'])
    version_id = json.loads(versions)
    for idx in range(0, len(version_id)):
        versionlist.append(version_id[idx]['id'])

# 2. populate output file with test.
with open('output', 'w') as output_file:
    process = False
    idx = 0
    while idx < len(versionlist):
        threads = []
        # fixing mojang versioning to match with minepkg stanards
        for thread in range(0, THREADCOUNT):
            version = versionlist[idx]
            if re.match('^\d+.\d+(?:-[A-Za-z0-9-]*)?$', version):
                    if re.match('^\d+.\d+[-]', version):
                        version = re.sub('[-]', '.0-', version)
                    elif re.match('^\d+.\d+$', version):
                        version = re.sub('$', '.0', version)
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
            