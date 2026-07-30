# social-share-cards

Static HTML templates that render 1280x640 GitHub social-preview images for my repos.

GitHub shows a social preview card when a repo link is shared on Twitter, LinkedIn, or Slack. The default is auto-generated and looks identical for everyone. These are hand-built replacements: plain HTML sized to exactly 1280x640, no build step, no dependencies, just CSS.

Rendered PNGs are in `exports/`.

## Files

| File | Renders |
|---|---|
| `templates/social-cards.html` | Seven cards on one page: profile plus one per project repo |
| `templates/keel-card.html` | Standalone card for `keel`, bigger title treatment |
| `exports/*.png` | The exported images |

The seven: profile (goes on `sudhanshu1402/sudhanshu1402`), distributed-queue-engine, enterprise-auth-stack, otel-sdk-node, multi-region-mongo-patterns, llm-assessment-pipeline, system-design-portal.

## Exporting

Open the HTML file, then either:

1. DevTools, Elements, select the `.card` element, kebab menu, "Capture node screenshot". Gives an exact 1280x640 PNG.
2. `Cmd+Shift+4` and drag the card bounds.

Upload at repo Settings, Social preview, Edit.

## Editing

Everything is inline HTML and CSS. Edit the `<h1>`, `.desc`, `.chips`, and `.foot` blocks. New card: copy a `.card` block and change the text. Colors are CSS variables at the top of each file, so retheming is a one-place edit.

## Scope

A small personal utility, not a library. No generator, no CLI, no template engine. For seven cards, hand-editing HTML beats building a pipeline. If the repo count grows a lot, data-driven generation would start making sense.

## License

MIT
