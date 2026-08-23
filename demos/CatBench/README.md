# CatBench

Two prompts, one kitten, many models.

```
SVG    : Create a detailed SVG image of a cute kitten.
Python : Write a Python script that draws a cute kitten using matplotlib.
```

## Submitting a model

Three ways in, easiest first:

1. Open an issue with the CatBench submission form and paste both answers.
2. Open a PR adding the files to `assets/`.
3. Commit straight to `main` if you have write access.

An entry is both prompts: a `.py` and an `.svg` for the same model. Only one of
them and it waits for a human.

Auto-merge covers the boring case only. One model, files sitting directly in
`demos/CatBench/assets/`, nothing existing being changed, `.py` and `.svg` plus
an optional pre-rendered `.png` or `.jpg`. Anything else gets a `needs-review`
label. That isn't a rejection, just the point where a person looks.

Automatic submissions are capped per day (5, shared by the issue and PR paths).
Past the cap they stay open and go through after 00:00 UTC. Change it with the
repo variables `CATBENCH_AUTOMERGE_DAILY_LIMIT` and
`CATBENCH_AUTOMERGE_ENABLED` under Settings > Secrets and variables > Actions >
Variables. Both have working defaults, so there's nothing to set up.

### Why running submitted Python is safe

A submitted `.py` runs exactly once, in a job with a read-only token, no secrets
and no git credentials. The image it produces is committed next to the source,
and `build_catbench_manifest.py` only renders a `<model>.py` when no matching
`<model>-python.<raster>` exists. So the merged script never runs again under
`build.yml`, which does have write access to `main`. Submitted code only ever
runs where there's nothing worth taking.

The import allowlist in `.github/scripts/catbench_validate.py` (matplotlib,
numpy, basic maths) filters out things that aren't kitten drawings. It isn't the
security boundary. The job split above is.

## Filename convention

Drop everything into one folder, kind is detected by extension:

```
CatBench/assets/
  <model>.svg            # paste SVG content directly
  <model>.py             # Python source, auto-rendered by GH Action
  <model>.png|.jpg       # alt: drop a manual screenshot (takes priority over .py rendering)
```

The model name is the filename stem, lower-cased and with spaces/underscores normalised to dashes. `GpT-5.5.svg`, `gpt 5.5.py`, and `GPT_5.5.png` join as the same model `gpt-5.5`.

## Auto-render details

Build pipeline runs each `python/<model>.py` with matplotlib's `Agg` backend (no display, no GUI, just direct PNG output via `plt.savefig`). Scripts that call `plt.show()` instead are handled: `show` is patched to a no-op and the figure is captured at exit. Render failures are recorded in `manifest.json` so the grid can show `⚠ render failed` with a link to the source.

## API

`manifest.json` is the whole gallery, and it is also the API. No key, no rate
limit, CORS open to everyone:

```
https://katehuuh.github.io/demos/CatBench/manifest.json
```

```json
{
  "base": "https://katehuuh.github.io/demos/CatBench/",
  "updated": "2026-08-23T08:18:34Z",
  "models": {
    "kimi-k3": {
      "display_name": "kimi-k3",
      "svg": "assets/kimi-k3-svg.jpg",
      "svg_source": "assets/kimi-k3.svg",
      "python_render": "assets/kimi-k3-python.jpg",
      "python_source": "assets/kimi-k3.py",
      "added": "2026-08-22T21:03:11Z"
    }
  },
  "prompts": { "svg": "...", "python": "..." }
}
```

Paths are relative, join them onto `base`. `svg` and `python_render` are the
pictures the grid shows, always a jpg or gif, so they drop straight into a
Discord embed or a README on the Hub. `svg_source` and `python_source` are what
the model actually wrote. A model missing one of the two prompts has no field
for it.

Keys are newest first, same order as the grid, so the first one is the latest
entry. A key is the name lowercased with spaces and underscores turned into
dashes, so `Qwen3.8-27B-exl3-5.00bpw` becomes `qwen3.8-27b-exl3-5.00bpw`. An
id from the Hub needs its org prefix dropped first.

```bash
# both pictures for one model
curl -s https://katehuuh.github.io/demos/CatBench/manifest.json |
  jq -r --arg m "kimi-k3" '.base + (.models[$m] | .svg, .python_render)'

# every name in the grid
curl -s https://katehuuh.github.io/demos/CatBench/manifest.json | jq -r '.models[].display_name'
```

```js
const id = name.toLowerCase().replace(/[_\s]+/g, '-');
const api = await (await fetch('https://katehuuh.github.io/demos/CatBench/manifest.json')).json();
const hit = api.models[id];
if (hit) send({
  content: `${api.base}?model=${id}`,
  files: [api.base + hit.svg, api.base + hit.python_render],
});
```

`?model=<id>` on the page scrolls to that column and rings it, so the link is
worth posting next to the pictures.

The file is rebuilt by the same Action that builds the grid, so a model shows
up about 30 seconds after its files land on `main`. `updated` is the date of
the newest entry, not of the build, so polling it says whether anything is
actually new.

## Manifest

Regenerated by `.github/scripts/build_catbench_manifest.py`. Don't hand-edit, it'll be overwritten on the next push. Local preview:

```
python ../../.github/scripts/build_catbench_manifest.py
```

(needs `matplotlib` installed for rendering; manifest builds even without it, just renders are skipped.)

## GitHub-web workflow (no local steps required)

The intended flow is to paste files into `CatBench/assets/` directly via the GitHub web UI and let the Action do the rest. On every push:

1. The Action runs `build_catbench_manifest.py`: renders any new `.py`, regenerates `manifest.json`, commits the result back.
2. Pages picks up the new commit and republishes within ~30 seconds.

For SVG and pre-rendered PNG uploads, the page also queries the GitHub Contents API at runtime (`/repos/{owner}/{repo}/contents/CatBench/assets`) and merges anything not yet in the manifest. Result: a freshly pasted SVG appears in the grid as soon as it's committed, without waiting for the Action. The API call is sessionStorage-cached for 30s and falls back silently to the static manifest if rate-limited (anonymous limit is 60/hr per IP).

`.py` files still need the Action to render to PNG, no way around running matplotlib.
