# Publishing open science prompts

Skills owns the standalone prompts, audit report template and behavioral
evaluations under `prompts/open-science/`. This website owns explanations,
starter prompts, presentation and its dependency pin. The public entry point
remains the Open Science Assistant resource page.

## Published sources

`data/open-science-source.json` pins the full Skills commit and four SHA-256
checksums. It currently selects [v2026.11](https://github.com/openmodelingfoundation/skills/releases/tag/v2026.11),
resolved to `6d979bae1c590eeaea380f1a2780daab5a8031e6`. The release label is
informational; retrieval always uses that commit, never a moving branch or tag.

The `open-science-resources.html` partial reads the manifest through Hugo data,
retrieves each source, verifies its checksum and publishes the original bytes
through `resources.Copy`. A cached partial shares the resources between the
page's shortcodes within a build. Retrieval is fresh each build. Missing files,
HTTP errors or checksum mismatches fail the build. A 128 KiB content-size check
runs after retrieval; Hugo buffers responses, so it is not a streaming limit.

The existing public paths remain:

- `/prompts/open-science-agent.md`
- `/prompts/open-science-audit-report.md`
- `/prompts/open-science-tutor.md`
- `/prompts/open-science-sandbox.md`

The partial also publishes `/prompts/open-science-source.json`. The resource
page links to that record and the source revision. Resource permalinks support
URL prefixes. There are no maintained `static/prompts/` copies, generated static
mount or Python downloader.

## Local drafts

```sh
make serve PROMPTS_SOURCE=/absolute/path/to/skills
make render-site-isolated PROMPTS_SOURCE=/absolute/path/to/skills
make site-check PROMPTS_SOURCE=/absolute/path/to/skills
```

The optional Compose overlay mounts the checkout's `prompts/open-science/`
read-only as `assets/open-science-local/` and sets `HUGO_OPEN_SCIENCE_LOCAL=1`.
Hugo publishes those assets, computes their actual hashes and labels the source
record `local-preview` without release or commit claims. Drafts may differ
from the release; missing files still fail. Never use this mode for deployment.

Hugo watches the mounted assets. Restart the preview when changing the checkout
path. Local prompts do not require GitHub retrieval; the full site still needs
its other dependencies, including Hugo modules and bibliography tooling.

## Update and verify

1. Review and publish the source changes in Skills with the required authorization.
2. Resolve the release to its full commit. Update `revision`, the descriptive
   `release` label and all four hashes from exact committed bytes.
3. Without `PROMPTS_SOURCE`, run `make content-test`,
   `make render-site-isolated`, `make site-check` and `make html-check`.
   Each render checks published hashes, revision links and bibliography output.
   `site-check` includes `/preview/` deployment. Tests exercise actual Hugo
   partials, including missing sources, warm-cache failures and local drafts.
4. Review the diff before an authorized commit, push or deployment. Older output
   left by a failed build is not a successful deployment artifact.

These are website checks, not behavioral prompt evaluations. See [generated content](generated-content.md)
for bibliography and Awesome policies.
