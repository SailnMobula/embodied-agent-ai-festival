# From Humanoid Robot to Embodied Agent

Companion site for a 55-minute workshop on how an AI agent controls a real humanoid robot
(AgiBot X2 Ultra), held at the KI Festival.

The site has two jobs: it is the red thread the speaker navigates during the talk, and it is the
reference participants can read on their own afterwards. It is spoken in German and written in
English.

## The five stations

| # | Station | Minutes | Interactive |
| --- | --- | --- | --- |
| 1 | What is an AI agent? | 10 | Clickable state machine |
| 2 | Kinematics | 5 | 2D arm with joint sliders |
| 3 | Cameras and perception | 10 | Live detection (planned) |
| 4 | Skills | 10 | Skill catalogue (planned) |
| 5 | The agent | 20 | Clickable state machine |

## Stack

[Astro](https://astro.build) with [React](https://react.dev) islands and
[Tailwind CSS](https://tailwindcss.com). Content pages ship zero JavaScript; only the two demos
hydrate in the browser.

Styling follows the Exxeta design system — tokens in `src/styles/global.css`, brand rules in
[`.claude/skills/frontend-design/`](.claude/skills/frontend-design/SKILL.md). Sen and Bandeins
Strange are self-hosted from `src/fonts/`.

## Local development

```bash
npm install
npm run dev      # http://localhost:4321/embodied-agent-ai-festival/
npm run build    # static output in dist/
npm run preview  # serve the built output
```

## Project layout

```
src/
  content/stations/   station content as MDX, one file per station
  components/         Astro components and React islands
  layouts/            page shells
  lib/                pure logic: kinematics, state machine, routing
  pages/              overview and the station route
```

Station order, duration and titles live in each MDX file's frontmatter. Adding a station means
adding one file — the timeline, the header navigation and the previous/next pager derive from the
collection.

## Deployment

Pushing to `main` builds the site and publishes it to GitHub Pages via
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). Enable it once under
**Settings → Pages → Source: GitHub Actions**.

The site is served from a subpath, so `base` in `astro.config.mjs` must match the repository name.

## License

[CC BY-SA 4.0](LICENSE) — content and code alike.

Reuse it, remix it, teach it. Credit the source, and anything you build on it stays under the same
license.
