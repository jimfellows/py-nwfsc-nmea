import time
from .kinematics import VesselState

class Simulator:
    """
    Core engine loop that iterates the vessel physics 
    and drives the generators to publish data to sinks.
    """
    def __init__(self, hz: float = 1.0):
        self.hz = hz
        self.state = VesselState()
        self.sinks = []
        self.generators = []
        self._running = False

    def add_sink(self, sink):
        self.sinks.append(sink)

    def add_generator(self, generator):
        self.generators.append(generator)

    def start(self):
        for sink in self.sinks:
            sink.open()
            
        self._running = True
        try:
            self._loop()
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        self._running = False
        for sink in self.sinks:
            sink.close()

    def _loop(self):
        interval = 1.0 / self.hz
        
        while self._running:
            start_t = time.time()
            
            # Physics Step
            self.state.update()
            
            # Generate and publish NMEA strings
            sentences = []
            for gen in self.generators:
                gen_sents = gen.generate(self.state)
                if gen_sents:
                    if isinstance(gen_sents, list):
                        sentences.extend(gen_sents)
                    else:
                        sentences.append(gen_sents)
                        
            for sentence in sentences:
                for sink in self.sinks:
                    sink.write(sentence)
                    
            # Sleep to maintain frequency
            elapsed = time.time() - start_t
            if elapsed < interval:
                time.sleep(interval - elapsed)
