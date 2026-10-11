#pragma once

#include <cstdint>
#include <cstddef>

struct ProbeRecord {
    double sim_time_s;
    double gyro_rad_s[3];
    uint32_t sequence;
};

extern "C" double increment(double value);

extern "C" int32_t copy_probe_record(
    const ProbeRecord* input,
    ProbeRecord* output
);

extern "C" std::size_t probe_record_size();
extern "C" std::size_t probe_record_alignment();
extern "C" std::size_t probe_record_time_offset();
extern "C" std::size_t probe_record_gyro_offset();
extern "C" std::size_t probe_record_sequence_offset();