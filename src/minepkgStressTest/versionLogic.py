# if 1.19.4 works, we can safely assume 1.19.0 - 1.19.3 works.
# if 1.19.4 doesn't work, we should try 1.19.3. if 1.19.3 works, we can safely assume 1.19.0 - 1.19.2 works.
# etc. repeat for all versions 1.0+
# TODO come up with a similar system for beta, alpha, and early versions.

def latestVersion(vers):
    
    return vers