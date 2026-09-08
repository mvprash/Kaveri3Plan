# Registration Appeal – Classic Part XII (Secs. 71–77)

Swimlane process diagram for the **classic Registration Act Part XII** refusal / appeal path (not Karnataka Secs. 22-B / 22-C / 22-D).

## Actors (lanes)

| Lane | Actor |
|------|--------|
| Citizen | Presentant / person claiming under the document |
| System | Kaveri workflow, Book 2 recording, notifications, timeline checks |
| Sub-Registrar | Examination, Sec. 71 refusal, registration under order/decree |
| District Registrar | Sec. 72 appeal / Sec. 73 application, Sec. 74 enquiry, Sec. 75 / 76 orders |
| Civil Court | Sec. 77 suit and decree |

## Files

| File | Purpose |
|------|---------|
| `Registration_Appeal_Part_XII.drawio` | Editable diagrams.net swimlane (**open this**) |
| `Registration_Appeal_Part_XII.png` | Exported PNG |
| `Registration_Appeal_Part_XII.mmd` | Mermaid alternative |
| `_generate_part12_appeal_drawio.py` | Regenerator |

## Flow (summary)

1. **Sec. 71** — Sub-Registrar refuses → reasons in **Book 2** → copy to citizen  
2. Branch: **denial of execution?**  
   - **No** → **Sec. 72** appeal to District Registrar (≤ 30 days)  
   - **Yes** → **Sec. 73** application (≤ 30 days) → **Sec. 74** enquiry  
3. District Registrar: **Sec. 75** order to register **or** **Sec. 76** refuse  
4. If ordered: present again ≤ 30 days → register (effect from original presentation date)  
5. If Sec. 76: optional **Sec. 77** civil suit ≤ 30 days → decree may direct registration  

## Open / regenerate

- Open `.drawio` in [diagrams.net](https://app.diagrams.net) or the Draw.io VS Code extension.  
- Regenerate: `python3 _generate_part12_appeal_drawio.py`
