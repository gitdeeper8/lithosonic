import pytest
from litho_physics.emission import AEClassifier, Event

class TestEmission:
    def test_ae_rate(self):
        classifier = AEClassifier()
        for i in range(10):
            event = Event(timestamp=i, magnitude=-1.0, location=(0,0,0), energy=1e-6)
            classifier.add_event(event)
        rate = classifier.compute_rate(10)
        assert rate == 1.0
