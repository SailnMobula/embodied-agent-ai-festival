# ki-festival-workshop

Static companion site for a 55-minute workshop on embodied agents, built with Astro, React islands
and Tailwind CSS, deployed to GitHub Pages.

Read [docs/DECISIONS.md](docs/DECISIONS.md) before changing architecture, and
[docs/workshop-brief.md](docs/workshop-brief.md) for the original workshop specification.

## Design

All UI work follows the Exxeta corporate design system. Use these skills for anything touching
colors, typography, spacing, layout or components:

- `frontend-design` — Exxeta brand tokens, the single source of truth (`.claude/skills/`)
- `web-design-guidelines` — accessibility and interface review
- `vercel-react-best-practices` — for the React islands

Non-negotiable brand rules:

- Turquoise (`accent`) is for active controls, focus rings and the current-page indicator only.
  Never for body emphasis, never as a fill.
- Bandeins Strange (`.font-display`) is for headlines only. Body and UI text is Sen.
- Cards are `rounded-card` (16px), pills and buttons `rounded-pill` (24px).

Semantic Tailwind tokens are defined in `src/styles/global.css`: `background`, `foreground`,
`card`, `card-foreground`, `muted-foreground`, `body`, `border`, `border-strong`, `accent`,
`accent-foreground`. Use these, not raw hex.

## Content

Stations are MDX files in `src/content/stations/`. Frontmatter drives the timeline, the header
navigation and the previous/next pager — there is no separate ordering list to keep in sync.

The workshop is delivered in German; everything written is English.

## Code

- Logic goes in `src/lib/` as pure functions with no React import. Components render, they do not
  compute.
- No inline comments. Name things so they do not need one.
- No docstrings tracking project history — that belongs in `docs/DECISIONS.md`.
- Conventional commits, short subject lines, no co-author trailers.
