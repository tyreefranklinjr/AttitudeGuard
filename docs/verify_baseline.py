from pathlib import Path
import os, sys, runpy, shutil, subprocess, platform, hashlib, contextlib
root=Path('/Users/tyreefranklinjr/AttitudeGuard')
for rel in ['docs','sim/baseline','results/baseline']:
    (root/rel).mkdir(parents=True,exist_ok=True)
os.environ['MPLBACKEND']='Agg'
os.environ['MPLCONFIGDIR']='/private/tmp/attitudeguard-mpl'
import matplotlib.pyplot as plt
import Basilisk
original=root/'examples/scenarioAttitudeFeedbackRW.py'
copy=root/'sim/baseline/scenarioAttitudeFeedbackRW.py'
shutil.copy2(original,copy)
def save_figures(*args,**kwargs):
    for number,name in [(1,'attitude-rate.png'),(2,'wheel-response.png'),(3,'body-rate.png'),(4,'wheel-speed.png'),(5,'wheel-voltage.png')]:
        if plt.fignum_exists(number):
            plt.figure(number).savefig(root/'results/baseline'/name,dpi=160,bbox_inches='tight')
plt.show=save_figures
os.chdir(root)
sys.path.insert(0,str(original.parent))
with (root/'results/baseline/run-original.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
    print('Original example:',original)
    print('Working directory:',root)
    print('Entry point flags: True, False, True; Agg rendering with figure export in plt.show')
    runpy.run_path(str(original),run_name='__main__')
    print('PASS: original simulation completed without an unhandled exception.')
with (root/'results/baseline/run-copy.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
    runpy.run_path(str(copy),run_name='__main__')
    print('PASS: preserved baseline completed without an unhandled exception.')
compiler=subprocess.check_output(['clang++','--version'],text=True)
metadata=subprocess.check_output([sys.executable,'-m','pip','show','bsk'],text=True)
pip=subprocess.check_output([sys.executable,'-m','pip','--version'],text=True)
(root/'docs/environment.txt').write_text(f'Verified: 2026-10-06 (America/New_York)\nOS: macOS {platform.mac_ver()[0]}\nArchitecture: {platform.machine()}\nPython: {sys.version}\nEnvironment location: {root}/.venv\nActivation command: source {root}/.venv/bin/activate\nPython interpreter path: {sys.executable}\nBasilisk package location: {Basilisk.__file__}\n\n{pip}\n{metadata}\n{compiler}')
(root/'docs/requirements-baseline.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
(root/'docs/baseline.md').write_text(f'''# AttitudeGuard upstream reaction-wheel baseline

Baseline name: scenarioAttitudeFeedbackRW, voltage interface, no jitter
Date: 2026-10-06 (America/New_York)
Operating system: macOS {platform.mac_ver()[0]}
CPU architecture: {platform.machine()}
Python executable and version: {sys.executable}; {platform.python_version()}
Environment location: {root}/.venv
Environment activation command: `source {root}/.venv/bin/activate`
Basilisk version and module location: 2.12.0; {Basilisk.__file__}
Compiler version: {compiler.splitlines()[0]}
Full metadata: environment.txt. Dependency snapshot: requirements-baseline.txt.

## Source and launch

Upstream attribution: Autonomous Vehicle Systems Lab, University of Colorado at Boulder; ISC license retained in the script.
Upstream example source: https://github.com/AVSLab/basilisk/blob/v2.12.0/examples/scenarioAttitudeFeedbackRW.py (source attribution; local file not compared against this tag).
Original example path: {original}
Saved baseline path: {copy}
SHA-256 (both files): {hashlib.sha256(original.read_bytes()).hexdigest()}
Working directory verified today: {root}
Exact interactive launch command:

```sh
cd {root}
source .venv/bin/activate
python examples/scenarioAttitudeFeedbackRW.py
```

Saved copy launch: `python sim/baseline/scenarioAttitudeFeedbackRW.py` from the same directory with the same environment active.

show_plots: True
useJitterSimple: False
useRWVoltageIO: True
Simulation duration: 10 minutes / 600 seconds (line 403).
Dynamics/flight-software time steps: shared simTask, 0.1 seconds (lines 411–412).
Random seed: no seed or stochastic-input configuration appears in this example; SimpleNav is instantiated without noise configuration. Library-internal defaults were not independently audited.

## Sprint 1 verification

PASS: intended isolated .venv interpreter imports Basilisk; pip belongs to that environment; architecture and versions match the supplied notes.
PASS: original example and preserved copy each completed without an unhandled exception and produced five exported figures. Evidence: ../results/baseline/run-original.log and run-copy.log.
The automatic verification executes each script's actual __main__ entry point with its flags unchanged. It uses Matplotlib Agg and exports figures when plt.show is called, so interactive window display was not tested. The exact verification harness is verify_baseline.py; launch it with `python docs/verify_baseline.py` from the project directory.
Yesterday's working directory, exact command and settings are unknown: today's values are verified from the current script, not terminal history. Existing results/Figure_4.png and Figure_5.png are retained.

## Sprint 2 control path

- SimpleNav receives scObject.scStateOutMsg (line 620), producing simulated navigation attitude/rate. attTrackingError combines that navigation with inertial3D's reference (lines 621–622).
- mrpControl receives attitude/rate guidance error, spacecraft inertia/configuration, wheel geometry/configuration and simulated wheel speeds (lines 623–626). It produces cmdTorqueOutMsg, the requested body control torque. This is the upstream MRP feedback controller.
- rwMotorTorqueObj receives body torque and wheel configuration (lines 627–628). With all three control axes enabled, it allocates the body torque into individual wheel motor torque commands.
- Voltage conversion is enabled. rwMotorVoltage converts requested wheel torques to voltages using wheel parameters (lines 630–631); motorVoltageInterface receives those voltages (line 632), applies configured 0.02 Nm/V gains, and outputs motor torques to rwStateEffector (line 633). The direct torque branch at line 635 is inactive.
- rwFactory.addToSpacecraft attaches rwStateEffector to scObject (line 474). Motor torques accelerate wheels; their coupled angular momentum changes exert reaction torques on spacecraft attitude dynamics.
- Navigation and wheel-speed feedback currently come from the simulated state and upstream modules; inertia, wheel parameters and inertial reference are configured in this example. Original sensor-fault handling is not present.

## Figures

Time axis on each figure: minutes.
- attitude-rate.png: attitude tracking error, dimensionless MRP components (not degrees).
- wheel-response.png: requested/applied wheel motor torque, Nm.
- body-rate.png: rate tracking error, rad/s.
- wheel-speed.png: wheel speed, RPM.
- wheel-voltage.png: wheel voltage, V.

## What this proves and remaining questions

This baseline establishes that the upstream Basilisk simulation runs in my isolated environment and that its voltage-interface reaction-wheel control path produces inspectable results. It does not yet demonstrate my original quaternion controller, sensor-fault detection or recovery supervisor.

Unknown: yesterday's exact invocation; initial installation procedure; local example differences from the upstream release; clean-machine reproduction. The dependency snapshot records this environment, not a verified fresh installation recipe.
''')
harness_destination = root/'docs/verify_baseline.py'
if Path(__file__).resolve() != harness_destination.resolve():
    shutil.copy2(__file__, harness_destination)
print('PASS: both runs completed; environment, configuration, dependency snapshot and figures saved.')
