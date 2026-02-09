import re
import datetime
import sys
from collections import defaultdict

DT_RE_START = re.compile(r'hasStartTime "([^"]+)"\^\^xsd:dateTime')
DT_RE_FIN   = re.compile(r'hasFinishTime "([^"]+)"\^\^xsd:dateTime')
TASK_HEAD   = re.compile(r'^<https://w3id\.org/sfs/ParkingCase/(T_[^>]+)>\s+a\s+ns1:TaskNode\s*;')
ASSIGNED_RE = re.compile(r'assignedToMachine <([^>]+)>')
COST_RE     = re.compile(r'^<https://w3id\.org/sfs/ParkingCase/(Plasma_[^>]+)>\s+a\s+ns1:PlasmaTableMachine\s*;')
INDEX_RE    = re.compile(r'operationalCostIndex\s+([0-9]+)\s*;')

def parse_dt(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s)

def main(ttl_path: str):
    text = open(ttl_path, "r", encoding="utf-8").read()
    lines = text.splitlines()

    # 1) machine operationalCostIndex
    plasma_index = {}
    current_plasma = None
    for ln in lines:
        m = COST_RE.match(ln.strip())
        if m:
            current_plasma = "https://w3id.org/sfs/ParkingCase/" + m.group(1)
            continue
        if current_plasma:
            m2 = INDEX_RE.search(ln)
            if m2:
                plasma_index[current_plasma] = int(m2.group(1))
            if ln.strip().endswith("."):
                current_plasma = None

    # 2) tasks with start/finish/assigned machine
    tasks = {}
    current_task = None
    for ln in lines:
        mh = TASK_HEAD.match(ln.strip())
        if mh:
            current_task = "https://w3id.org/sfs/ParkingCase/" + mh.group(1)
            tasks[current_task] = {"start": None, "finish": None, "machine": None}
            continue
        if current_task:
            ma = ASSIGNED_RE.search(ln)
            if ma:
                tasks[current_task]["machine"] = ma.group(1)
            ms = DT_RE_START.search(ln)
            if ms:
                tasks[current_task]["start"] = parse_dt(ms.group(1))
            mf = DT_RE_FIN.search(ln)
            if mf:
                tasks[current_task]["finish"] = parse_dt(mf.group(1))
            if ln.strip().endswith("."):
                current_task = None

    # Makespan
    starts = [v["start"] for v in tasks.values() if v["start"] is not None]
    finishes = [v["finish"] for v in tasks.values() if v["finish"] is not None]
    makespan_h = (max(finishes) - min(starts)).total_seconds() / 3600.0

    # Plasma busy time + cost proxy + dominant table
    plasma_busy = 0.0
    per_plasma_busy = defaultdict(float)
    plasma_cost_proxy = 0.0

    for v in tasks.values():
        m = v["machine"]
        if not m or "/Plasma_" not in m:
            continue
        dur_h = (v["finish"] - v["start"]).total_seconds() / 3600.0
        plasma_busy += dur_h
        per_plasma_busy[m] += dur_h
        plasma_cost_proxy += dur_h * plasma_index.get(m, 0)

    dominant = None
    if per_plasma_busy:
        dominant = max(per_plasma_busy.items(), key=lambda x: x[1])[0].split("/")[-1]

    print(f"# file={ttl_path}")
    print(f"Makespan (h)\t{makespan_h:.1f}")
    print(f"Plasma busy time (h)\t{plasma_busy:.1f}")
    print(f"Plasma cost proxy (Σh×index)\t{plasma_cost_proxy:.1f}")
    print(f"Dominant plasma table\t{dominant}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python compute_table7_kpis.py <instances_policyA.ttl|instances_policyB.ttl>")
    main(sys.argv[1])
