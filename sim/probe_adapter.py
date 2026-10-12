import ctypes
from pathlib import Path
from Basilisk.architecture import sysModel

class ProbeRecord(ctypes.Structure):
    _fields_ = [
        ("sim_time_s", ctypes.c_double),
        ("gyro_rad_s", ctypes.c_double * 3),
        ("sequence", ctypes.c_uint32),
    ]

class ProbeAdapter(sysModel.SysModel):
    def __init__(self):
        super().__init__()
        self.ModelTag = "ProbeAdapter"

        project_dir = Path(__file__).resolve().parent.parent
        library_path = project_dir / "cpp" / "libprobe.dylib"
        
        self.library = ctypes.CDLL(str(library_path))

        self.library.copy_probe_record.argtypes = [
            ctypes.POINTER(ProbeRecord),
            ctypes.POINTER(ProbeRecord),
        ]
        self.library.copy_probe_record.restype = ctypes.c_int32
        self.sequence = 0
        self.callback_results = []
    
    def Reset(self, CurrentSimNanos):
        self.sequence = 0
        self.callback_results.clear()

    def UpdateState(self, CurrentSimNanos):
        sim_time_s = CurrentSimNanos * 1e-9
        input_record = ProbeRecord(
            sim_time_s,
            (ctypes.c_double * 3)(0.01, -0.02, 0.03),
            self.sequence,
        )
        output_record = ProbeRecord()

        status = self.library.copy_probe_record(
            ctypes.byref(input_record), ctypes.byref(output_record),
        )

        assert status == 0, f"FAIL - callback returned status {status}"
        assert output_record.sim_time_s == input_record.sim_time_s
        assert list(output_record.gyro_rad_s) == list(input_record.gyro_rad_s)
        assert output_record.sequence == input_record.sequence

        self.callback_results.append(
            {
                "time_ns": CurrentSimNanos,
                "time_s": sim_time_s,
                "input_sequence": input_record.sequence,
                "returned_sequence": output_record.sequence,
            }
        )

        print(f"PASS - callback time={sim_time_s:.3f} s, " f"input sequence={input_record.sequence}, " f"returned sequence={output_record.sequence}")
        self.sequence += 1
