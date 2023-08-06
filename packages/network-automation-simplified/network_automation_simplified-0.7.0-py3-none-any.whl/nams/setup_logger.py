from os import path
from yaml import warnings

warnings({'YAMLLoadWarning': False})

def log_decorator(func):
    def log(*args, title=False, char="*"):
        Logger, msg = args[0], args[1]
        results = Logger.router.results

        # create title message
        if title:
            chars = char * (100 - len(args[1]))
            msg = f"\n[{msg}] {chars}"

        # increment fatal or success
        if "fatal" in msg:
            results.report["fatal"] += 1
        elif "success" in msg:
            results.report["successful"] += 1

        # write to file
        Logger.file.write(f"{msg}\n")

        # write to text log
        results.log += f"{msg}\n"

        # append to errors
        if "fatal" in msg:
            results.errors.append(msg[7:])

        # 'func' is print or don't print
        func(Logger, msg)

    # return the decorated function
    return log

class Logger:
    '''
    The standard 'logging' library was not used because it interfered with the
    Jsnapy library.  No work around could be found.
    '''

    def __init__(self, router):
        self.router = router

        if router.requests.silent:
            self.debug = self.stdout_off
        else:
            self.debug = self.stdout_on

    def close(self):
        try:
            self.file.close()
        except OSError as e:
            self.debug(f"fatal: could not save file --> {e}")

    def open(self):
        fn = f"{self.router.inventory.hostname}.log"
        self.file = open(path.join(self.router.output_dir, fn), "w")

    @log_decorator
    def stdout_on(self, message):
        print(message)

    @log_decorator
    def stdout_off(self, message):
        return None

class Results:
    '''
    This is the object that will be returned to the caller. There are
    predefined attributes e.g. 'log', 'report', etc. at instantiation and
    attributes can be added after execution e.g. 'self.diff', 'self.rpcs', etc.
    '''

    def __init__(self, output_dir, hostname):
        self.hostname = hostname
        self.log = ""
        self.errors = []
        self.report = {"fatal": 0, "successful": 0}
        self.healthy = {'pre': 'unknown', 'pst': 'unknown'}
        self.changed = False

    def __str__(self):
        results = ""

        for item in dir(self):
            if not item.startswith("__") and not item.startswith("_"):
                if isinstance(getattr(self, item), types.MethodType):
                    results += f" object.{item}()\n"
                else:
                    results += f" object.{item}\n"

        return results

    def __bool__(self):
        if self.report["fatal"] == 0 and self.report["successful"] >= 1:
            return True
        else:
            return False

