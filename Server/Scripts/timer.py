import time


# Keeps track of the minutes and hours
class Timer:

    def __init__(self):
        self.minute = 0
        self.hour = 0
        self.start_time = time.clock()
        self.last_time = self.start_time
        self.current_time = ''

    def update_time(self):
        self.current_time = time.clock()

        if self.current_time - self.last_time >= 6:
            self.minute += 1
            self.last_time = self.current_time
        if self.minute >= 60:
            self.hour += 1
            self.minute = 0
        if self.hour > 24:
            self.hour = 0
        print('Minute: ' + str(self.minute))
        print('Hour: ' + str(self.hour))
