from dataclasses import dataclass


@dataclass
class MetricI():
    
    def group():
        pass

@dataclass
class ColorHistogram(MetricI):
    pass


@dataclass
class Object(MetricI):
    pass


@dataclass
class Identity(MetricI):
    pass

