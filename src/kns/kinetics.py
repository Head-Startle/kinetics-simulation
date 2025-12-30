import numpy as np
from pathlib import Path

try:
    from tqdm import tqdm
except Exception:
    tqdm = lambda x: x

from . import parser


def rate_from_side(conc_map, side_stoich_dict, order_dict=None):
    r = 1.0
    for name, stoich in side_stoich_dict.items():
        val = conc_map.get(name, 0.0)
        if order_dict and name in order_dict:
            exponent = order_dict[name]
        else:
            exponent = stoich
        # handle 0^0
        if val == 0.0 and exponent == 0.0:
            factor = 1.0
        else:
            factor = val ** exponent
        r *= factor
    return r


def simulate(control):
    """Run explicit-Euler kinetic simulation.

    Returns: times (np.ndarray), data (2D np.ndarray), species (list), outpath (Path)
    """
    species_list = []
    initial_concs = []
    name_to_idx_map = {}

    for i, s in enumerate(control['species']):
        if isinstance(s, (list, tuple)):
            name = str(s[0])
            init = float(s[1]) if len(s) > 1 else 0.0
            alias = str(s[2]) if len(s) > 2 else None
        else:
            name = s['name']
            init = float(s.get('initial', 0.0))
            alias = s.get('alias')

        if name in name_to_idx_map:
            raise ValueError(f'Duplicate species name: {name}')
        species_list.append(name)
        initial_concs.append(init)
        name_to_idx_map[name] = i
        if alias:
            if alias in name_to_idx_map:
                raise ValueError(f'Duplicate alias: {alias}')
            name_to_idx_map[alias] = i

    species = species_list
    name_to_idx = name_to_idx_map
    conc = np.array(initial_concs, dtype=float)

    # parse reactions
    reactions = []
    for r in control.get('reactions', []):
        if isinstance(r, (list, tuple)):
            eq = r[0]
            kf = float(r[1]) if len(r) > 1 else 0.0
            kb = float(r[2]) if len(r) > 2 else 0.0
        else:
            eq = r['equation']
            kf = float(r.get('kf', 0.0))
            kb = float(r.get('kb', 0.0))

        react, prod, react_orders, prod_orders = parser.parse_reaction(eq)
        for nm in list(react.keys()) + list(prod.keys()):
            if nm not in name_to_idx:
                raise ValueError(f'Species "{nm}" in reaction not defined in species list')
        s_vec = np.zeros(len(species), dtype=float)
        for nm, c in prod.items():
            s_vec[name_to_idx[nm]] += c
        for nm, c in react.items():
            s_vec[name_to_idx[nm]] -= c
        reactions.append({
            'react': react,
            'prod': prod,
            'react_order': react_orders,
            'prod_order': prod_orders,
            'kf': kf,
            'kb': kb,
            's': s_vec
        })

    dt = float(control.get('dt', 0.01))
    steps = int(control.get('steps', 1000))
    outpath = Path(control.get('output', 'ct_output.csv'))

    times = np.zeros(steps + 1)
    data = np.zeros((steps + 1, len(species)))
    times[0] = 0.0
    data[0, :] = conc.copy()

    for step in tqdm(range(1, steps + 1)):
        conc_map = {}
        for i, name in enumerate(species):
            conc_map[name] = conc[i]
        for key, idx in name_to_idx.items():
            conc_map[key] = conc[idx]

        dcdt = np.zeros_like(conc)
        for rx in reactions:
            r_f = rx['kf'] * rate_from_side(conc_map, rx['react'], rx.get('react_order'))
            r_b = rx['kb'] * rate_from_side(conc_map, rx['prod'], rx.get('prod_order'))
            net = r_f - r_b
            dcdt += rx['s'] * net
        conc = conc + dt * dcdt
        conc[conc < 0] = 0.0
        times[step] = times[step - 1] + dt
        data[step, :] = conc

    return times, data, species, outpath
