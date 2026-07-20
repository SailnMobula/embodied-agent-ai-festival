# Decisions

## 1. Astro with React islands instead of hand-written static HTML

`Workshop-Ideas.md` asked for plain HTML/CSS/JS with no build step. We chose Astro anyway.

The site needs two genuinely interactive components (forward kinematics, state machine) and five
content pages that share a layout, a navigation bar and a previous/next pager. Written by hand,
the shared chrome gets copy-pasted five times and the demos become imperative DOM code.

Astro keeps the output static and ships zero JavaScript on content pages — only the two demos
hydrate, and only once scrolled into view. The build step is paid for by GitHub Actions, not by
the audience.

Rejected: Docusaurus (docs-shaped chrome we would spend more time removing than we save), Vite +
React SPA (ships a runtime for pages that are 95% prose).

## 2. Station content as an MDX content collection

Each station is one MDX file with `order`, `title`, `tagline`, `durationMinutes` and `takeaway` in
its frontmatter. The overview timeline, the header navigation and the pager all derive from that
collection.

Consequence: reordering or retiming the workshop is a frontmatter edit, and the schedule can never
drift out of sync between the overview and the stations.

## 3. Interactive logic lives in `src/lib/`, not in the components

`forwardKinematics.ts` and `stateMachine.ts` hold pure functions with no React import. The
components read state and render; they do not compute.

This keeps the geometry and the transition rules testable without a DOM, and it makes the demos
readable to someone who does not know React — which matters, because these files may end up on a
beamer.

## 4. Dual license: CC BY-SA 4.0 for content, AGPL-3.0 for code

The repository holds teaching material and software, and one license fits both badly.

CC BY-SA is the strong-copyleft standard for educational content, but the FSF advises against it
for software. AGPL was chosen over GPL because this artifact is a website: without the network
clause, a modified hosted copy carries no obligation to share anything back.

Rejected: GNU FDL for the content — invariant sections and transparent-copy requirements are a
poor fit for a web page.

## 5. Dark theme, fluid type

The primary display is a beamer in a lit room; the secondary is a laptop after the fact. Type
scales with `clamp()` against the viewport, so the same page is legible in both without a
presentation mode. Colours are defined as `@theme` tokens in `src/styles/global.css`.
