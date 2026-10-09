# C++–Python Interoperability

## Shared library

A C++20 library exposes `increment(double)` to Python through an `extern "C"` interface. The function returns twice its input.

| File | Purpose |
| --- | --- |
| `cpp/probe.h` | Function declaration |
| `cpp/probe.cpp` | Function implementation |
| `cpp/libprobe.dylib` | Compiled macOS shared library |

## Build command

Run from the project directory:

```sh
cd ~/AttitudeGuard
clang++ -std=c++20 -dynamiclib cpp/probe.cpp -o cpp/libprobe.dylib
```

**Library path:** `/Users/tyreefranklinjr/AttitudeGuard/cpp/libprobe.dylib`

## Build verification

Confirm the output exists:

```sh
ls -lh cpp/libprobe.dylib
```

**Build status:** NOT RUN — update to PASS or FAIL after verification.

## Remaining checks

- NOT RUN — Python scalar calls
- NOT RUN — Record layout and field copying
- NOT RUN — Null-pointer handling
- NOT RUN — Repeated-input checks
- NOT RUN — Basilisk simulation-clock callback

Actual test results will be saved in `results/interop-checks.txt`.