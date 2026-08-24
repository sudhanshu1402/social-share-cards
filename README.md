# social-share-cards

Static HTML templates that render 1280x640 GitHub social-preview images for my repos.

GitHub shows a social preview card when a repo link is shared on Twitter, LinkedIn, or Slack. The default is auto-generated and looks identical for everyone. These are hand-built replacements: plain HTML sized to exactly 1280x640, no build step, no dependencies, just CSS.

Rendered PNGs are in `exports/`. Two of them:

![Profile card](exports/profile.png)

![keel card](exports/keel.png)

## Files

| File | Renders |
|---|---|
| `templates/social-cards.html` | Eight cards on one page: profile plus one per project repo |
| `templates/keel-card.html` | Standalone card for `keel`, bigger title treatment |
| `exports/*.png` | The exported images |
| `scripts/export-cards.py` | Renders any card to `exports/` in headless Chrome |
| `scripts/check-cards.py` | Checks every export is 1280x640 and matches a declared card |

The eight: profile (goes on `sudhanshu1402/sudhanshu1402`), distributed-queue-engine, enterprise-auth-stack, otel-sdk-node, multi-region-mongo-patterns, llm-assessment-pipeline, system-design-portal, receipts.

## Exporting

```bash
python3 scripts/export-cards.py                  # every card
python3 scripts/export-cards.py otel-sdk-node    # one, by exported filename
```

It pulls each card out of the template, renders it alone in headless Chrome at 1280x640, and writes `exports/<name>.png`. No dependencies beyond Chrome at the standard macOS path. New headless does not always exit after taking the screenshot, so the script waits for the PNG to stop growing and then ends the process itself.

By hand, if you would rather: open the HTML, DevTools, Elements, select the `.card` element, kebab menu, "Capture node screenshot".

Upload at repo Settings, Social preview, Edit.

Stale exports are the failure mode here: the text lives in HTML, the uploaded image does not. After editing a card, re-export it.

## Checking

```bash
python3 scripts/check-cards.py
```

Confirms every PNG in `exports/` is exactly 1280x640, and that the filenames the `.cap` lines declare and the files in `exports/` are the same set. GitHub wants 2:1 and crops anything else, so an off-aspect export loses content. `.github/workflows/cards.yml` runs it on push and pull request. It cannot tell whether an image's text matches its template — that part is on you.

## Editing

Everything is inline HTML and CSS. Edit the `<h1>`, `.desc`, `.chips`, and `.foot` blocks. New card: copy a `.card` block and change the text. Colors are CSS variables at the top of each file, so retheming is a one-place edit.

## Scope

A small personal utility, not a library. No generator, no CLI, no template engine. For eight cards, hand-editing HTML beats building a pipeline. If the repo count grows a lot, data-driven generation would start making sense.

## License

MIT
