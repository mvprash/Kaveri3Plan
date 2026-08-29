# Document Registration – Online: draw.io Import Procedure

## Reference

This diagram replicates the swimlane process map from:

**`DocumentRegistrationProcessMap.pdf`** (Annexure 2 – MOD 01 Document Registration Process, New Kaveri FRS)

## Diagram structure

The process map uses **4 horizontal swimlanes** (left-to-right flow):

| Lane | Actor | Typical step colours |
|------|-------|----------------------|
| Citizen | Applicant | Yellow (online), Blue (in-office signing) |
| System | Automated system | Green (generation/records), Yellow (status updates) |
| SR | Sub-Registrar | Blue (examination/signing), Green (admission), Yellow (referrals) |
| FDA/SDA | Front-desk assistant | Green (biometrics, printing, filing) |

## Files

| File | Purpose |
|------|---------|
| `Document_Registration_Online.drawio` | Editable swimlane diagram (**open this**) |
| `Document_Registration_Online.mmd` | Mermaid alternative (subgraph swimlanes) |
| `_generate_drawio.py` | Regenerator script |
| `DocumentRegistrationProcessMap.pdf` | Original reference PDF |

## Option A – Open .drawio directly (recommended)

1. Go to [https://app.diagrams.net](https://app.diagrams.net) or use **Draw.io Integration** in Cursor/VS Code.
2. **File → Open from → Device**
3. Select `Document_Registration_Online.drawio`
4. **View → Fit Page** to see all four swimlanes
5. Compare side-by-side with `DocumentRegistrationProcessMap.pdf` and adjust edge routing if needed
6. Export: **File → Export as → PNG / PDF / SVG**

## Option B – Import Mermaid

1. Open [https://app.diagrams.net](https://app.diagrams.net) → blank diagram
2. **Arrange → Insert → Advanced → Mermaid**
3. Paste contents of `Document_Registration_Online.mmd`
4. Click **Insert**, then manually align to match the PDF swimlane layout

## Option C – Regenerate

```powershell
cd "E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\ProcessDiagrams\Document_Registration_Online"
python _generate_drawio.py
```

## Tips for matching the PDF exactly

- The PDF uses landscape layout with lanes stacked vertically; the `.drawio` file follows the same structure.
- Some connectors cross between lanes — drag edge waypoints in draw.io to match the PDF routing.
- Decision diamonds (Valid Application?, Full SD/RF paid?, etc.) are placed in the lane shown in the PDF.
