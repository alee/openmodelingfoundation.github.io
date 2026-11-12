---
title: "Open Science Assistant"
linkTitle: "Open Science Assistant"
description: "Experimental guidance for learning and applying open science practices with an agent."
weight: 40
---

**Experimental guidance · Version 0.9 draft**

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
and apply its guidance to this project.

Start with an audit without modifying files. Use the project’s stated
purpose and existing documentation to establish the scope. Identify
the materials supporting its claims or outputs, and gaps affecting
reuse or verification. Cite file paths supporting your findings.

Prioritize improvements by their likely benefit and effort. If the
project is too large for a useful initial audit, explain the scope
you recommend and why.

If you cannot retrieve the guidance, tell me before proceeding.
```

## Learn while you work

The **Open Science Practice Tutor (version 0.9 draft)** helps you understand
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

[Send feedback on version 0.9 draft](https://github.com/openmodelingfoundation/openmodelingfoundation.github.io/issues/new?projects=openmodelingfoundation/openmodelingfoundation.github.io/6&template=site-wide.md).
Include which prompt you used, its version, and a non-sensitive description of
what helped or needs improvement.
