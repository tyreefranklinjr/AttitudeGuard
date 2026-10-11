from typing import Any

import ctypes
from pathlib import Path

from Basilisk.topLevelModules.pyswice import cyllat_c

project_dir = Path(__file__).resolve().parent.parent
library_path = project_dir / "cpp" / "libprobe.dylib"

library = ctypes.CDLL(str(library_path))

library.increment.argtypes = [ctypes.c_double]
library.increment.restype = ctypes.c_double

for value, expected in [(0.0, 0.0), (-1.25, -2.5), (3.5, 7.0)]:
    actual = library.increment(value)
    assert actual == expected, f"FAIL — input {value}: got {actual}, expected {expected}"
    print(f"PASS — input {value}: got {actual}, expected {expected}")

print("PASS - all three scalar checks")

class ProbeRecord(ctypes.Structure):
    _fields_ = [
        ("sim_time_s", ctypes.c_double),
        ("gyro_rad_s", ctypes.c_double * 3),
        ("sequence", ctypes.c_uint32),
    ]

library.copy_probe_record.argtypes = [
    ctypes.POINTER(ProbeRecord),
    ctypes.POINTER(ProbeRecord)
]

library.copy_probe_record.restype = ctypes.c_int32

input_record = ProbeRecord(
    0.1,
    (ctypes.c_double * 3)(0.01, -0.02, 0.03),
    7,
)

for sim_time in [0.0, 0.1, 0.2]:
    input_record.sim_time_s = sim_time
    first_output = ProbeRecord()
    status = library.copy_probe_record(ctypes.byref(input_record), ctypes.byref(first_output))
    assert status == 0, f"FAIL — record copy returned status {status}"
    assert first_output.sim_time_s == input_record.sim_time_s
    assert list(first_output.gyro_rad_s) == list(input_record.gyro_rad_s)
    assert first_output.sequence == input_record.sequence

    print(f"PASS - all fields copied at time {sim_time} s")

    repeated_output = ProbeRecord()
    status = library.copy_probe_record(ctypes.byref(input_record), ctypes.byref(repeated_output))

    assert status == 0, f"FAIL — record copy returned status {status}"
    assert repeated_output.sim_time_s == first_output.sim_time_s
    assert list(repeated_output.gyro_rad_s) == list(first_output.gyro_rad_s)
    assert repeated_output.sequence == first_output.sequence

    print(f"PASS - identical input produces identical fields at {sim_time} s")

# output_record = ProbeRecord()

# status = library.copy_probe_record(
#     ctypes.byref(input_record),
#     ctypes.byref(output_record),
# )

# assert status == 0, f"FAIL — record copy returned status {status}"
# assert output_record.sim_time_s == input_record.sim_time_s
# assert list(output_record.gyro_rad_s) == list(input_record.gyro_rad_s)
# assert output_record.sequence == input_record.sequence

# print("PASS — record copy: time=0.1, gyro=[0.01, -0.02, 0.03], sequence=7")

# status = library.copy_probe_record(
#     None,
#     ctypes.byref(output_record),
# )
# assert status == 1, f"FAIL — null input returned status {status}"
# print("PASS — null input returns status 1")

status = library.copy_probe_record(
    ctypes.byref(input_record),
    None,
)
assert status == 1, f"FAIL — null output returned status {status}"
print("PASS — null output returns status 1")

library.probe_record_size.argtypes = []
library.probe_record_size.restype = ctypes.c_size_t
library.probe_record_alignment.argtypes = []
library.probe_record_alignment.restype = ctypes.c_size_t
library.probe_record_time_offset.argtypes = []
library.probe_record_time_offset.restype = ctypes.c_size_t
library.probe_record_gyro_offset.argtypes = []
library.probe_record_gyro_offset.restype = ctypes.c_size_t
library.probe_record_sequence_offset.argtypes = []
library.probe_record_sequence_offset.restype = ctypes.c_size_t

cpp_size = library.probe_record_size()
cpp_alignment = library.probe_record_alignment()
cpp_time_offset = library.probe_record_time_offset()
cpp_gyro_offset = library.probe_record_gyro_offset()
cpp_sequence_offset = library.probe_record_sequence_offset()

python_size = ctypes.sizeof(ProbeRecord)
python_alignment = ctypes.alignment(ProbeRecord)
python_time_offset = ProbeRecord.sim_time_s.offset
python_gyro_offset = ProbeRecord.gyro_rad_s.offset
python_sequence_offset = ProbeRecord.sequence.offset

assert cpp_size == python_size, f"Size error: C++ - {cpp_size}, Py - {python_size}"
print(f"Size: PASS - c++: {cpp_size}, python: {python_size}")
assert cpp_alignment == python_alignment, f"Alignment error: C++ - {cpp_alignment}, Py - {python_alignment}"
print(f"Alignment: PASS - c++: {cpp_alignment}, python: {python_alignment}")
assert cpp_time_offset == python_time_offset, f"Time error: C++ - {cpp_time_offset}, Py - {python_time_offset}"
print(f"Time: PASS - c++: {cpp_time_offset}, python: {python_time_offset}")
assert cpp_gyro_offset == python_gyro_offset, f"Gyro error: C++ - {cpp_gyro_offset}, Py - {python_gyro_offset}"
print(f"Gyro: PASS - c++: {cpp_gyro_offset}, python: {python_gyro_offset}")
assert cpp_sequence_offset == python_sequence_offset, f"Sequence error: C++ - {cpp_sequence_offset}, Py - {python_sequence_offset}"
print(f"Sequence: PASS - c++: {cpp_sequence_offset}, python: {python_sequence_offset}")

print("PASS - all cpp & python conversion objects matched.")