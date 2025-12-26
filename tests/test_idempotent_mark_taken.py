import asyncio

from custom_components.dose_nudge.medication_manager import MedicationManager

class DummyStore:
    def __init__(self):
        self.saves = 0
    async def async_save_state(self, state):
        self.saves += 1

def test_mark_taken_idempotent():
    store = DummyStore()
    mgr = MedicationManager(state={}, store=store)

    async def run():
        first = await mgr.mark_taken("med")
        second = await mgr.mark_taken("med")
        return first, second, store.saves

    first, second, saves = asyncio.get_event_loop().run_until_complete(run())
    assert first is True
    assert second is False
    assert saves == 1
