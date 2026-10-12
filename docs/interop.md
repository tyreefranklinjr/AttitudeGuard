# C++–Python Interoperability

**SC-03 · AttitudeGuard · Verified October 11, 2026**

A C++20 shared library exchanges typed scalar values and records with Python. A dedicated Basilisk flight-software task invokes the same interface every **0.1 seconds**.

**Status: SC-03 complete.** The C++20 build, standalone interface checks, and actual Basilisk callbacks pass. Full results are saved in the evidence file.

## Project files

- [Header](../cpp/probe.h) — record definition and exported declarations.
- [Implementation](../cpp/probe.cpp) — scalar, record-copy, and layout functions.
- `cpp/libprobe.dylib` — compiled macOS library.
- [Standalone checks](../tests/check_probe.py) — scalar, record, boundary, and layout tests.
- [Adapter](../sim/probe_adapter.py) — library connection and scheduled callback.
- [Callback scenario](../sim/check_probe_callback.py) — short Basilisk integration test.
- [Saved evidence](../results/interop-checks.txt) — complete build, standalone, and callback results.

## Build and run

Use the existing project and isolated environment:

```sh
cd ~/AttitudeGuard
source .venv/bin/activate
clang++ -std=c++20 -dynamiclib cpp/probe.cpp -o cpp/libprobe.dylib
```

**Working directory:** `/Users/tyreefranklinjr/AttitudeGuard`

**Library path:** `/Users/tyreefranklinjr/AttitudeGuard/cpp/libprobe.dylib`

The build command above was executed successfully during verification, followed by both tests against the rebuilt library.

Run the checks:

```sh
python tests/check_probe.py
python sim/check_probe_callback.py
```

To refresh the standalone and callback evidence after future changes:

```sh
python tests/check_probe.py > results/interop-checks.txt 2>&1 &&
python sim/check_probe_callback.py >> results/interop-checks.txt 2>&1
```

The first command replaces the evidence file. The second appends callback results only if the first succeeds. Run without Python's `-O` flag, which disables assertions.

## Interface contract

All exported functions use `extern "C"`. Python loads the library with `ctypes.CDLL` and explicitly declares argument and return types. C++ classes, strings, vectors, and exceptions do not cross this interface.

**Scalar:** `increment(double)` returns twice the input. Python declares one `c_double` argument and a `c_double` result.

**Record copy:** `copy_probe_record(const ProbeRecord*, ProbeRecord*)` accepts input and output pointers. Python declares two `POINTER(ProbeRecord)` arguments and a `c_int32` result.

- **Ownership:** Python creates and retains both records during the synchronous call. C++ does not allocate, free, or retain their memory.
- **Success:** status `0`; all fields are copied into the output.
- **Invalid pointer:** status `1` if input or output is null, checked before either is accessed.
- **Input:** read through a const pointer; the function does not modify it.

## Record layout and units

Field order is identical in C++ and `ctypes.Structure`:

```cpp
struct ProbeRecord {
    double sim_time_s;
    double gyro_rad_s[3];
    uint32_t sequence;
};
```

- `sim_time_s`: seconds; offset **0 bytes**.
- `gyro_rad_s`: three angular-rate components in rad/s; offset **8 bytes**. Callback values are synthetic test data, with no sensor or frame interpretation asserted here.
- `sequence`: unsigned 32-bit sample identifier; offset **32 bytes**.

**Measured on both sides:** size **40 bytes**, alignment **8 bytes**. Fields occupy 36 bytes; the layout includes 4 trailing padding bytes. No packing is forced.

C++ exposes `sizeof`, `alignof`, and each `offsetof` through no-argument functions returning `std::size_t`. Python uses `c_size_t` results and compares them with `ctypes.sizeof`, `ctypes.alignment`, and field `.offset` values. Repeatability checks compare fields, not padding bytes.

## Basilisk callback

`ProbeAdapter` derives from `sysModel.SysModel`. Initialization loads the library once; `Reset` clears the sequence and callback log.

Basilisk invokes `UpdateState` on `flightSoftwareTask`. Each update converts the supplied integer nanoseconds to seconds, copies a record through C++, verifies its fields, and records callback time plus input/returned sequences.

The dedicated scenario runs through **0.5 seconds**:

- Observed ticks: **0.0, 0.1, 0.2, 0.3, 0.4, 0.5 seconds**.
- Verified spacing: **100,000,000 nanoseconds**.
- Input and returned sequences: **0 through 5**, matching at every tick.
- Synthetic gyro input: **[0.01, -0.02, 0.03] rad/s**.

This proves scheduling by Basilisk itself. It is a minimal task integration test, without spacecraft dynamics; the preserved spacecraft baseline remains unchanged.

## Acceptance record

These statuses reflect the current verification and the saved results file.

- **PASS** — C++20 shared library rebuilt, loads, and exposes its required functions.
- **PASS** — scalar inputs `0.0`, `-1.25`, `3.5` return `0.0`, `-2.5`, `7.0`.
- **PASS** — time, all three gyro values, and sequence copy correctly, including the required time `0.1` and sequence `7`.
- **PASS** — size, alignment, and every field offset match.
- **PASS** — null output returns status `1`.
- **PASS** — null input returns status `1` without crashing.
- **PASS** — record calls at `0.0`, `0.1`, `0.2` seconds and repeated identical inputs.
- **PASS** — six actual Basilisk callbacks, task spacing, and sequence checks.
- **PASS** — combined build, standalone, and callback evidence saved; both scripts exit with status `0`.

SC-03 verifies the language interface and scheduling. Spacecraft physics, original control, and fault recovery are separate milestones.
