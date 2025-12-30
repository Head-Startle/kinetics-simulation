import re


def parse_term(term):
    term = term.strip()
    if not term:
        return None
    # support optional stoichiometric coeff, name, and optional order in parentheses
    # examples: "2.5B(1.5)", "B(2)", "3A"
    m = re.match(r"^(\d*\.?\d+)?\s*([A-Za-z][A-Za-z0-9_]*)\s*(?:\(\s*([0-9]*\.?[0-9]+)\s*\))?$", term)
    if not m:
        raise ValueError(f'Cannot parse term: "{term}"')
    coeff = float(m.group(1)) if m.group(1) else 1.0
    name = m.group(2)
    order = float(m.group(3)) if m.group(3) else None
    return name, coeff, order


def parse_side(side_str):
    if side_str.strip() == '':
        return {}, {}
    parts = [p.strip() for p in side_str.split('+')]
    stoich = {}
    orders = {}
    for p in parts:
        parsed = parse_term(p)
        if parsed is None:
            continue
        name, coeff, order = parsed
        stoich[name] = stoich.get(name, 0.0) + coeff
        if order is not None:
            # if conflicting orders are provided, last one wins
            if name in orders and orders[name] != order:
                print(f'Warning: conflicting orders for {name}, using last: {order}')
            orders[name] = order
    return stoich, orders


def parse_reaction(equation):
    # accept '--' or '->' or '⇌'
    if '--' in equation:
        left, right = equation.split('--', 1)
    elif '->' in equation:
        left, right = equation.split('->', 1)
    elif '⇌' in equation:
        left, right = equation.split('⇌', 1)
    else:
        raise ValueError('Reaction must contain -- or ->: ' + equation)
    react, react_orders = parse_side(left)
    prod, prod_orders = parse_side(right)
    return react, prod, react_orders, prod_orders
