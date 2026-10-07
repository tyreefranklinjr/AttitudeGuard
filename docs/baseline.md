# Baseline reference

**Verified:** October 6, 2026 · **Name:** reaction-wheel attitude feedback, voltage interface

Both the original and saved example completed without an unhandled exception. Figures were exported and checked for readable curves and labels.

## Launch

```sh
cd ~/AttitudeGuard
source .venv/bin/activate
python sim/baseline/scenarioAttitudeFeedbackRW.py
```

Original launch: `python examples/scenarioAttitudeFeedbackRW.py` from the same directory.
Automatic verification: `python docs/verify_baseline.py`.

## Configuration

| Setting | Verified value |
| :--- | :--- |
| `show_plots` | `True` |
| `useJitterSimple` | `False` |
| `useRWVoltageIO` | `True` |
| Duration | 600 seconds / 10 minutes — script line 403 |
| Dynamics and flight software | Shared task, 0.1-second step — lines 411–412 |
| Stochastic inputs | No seed or noise configured in the example; library defaults not independently audited |
| Python / Basilisk | 3.14.4 / 2.12.0 |
| Platform / compiler | macOS 26.5.1, arm64 / Apple Clang 21.0.0 |

[Full environment record](environment.txt) · [Dependency snapshot](requirements-baseline.txt)

## Active control path

Line references apply to the [saved script](../sim/baseline/scenarioAttitudeFeedbackRW.py).

| Stage | Input → output | Lines |
| :--- | :--- | :--- |
| Navigation | Simulated spacecraft state → attitude and rate | 620 |
| Tracking error | Navigation + inertial reference → guidance error | 621–622 |
| `mrpControl` | Guidance error, inertia, wheel parameters and speeds → body torque | 623–626 |
| `rwMotorTorqueObj` | Body torque + wheel geometry → individual motor torques | 627–628 |
| Voltage conversion | Wheel torques → voltages → applied motor torques, with 0.02 Nm/V interface gain | 630–633; gain at 485 |
| `rwStateEffector` | Motor torque → wheel acceleration and spacecraft reaction torque | 633; attachment at 474 |

The direct-torque connection at line 635 is inactive. Navigation and wheel-speed feedback come from the simulation; the reference, inertia, and wheel parameters are configured by the example.

## Saved evidence

All plots use **time in minutes** on the horizontal axis.

| Figure | Vertical axis |
| :--- | :--- |
| [Attitude error](../results/baseline/attitude-rate.png) | Dimensionless MRP components |
| [Wheel torque](../results/baseline/wheel-response.png) | Requested and applied torque, Nm |
| [Body rate](../results/baseline/body-rate.png) | Rate tracking error, rad/s |
| [Wheel speed](../results/baseline/wheel-speed.png) | RPM |
| [Wheel voltage](../results/baseline/wheel-voltage.png) | V |

[Original run log](../results/baseline/run-original.log) · [Saved-copy run log](../results/baseline/run-copy.log)

The verification script preserves the entry-point flags and uses Matplotlib Agg to export figures at `plt.show()`. Interactive windows were not tested. Earlier `results/Figure_4.png` and `Figure_5.png` remain available.

## Scope and open questions

This verifies the upstream simulation setup. Original quaternion control, sensor-fault detection, and recovery supervision remain future work.

Still unknown: the previous day's exact invocation, original installation procedure, differences from the upstream release, and fresh-machine reproduction. The dependency snapshot records this working environment.

<details>
<summary>Source attribution and exact local paths</summary>

- Author: Autonomous Vehicle Systems Lab, University of Colorado at Boulder. ISC license retained.
- [Upstream example](https://github.com/AVSLab/basilisk/blob/v2.12.0/examples/scenarioAttitudeFeedbackRW.py): attribution only; local source not compared against the release tag.
- Project / working directory: `/Users/tyreefranklinjr/AttitudeGuard`
- Original: `/Users/tyreefranklinjr/AttitudeGuard/examples/scenarioAttitudeFeedbackRW.py`
- Saved copy: `/Users/tyreefranklinjr/AttitudeGuard/sim/baseline/scenarioAttitudeFeedbackRW.py`
- Environment: `/Users/tyreefranklinjr/AttitudeGuard/.venv`
- Interpreter: `/Users/tyreefranklinjr/AttitudeGuard/.venv/bin/python`
- Activation: `source /Users/tyreefranklinjr/AttitudeGuard/.venv/bin/activate`
- Basilisk module: `/Users/tyreefranklinjr/AttitudeGuard/.venv/lib/python3.14/site-packages/Basilisk/__init__.py`
- Both scripts' verified SHA-256: `aed4ac66131236f406aea65636329b97760e34c25b8de0b2e306602cd6574252`

</details>
