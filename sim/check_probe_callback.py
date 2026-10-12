from Basilisk.utilities import SimulationBaseClass, macros
from probe_adapter import ProbeAdapter


simulation = SimulationBaseClass.SimBaseClass()

process = simulation.CreateNewProcess("probeProcess")

task_name = "flightSoftwareTask"
period_ns = macros.sec2nano(0.1)

process.addTask(
    simulation.CreateNewTask(task_name, period_ns)
)

adapter = ProbeAdapter()
simulation.AddModelToTask(task_name, adapter)

simulation.InitializeSimulation()
simulation.ConfigureStopTime(macros.sec2nano(0.5))
simulation.ExecuteSimulation()

# Verify that Basilisk invoked the adapter on every expected tick.
results = adapter.callback_results
expected_times = [tick * period_ns for tick in range(6)]
actual_times = [entry["time_ns"] for entry in results]

assert actual_times == expected_times, (
    f"FAIL — callback times: {actual_times}; expected {expected_times}"
)

for index, entry in enumerate(results):
    assert entry["input_sequence"] == index, (
        f"FAIL — input sequence at tick {index}"
    )
    assert entry["returned_sequence"] == entry["input_sequence"], (
        f"FAIL — returned sequence at tick {index}"
    )

for previous, current in zip(results, results[1:]):
    assert current["time_ns"] - previous["time_ns"] == period_ns, (
        "FAIL — incorrect callback spacing"
    )

print("PASS — Basilisk invoked all six callbacks from 0.0 through 0.5 s")
print("PASS — flight-software callback period is 0.1 s")
print("PASS — input sequences advance and returned sequences match")