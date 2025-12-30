#!/usr/bin/env python3
"""simulation.py (main entry)

Lightweight main script that reads a YAML control file, prepares output
directories, calls the simulation kernel in `kinetics.py` and the
interactive plotting in `io_plot.py`.
"""
import sys
from pathlib import Path

try:
    import yaml
except Exception:
    print('PyYAML is required. Install with: pip install pyyaml')
    sys.exit(1)

import csv

from .kinetics import simulate
from .io_plot import interactive_plot


def main():
    # 项目根目录是 src/simulation 的上两级
    project_root = Path(__file__).parent.parent.parent
    dat_dir = project_root / 'dat'
    pic_dir = project_root / 'pic'
    dat_dir.mkdir(exist_ok=True)
    pic_dir.mkdir(exist_ok=True)

    if len(sys.argv) > 2 and sys.argv[1] == '--plot':
        data_path = Path(sys.argv[2])
        if not data_path.exists():
            print('Data file not found:', data_path)
            sys.exit(1)
        print(f'Loading existing data from {data_path}...')
        try:
            import numpy as np
            with open(data_path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)  # ['time', 'A', 'B', ...]
                species = header[1:]   # skip 'time' column
                rows = list(reader)
            times = np.array([float(row[0]) for row in rows])
            data = np.array([[float(val) for val in row[1:]] for row in rows])
            title = Path(data_path).stem
        except Exception as e:
            print(f'Error reading CSV: {e}')
            sys.exit(1)
        interactive_plot(times, data, species, title=title, outdir=pic_dir)
        return

    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else project_root / 'control.yaml'
    if not cfg_path.exists():
        print('Control file not found:', cfg_path)
        sys.exit(1)
    with cfg_path.open('r') as f:
        control = yaml.safe_load(f)

    # ensure output ends with .csv
    outname = control.get('output', 'output')
    if not str(outname).lower().endswith('.csv'):
        outname = str(outname) + '.csv'
    control['output'] = str(dat_dir / Path(outname).name)

    times, data, species, outpath = simulate(control)

    # write CSV
    header = ['time'] + species
    try:
        with open(outpath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in range(len(times)):
                writer.writerow([f'{times[i]:.8g}'] + [f'{v:.8g}' for v in data[i]])
    except Exception as e:
        print('Failed to write CSV:', e)
        sys.exit(1)

    print('Wrote', outpath)
    title = control.get('title') or Path(control['output']).stem
    interactive_plot(times, data, species, title=title, outdir=pic_dir)


if __name__ == '__main__':
    main()
