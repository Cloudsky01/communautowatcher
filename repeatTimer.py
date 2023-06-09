from threading import Timer


# Source : https://stackoverflow.com/questions/12435211/threading-timer-repeat-function-every-n-seconds

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)