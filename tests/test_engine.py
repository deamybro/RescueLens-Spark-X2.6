"""
RescueLens Unit & Regression Tests
Ensures strict schema validation, reasoning output parsing, and prioritization stability.
"""

import os
import sys
import unittest

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from engine import SparkTriageEngine
from schemas import EmergencyTriageResult

class TestRescueLens(unittest.TestCase):
    def setUp(self):
        self.engine = SparkTriageEngine()

    def test_flood_p1_extraction(self):
        msg = "Water is reaching 2nd floor on Riverside Ave. Grandma is diabetic, out of insulin, 8-month infant present. Need boat!"
        res, raw = self.engine.triage_incident("TEST-001", msg, channel="SMS", disaster_hint="Flood")
        
        self.assertIsInstance(res, EmergencyTriageResult)
        self.assertEqual(res.priority_level, "P1-Immediate")
        self.assertGreaterEqual(res.urgency_score, 8)
        self.assertIn("Riverside Ave", res.location.raw_location_text or res.location.landmarks)
        self.assertTrue(any(r.category == "boat_rescue" for r in res.resources_required))
        self.assertTrue(any(r.category == "medical" for r in res.resources_required))
        self.assertTrue("<think>" in raw and "</think>" in raw)

    def test_routine_logistics_extraction(self):
        msg = "Shelter safe, diesel generator has 8 hours left. 45 people here. Request fuel delivery tomorrow morning."
        res, raw = self.engine.triage_incident("TEST-002", msg, channel="Shelter", disaster_hint="Logistics")
        
        self.assertIsInstance(res, EmergencyTriageResult)
        self.assertEqual(res.priority_level, "P3-Routine")
        self.assertLessEqual(res.urgency_score, 4)
        self.assertTrue(any(r.category == "fuel_power" for r in res.resources_required))

if __name__ == "__main__":
    unittest.main()
