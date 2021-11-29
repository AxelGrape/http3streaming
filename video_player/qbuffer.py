class QBuffer():

    def __init__(self, mpd):
        self.buffer = []


    def buffer_time(self):
        sum = 0
        for i, v in enumerate(self.buffer):
            t = self.mpd.get_segment_duration(self.buffer[i][0])
            sum += t

        return sum


    def fill_buffer(self):
        max_buffer_time = self.mpd.get_buffer_time()
        
        while self.buffer_time() < max_buffer_time:
            self.buffer.append(self.mpd.get_next_segment(0))


    def add_segment(self, segment):
        self.buffer.append(segment)


    def remove_segment(self, segment = None):
        if type(segment) == int:
            del self.buffer[segment]
        else:
            if segment == None:
                del self.buffer[0]
            elif segment != None:
                self.buffer.remove(segment)
    