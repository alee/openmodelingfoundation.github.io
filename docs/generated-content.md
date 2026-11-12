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

Run `make content-test` to test clean/stale workspace preparation and failed
preview startup. Commit, push and deployment require the relevant authorization.
