# if 1.19.4 works, we can safely assume 1.19.0 - 1.19.3 works.
# if 1.19.4 doesn't work, we should try 1.19.3. if 1.19.3 works, we can safely assume 1.19.0 - 1.19.2 works.
# etc. repeat for all versions 1.0+
# TODO come up with a similar system for beta, alpha, and early versions.

import re

class versionLogic:
    def __init__(self, versions):
        self.version_list = versions
        pass        
    def latestVersion(self, vers, status):
        # create a mini list from version_list
        minor_list = []
        for version in self.version_list:
            if vers in version:
                minor_list.append(version)
        
        for version in minor_list:
            # skip rc's
            if re.match('(?:-[A-Za-z0-9-]*)?$', version):
                print(f'skipping {version}')
            else:
                print(f'{version} valid choice')
                break
            return None