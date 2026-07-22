# social-share-cards

Static HTML templates that render 1280×640 GitHub social-preview images for my repos.

## What this is

GitHub lets you set a "social preview" image per repo (Settings → Social preview) that shows up when a repo link is shared on Twitter, LinkedIn, Slack, etc. The default is an auto-generated card that looks the same for everyone. This directory holds hand-built replacements.

Each card is a plain HTML element sized to exactly `1280×640` (the size GitHub expects). You open the file in a browser, screenshot the card node, and upload the PNG to the repo. No build step, no dependencies, no framework — just CSS.

The already-rendered PNGs live in `exports/`.

## Files

| File | What it renders |
|------|-----------------|
| `templates/social-cards.html` | Seven cards on one page: a profile card plus one per project repo |
| `templates/keel-card.html` | A standalone card for the `keel` package (bigger title treatment) |
| `exports/*.png` | The exported 1280×640 images, one per card |

The seven cards in `social-cards.html`:

- **profile** → uploaded on the `sudhanshu1402/sudhanshu1402` profile repo
- distributed-queue-engine
- enterprise-auth-stack
- otel-sdk-node
- multi-region-mongo-patterns
- llm-assessment-pipeline
- system-design-portal

## Design

All cards share one look, defined inline in each file:

- Dark background (`#05070b`) with two soft radial gradients (blue top-right, purple bottom-left).
- A faint 64px grid, masked with a radial gradient so it fades at the edges.
- A vertical purple→blue accent bar on the left.
- Gradient-clipped white→purple heading text.
- Monospace handle line, tech chips, and a footer tagline.

The color palette is a set of CSS variables at the top of each file (`--blue`, `--purple`, `--border`, etc.), so retheming is a one-place edit.

## Exporting a card to PNG

No tooling required. Two ways:

1. **Chrome node screenshot (exact size):** open the HTML file, open DevTools → Elements, select the `.card` element, click the ⋮ menu → "Capture node screenshot". You get an exact 1280×640 PNG.
2. **macOS region grab:** `⌘⇧4`, drag the bordered card bounds.

Then upload it: **repo → Settings → Social preview → Edit → Upload an image**.

The in-page guide at the top of `social-cards.html` repeats these steps.

## Editing a card

Everything is inline HTML/CSS — edit the text in the `<h1>`, `.desc`, `.chips`, and `.foot` blocks. To add a new project card, copy one of the existing `.card` blocks and change the handle, title, description, and chips. Re-export afterward.

## Scope

This is a small personal utility, not a library. There's no generator, CLI, or template engine — the "cards" are literally styled `div`s. If the set of repos grows a lot, converting these into a data-driven generator would make sense; for seven cards, hand-editing HTML is faster.

## License

MIT — see `LICENSE`.
