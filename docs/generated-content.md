# Generated content and freshness

Supported preview and production commands run in the Compose Hugo service.
Use `make serve` for a preview and `make render-site-isolated` for a disposable
production-style render that does not disturb a running server.

## Bibliography

`assets/bibliographies/publications.bib` is authoritative. The shared
`.github/scripts/prepare-content.sh` regenerates `data/publications.json` in the
active workspace before preview startup and production rendering. The JSON is
ignored and is not baked into the image. Generation occurs after Compose mounts
are applied, so they cannot hide its output. Isolated renders exclude any host
JSON copy and regenerate it in their own workspace.

After editing BibTeX during a live preview, run `make publications-json`; Hugo
will see the changed data. Custom paths remain available through
`PUBLICATIONS_BIB_PATH` and `PUBLICATIONS_JSON_PATH`. A preparation command
failure stops startup/rendering.

The existing parser warns about failed BibTeX blocks and omits them. Inspect
warnings and compare generated records with intended entries; preparation does
not establish that every source entry parsed. Post-render checks verify that
all generated records are displayed and the downloadable BibTeX exactly matches
the maintained source.

## Awesome Modeling Practices

Hugo retrieves upstream `main/README.md` for each build. A cached partial shares
that result within the build; `caches.getresource.maxAge: 0` prevents older
responses being reused across builds. A no-cache header requests upstream
revalidation. Hugo may retry transient failures; this is one logical retrieval
per build, not a promise of one HTTP attempt.

Failed retrieval or invalid publication markers produce a visible warning and
the locally generated bibliography fallback. Older README content is not
silently substituted. Successful pages show "Source fetched for this build";
fallback pages show the page build time without claiming source freshness.
The timestamp does not claim when the upstream author changed the README.
Live-preview rebuilds may retrieve again. This optional source does not block
unrelated pages.

## Open science downloads

Prompts use Hugo retrieval with a full commit pin and required checksums;
retrieval failure blocks the build. See [prompt publication](open-science-prompts.md)
for source ownership and local drafts.

Run `make content-test` for native Hugo publication, cache/fallback and clean or
stale bibliography preparation tests. Commit, push and deployment still require
the relevant authorization.
