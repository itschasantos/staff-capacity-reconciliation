# Staff Capacity Reconciliation

Adapted from existing scheduling reconciliation work. Compares recurring availability with average booked hours by staff and weekday. Positive gaps indicate spare capacity; negative gaps indicate overbooking. This demo covers totals, not time-slot conflicts. The original method divides by weeks with appointments; weeks without appointments are excluded, and availability-only rows form the output. Those limits matter when interpreting results.

## Run

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo.py
```

## Privacy and provenance

The calculation functions were extracted from prior operational projects; the demo and assertions were added for this portfolio. Original records, notebook outputs, credentials, endpoints, branding, and source documents are excluded. All example records are synthetic. Source files remain untouched. No organization performance claims are made.

No license is assigned pending confirmation of rights to redistribute the original work.
