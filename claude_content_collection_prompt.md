# AIIL Website Content Collection Prompt

Use this prompt with a Claude-based research or writing system when preparing content for the AIIL homepage.

## Goal
Generate fact-based, bilingual website content for a **single-page academic lab homepage** for a **new PI at NPUST**.

The tone must be:
- academically credible
- modest and evidence-based
- clear enough for prospective students
- not written like a SaaS landing page

The site should present the lab as:
- a new research group in progress
- focused on computational biology, veterinary translation, and precision medicine
- currently investing heavily in teaching, a new NSTC project, and careful workflow building

## Critical writing rules
- Do not exaggerate scale, impact, or maturity.
- Distinguish clearly between:
  - current lab focus
  - prior work
  - collaborations
  - planned directions
- If a fact is uncertain, mark it as `[Needs confirmation]`.
- Do not invent awards, metrics, grants, student numbers, course titles, or speaking records.
- If a paper is accepted but not yet published, label it `Accepted` and do not imply it is already in print.
- If a workflow is mainly for internal use, say so directly.
- Keep the tone calm, specific, and academically grounded.

## Required output format
Return the output in Markdown with these sections, and provide **both zh-Hant and English** for every section.

### 1. Hero
Provide:
- one homepage title
- one lead sentence
- one supporting paragraph
- three short proof points

### 2. Current Focus
Provide three short blocks:
- Teaching / course preparation
- NSTC early-career project
- Workflow / computational infrastructure

Each block should include:
- short title
- 120-180 character summary in zh-Hant
- 120-180 word summary in English is too long for homepage, so keep the English summary to 35-60 words

### 3. Research Areas
For each research area, provide:
- short title
- one-sentence short version
- one-sentence expanded version
- 2-4 tags

Current areas to support:
- cross-species transfer learning
- vaccine informatics and protein design
- data-driven drug repurposing
- human-data collaborations and precision medicine

### 4. Selected Work
For each item, provide:
- title
- status / metadata line
- 1-2 sentence factual positioning
- note whether it belongs to current lab output, prior work, or collaboration

Include these content types when information is available:
- NSTC early-career project
- Neurology accepted paper
- NBCT / human data collaboration work
- prior stroke genomics / cancer transcriptomics context

### 5. Teaching
Provide:
- one paragraph on teaching philosophy
- one paragraph on what is currently being adjusted or learned in teaching
- three short points on what students can expect

### 6. Talks / Academic Engagement
If actual talk records are limited, do not fabricate them.
Instead provide:
- one short paragraph describing current seminar or sharing themes
- 3-5 possible seminar themes
- intended audience for each theme

### 7. Join the Lab
Provide:
- who the lab is looking for
- which backgrounds fit well
- what working style is valued
- one short invitation paragraph

## Context to preserve
- The PI is new at NPUST and has been in the role for less than a year.
- The lab should not be framed as a fully mature or large research group.
- Teaching currently takes the largest share of day-to-day effort.
- The newly awarded NSTC project is one of the strongest current anchors.
- Multi-agent workflows are mainly internal research operations support and should not be overstated as publishable research.
- Prior work in human data, stroke genomics, cancer transcriptomics, and real-world data remains important background.

## Final formatting rules
- Use short paragraphs, not hype-heavy bullets.
- Avoid buzzwords unless they correspond to real methods.
- Prefer concrete nouns over abstract branding language.
- Make the Chinese and English versions equivalent in meaning, even if not literal translations.
