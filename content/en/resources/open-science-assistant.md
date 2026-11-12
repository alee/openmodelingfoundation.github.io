---
title: "Open Science Assistant"
linkTitle: "Open Science Assistant"
description: "Experimental guidance for auditing research materials, learning open science practices, and running models in a sandbox with an agent."
weight: 40
---

**Experimental guidance · Packaging prompt version 0.11 draft**

The Open Science Research Packaging Assistant helps researchers use an agent to
make research materials understandable, inspectable, reusable, and appropriately
accessible. It guides proportionate audits, documentation, packaging, and
evidence-based verification of data, code, models, and supporting materials.
It prescribes a starting layout for software and datasets, with tooling defaults
for computational work and migration guidance for existing projects.

{{< prompt-links "prompts/open-science-agent.md" "packaging prompt" >}}

Give the prompt URL to your agent, attach the downloaded Markdown, or save it
locally and reference its file path. Start with an audit and review the findings
before requesting changes.

## Start an audit

Copy this starter prompt into your agent:

```text
Read https://www.openmodelingfoundation.org/prompts/open-science-agent.md
and its audit report template at
https://www.openmodelingfoundation.org/prompts/open-science-audit-report.md.
Apply them to this publication or project.

Start with an audit without modifying files. Use the project’s stated
purpose and existing documentation to establish the scope. Identify
the materials supporting its claims or outputs, and gaps affecting
reuse or verification. Cite file paths supporting your findings.
For publications and deposits, also cite URLs and sections or tables.
Check whether the underlying code and data are accessible at permanent URLs,
including materials bundled with code releases or supplements.

Prioritize improvements by their likely benefit and effort. If the
project is too large for a useful initial audit, explain the scope
you recommend and why.

Use the template to separate necessary corrections, optional enhancements
and questions for the authors. If the materials are adequate for the
assessed purpose, say so and explain why; do not invent work to do.

If you cannot retrieve the guidance, tell me before proceeding.
```

## Audit report template

The report template (version 0.11 draft) gives audits a consistent structure:
a purpose-specific verdict, an inventory with permanent code and data links,
an evidence-based assessment, prioritized actions, verification results,
questions for authors or custodians, and a worked example when requested and justified.

{{< prompt-links "prompts/open-science-audit-report.md" "audit report template" >}}

The template accommodates publications, computational models, datasets and
qualitative supporting materials. It distinguishes necessary corrections from
optional enhancements and allows a finding that no change is needed. It is
experimental reporting guidance, not a certification or scoring standard.

## Run a model in a sandbox

The **Computational Model Sandbox Runner (version 0.2 draft)** accepts a model
URL, permanent identifier or local path and treats the model, its installers
and its dependencies as untrusted code. It inspects the materials, identifies
the required inputs and runtime, and attempts a documented example within an
isolated environment with explicit resource limits.

{{< prompt-links "prompts/open-science-sandbox.md" "sandbox execution prompt" >}}

If no usable example exists, the agent works with you to agree on initial
conditions, input data, stopping criteria and a bounded trial before executing
it. If adequate isolation or authorized inputs are unavailable, it explains
what is needed. The run record distinguishes successful execution from
reproducing a publication's results.

This prompt is standalone; the packaging and tutor prompts are not required.
Use an execution environment approved for the model and data. The prompt
specifies agent behavior but does not itself provide or certify a sandbox.

Copy this starter prompt and replace the model reference:

```text
Read https://www.openmodelingfoundation.org/prompts/open-science-sandbox.md
and apply it to this model: [URL, permanent identifier or local path].

Treat the model as untrusted code. Inspect it before executing anything,
identify its input dependencies, and try its smallest documented example
in an appropriate sandbox. Preserve the original code and data.

If no usable example exists or important run conditions or inputs are
unresolved, propose a small safe trial and work with me to agree on those
choices before executing it. Report the actual isolation, resource limits,
commands, inputs, outputs and verification evidence.

If you cannot retrieve the guidance or establish adequate isolation,
tell me before executing the model.
```

## Learn while you work

The **Open Science Practice Tutor (version 0.12 draft)** helps you understand
open science principles as you apply them to your project. Choose a learning
goal and work through examples with questions, hints, demonstrations, or shared
work. The tutor pauses for your attempts and agrees on changes before editing
project files. You can adjust the help or ask the agent to take over a defined
task.

{{< prompt-links "prompts/open-science-tutor.md" "tutor prompt" >}}

The tutor requires the packaging prompt above for shared scientific-integrity
and sensitive-materials guidance. Give your agent both URLs, attach both
Markdown files, or reference both local paths. It must stop if either prompt
is unavailable.

To begin, copy this prompt and add your project or learning goal:

```text
Read https://www.openmodelingfoundation.org/prompts/open-science-tutor.md
and its required companion guidance at
https://www.openmodelingfoundation.org/prompts/open-science-agent.md.

Help me understand open science principles while we apply them to this
project. Start by helping me choose a useful learning task and how we
will share the work. Do not modify project files until we agree on the
changes. If you cannot read either guidance file, tell me and stop.
```

## Source and revision

The [OMF Skills repository](https://github.com/openmodelingfoundation/skills)
maintains the prompts, report template and behavioral evaluations. This website
provides explanations and generates downloads from an explicitly pinned revision.
Report prompt issues in Skills; report presentation or download problems here.

{{< open-science-source >}}

## Scope and responsibility

Researchers remain responsible for scientific decisions, permissions, and review
of proposed changes. Use an environment authorized to receive and process any
sensitive materials; establish authorization before giving the agent access.

These prompts are experimental workflow guidance. They do not establish compliance
with OMF standards or certify scientific validity or reproducibility. For modeling
projects, consult the OMF standards in development for
[Documentation]({{< relref "/standards/documentation" >}}),
[Accessibility]({{< relref "/standards/accessibility" >}}), and
[Reusability]({{< relref "/standards/reusability" >}}).
[OMF Agent Skills](https://github.com/openmodelingfoundation/skills) provide
specialized workflows; OMFA is the modeling methodology assistant.

[Send website feedback](https://github.com/openmodelingfoundation/openmodelingfoundation.github.io/issues/new?projects=openmodelingfoundation/openmodelingfoundation.github.io/6&template=site-wide.md).
Include which prompt you used, its version, and a non-sensitive description of
what helped or needs improvement.
