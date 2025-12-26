from homeassistant.util import dt as dt_util

from custom_components.dose_nudge.medication_manager import MedicationManager, MedicationConfig

class DummyStore:
    async def async_save_state(self, state):
        self.state = state

def test_is_due_when_never_taken():
    mgr = MedicationManager(state={}, store=DummyStore())
    cfg = MedicationConfig(name="Test", interval_hours=8)
    assert mgr.is_due("med", cfg) is True

def test_is_not_due_shortly_after_taken():
    now = dt_util.now()
    state = {"med": {"last_taken": now.isoformat()}}
    mgr = MedicationManager(state=state, store=DummyStore())
    cfg = MedicationConfig(name="Test", interval_hours=8)
    assert mgr.is_due("med", cfg) is False
