# parkingcase-ontology-repro

Reproducibility package for the structural steel fabrication case study (CQ1–CQ4).

## Software versions (reproduced)
- Protégé 5.6.7 (HermiT 1.4.3.456)
- Python 3.13.3
- pySHACL 0.30.1
- rdflib 7.5.0
- pyparsing 3.3.2

## Key files
- Ontology schema: `core.owl`
- SHACL shapes: `shapes.ttl`
- Scenario graphs: `instances_baseline.ttl`, `instances_disrupted.ttl`, `instances_rescheduled.ttl`, `instances_policyA.ttl`, `instances_policyB.ttl`
- Scripts: `run_sparql.py`, `compute_table7_kpis.py`
- CQ4 query templates: `CQ4_1_long_members_day.rq`, `CQ4_2_tasks_at_risk_maintenance.rq`, `CQ4_3_infeasible_punchline_with_diag.rq`
- Supplementary procedures: `supplementary/Supplementary_Reproducibility_AEI.docx`

## Quick reproduction (examples)
### SHACL validation (CQ1/CQ2/CQ3)
pySHACL:
- `pyshacl -s shapes.ttl -d instances_disrupted.ttl -f turtle -o report_disrupted_repro.ttl`
- `pyshacl -s shapes.ttl -d instances_rescheduled.ttl -f turtle -o report_rescheduled_repro.ttl`

### CQ4 queries (Figure 13)
- `python run_sparql.py --data instances_baseline.ttl --query CQ4_1_long_members_day.rq > CQ4_1_output.tsv`
- `python run_sparql.py --data instances_disrupted.ttl --query CQ4_2_tasks_at_risk_maintenance.rq > CQ4_2_before.tsv`
- `python run_sparql.py --data instances_rescheduled.ttl --query CQ4_2_tasks_at_risk_maintenance.rq > CQ4_2_after.tsv`
- `python run_sparql.py --data instances_disrupted.ttl report_disrupted_repro.ttl --query CQ4_3_infeasible_punchline_with_diag.rq > CQ4_3_output.tsv`
