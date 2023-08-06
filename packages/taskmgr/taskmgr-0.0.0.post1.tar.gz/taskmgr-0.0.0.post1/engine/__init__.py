""" hemi is responsible for running our task. """
import sys

class Hemi:

    def __init__(self):
        sys.path.insert(0, "modules")
    
    def run(self, module, action, args = None):
        """ run will execute the given action within a given module """
        fn = getattr(__import__(module), action)
        if args:
            return fn(args)
        return fn()
