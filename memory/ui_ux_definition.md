# UI/UX Definition — hello-counter

> Aligned with `/esencIA/core/UX_UI_POLICY.md`. Produced during Phase 3
> by `architect_agent` (per `BOOTSTRAP_RULES.md §3`).

## Visual Design Direction

Minimum viable UI. The product is a counter; the visual system reflects
that. No branding system, no theming, no custom iconography. One
viewport, one number, one button.

- **Primary color:** single teal (`#1BAFBF`) for the primary action.
- **Background:** light surface (`#F5F7FA`).
- **Typography:** system sans-serif stack (Inter fallback to system).
- **Radii:** 12px.
- **Shadows:** a single soft card shadow for the counter container.

## UX Principles for this project

1. **One primary action.** The `+1` button is the only interactive element.
2. **The number is the signal.** No success toast — the number itself
   changes, and that is the confirmation.
3. **Errors are transient, not blocking.** A network failure surfaces
   a toast with a retry; the page never navigates away or breaks.
4. **Keyboard-first.** The button is reachable with Tab; Space and
   Enter trigger it; focus rings are visible.
5. **Announce changes.** The counter display has `aria-live="polite"`
   so assistive tech announces each increment.

## Component Style System

Three components only. All live in `frontend/app.js` + `frontend/styles.css`.

### `CounterDisplay`
- Centered viewport block.
- Large numeric display (`4rem`), `font-variant-numeric: tabular-nums`.
- Caption underneath: "Counter" (text-secondary color).
- `aria-live="polite"` on the number.

### `PrimaryButton`
- Solid teal background, white text.
- `+1` label.
- Full focus ring on keyboard focus (`outline: 2px solid teal`).
- Disabled state during in-flight request.

### `Toast`
- Fixed position bottom-center.
- Error variant only (red surface, red fg).
- Auto-dismiss after 4s.
- Dismiss button for a11y keyboards.

## Data UI compliance

Per `UX_UI_POLICY.md`:

| Requirement | How this project honors it |
|-------------|----------------------------|
| Decision visually dominant | N/A — this project has no "decision"; the counter is the dominant element instead |
| Confidence visible/secondary | N/A |
| Primary business metric visually dominant | The counter number (4rem) is the primary metric and dominates the page |
| Rationale as structured explanation | N/A — there is no decision to explain |
| Warning states clearly surfaced | The error toast is visible, dismissable, and does not block the counter display |

## Validation

- [x] `architect_agent` defined this during Phase 3.
- [ ] `governance_agent` validates UI quality at go/no-go (to be executed at the first release).
