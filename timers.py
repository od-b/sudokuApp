''' Work in progress '''

# TODO: sync milliseconds of segments to avoid flip flop visual
# DIVISOR = 10 ** len(str(self.total_time - 1))
# print("divisor : " + str(DIVISOR))
# round_and_back = int(round((self.total_time / DIVISOR), None) * DIVISOR)
# self.total_time = round_and_back

class Time_segment:
    def __init__(self, start):
        self.start = start
        self.duration = 0

    def update_duration(self, current_time):
        self.duration = int(self.start - current_time)

    def get_duration(self):
        return self.duration


class Timer:
    def __init__(self):
        self.total = 0
        self.segments = []
        self.n_segments = 0  # to avoid calling len() every frame
        self.fastest = None

    def end_segment(self, archive):
        ''' do not call if segments is empty '''
        if archive:
            fastest = self.get_active_segment().duration
            for seg in self.segments:
                if (seg.duration < fastest):
                    fastest = seg.duration
            self.fastest = min(self.segments)
        else:
            seg = self.segments.pop()
            print(f'removed segment with duration = {seg.get_duration()}')
            self.n_segments = len(self.segments)

    def new_segment(self):
        self.segments.append(Time_segment(self.total))
        self.n_segments = len(self.segments)

    def get_active_segment(self):
        ''' do not call if segments is empty '''
        return self.segments[self.n_segments - 1]

    def update(self, ms_total_time):
        ''' ran every frame to update the time '''
        self.total = ms_total_time
        if (self.n_segments > 0):
            return min(self.segments)
