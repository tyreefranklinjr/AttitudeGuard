from pathlib import Path
import os, sys, runpy, shutil, subprocess, platform, hashlib, contextlib
root=Path(__file__).resolve().parents[1]
for rel in ['docs','sim/baseline','results/baseline']:
    (root/rel).mkdir(parents=True,exist_ok=True)
os.environ['MPLBACKEND']='Agg'
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'attitudeguard-mpl'))
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
harness_destination = root/'docs/verify_baseline.py'
if Path(__file__).resolve() != harness_destination.resolve():
    shutil.copy2(__file__, harness_destination)
print('PASS: both runs completed; environment, dependency snapshot, figures and logs refreshed. Baseline notes preserved.')
