#include "probe.h"

extern "C" double increment(double value) {
    return value * 2.0;
};

extern "C" int32_t copy_probe_record(
    const ProbeRecord* input,
    ProbeRecord* output
) {
    if (input == nullptr || output == nullptr) {
        return 1;
    }

    output->sim_time_s = input->sim_time_s;

    for (int i = 0; i < 3; ++i) {
        output->gyro_rad_s[i] = input->gyro_rad_s[i];
    }

    output->sequence = input->sequence;

    return 0;
}

extern "C" std::size_t probe_record_size() {return sizeof(ProbeRecord);}
extern "C" std::size_t probe_record_alignment() {return alignof(ProbeRecord);}
extern "C" std::size_t probe_record_time_offset() {return offsetof(ProbeRecord, sim_time_s);}
extern "C" std::size_t probe_record_gyro_offset() {return offsetof(ProbeRecord, gyro_rad_s);}
extern "C" std::size_t probe_record_sequence_offset() {return offsetof(ProbeRecord, sequence);}