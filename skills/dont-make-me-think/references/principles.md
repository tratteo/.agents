# Krug Principle Catalog

A chapter-by-chapter reference for auditing and building UI against Steve Krug's "Don't Make Me Think". Each section gives the principle, concrete review questions, common violations, and fixes. Use it to name the principle behind each finding. This file explains the theory. For the operational rules go to `rules.md`, for code patterns see `examples.md`, and for the gate see `checklists.md`.

## Table of contents

1. [Don't make me think (Ch. 1)](#1-dont-make-me-think)
2. [How we really use the Web (Ch. 2)](#2-how-we-really-use-the-web)
3. [Billboard Design 101 (Ch. 3)](#3-billboard-design-101)
4. [Mindless choices (Ch. 4)](#4-mindless-choices)
5. [Omit needless words (Ch. 5)](#5-omit-needless-words)
6. [Street signs and breadcrumbs (Ch. 6)](#6-street-signs-and-breadcrumbs)
7. [The home page (Ch. 7)](#7-the-home-page)
8. [Usability debates (Ch. 8)](#8-usability-debates)
9. [Usability testing (Ch. 9)](#9-usability-testing)
10. [Mobile (Ch. 10)](#10-mobile)
11. [Reservoir of goodwill (Ch. 11)](#11-reservoir-of-goodwill)
12. [Accessibility (Ch. 12)](#12-accessibility)
13. [The trunk test](#the-trunk-test)

---

## 1. Don't make me think

**Principle.** A page should be self-evident: the user grasps what it is and how to use it without effort. When a task is inherently complex or novel, aim for self-explanatory instead (a little thought, but no confusion). Self-evidence is the ultimate tie-breaker.

**Review questions.**
- Does any element make the user pause and ask a question ("Huh?", "What is this?", "How do I...?")
- Would a complete stranger know what this page is and what to do next within seconds?
- Are primary actions and important content distinguishable at a glance?
- Is anything labeled with internal jargon, a codename, or a clever-but-unclear phrase?

**Common violations.** Ambiguous primary action; two competing CTAs; icon-only buttons with no label; marketing cleverness ("Solutions", "Empower", "Next-gen") where plain words would work; unexplained acronyms.

**Fixes.** Use plain, specific labels. Give the primary action visual dominance. Add short clarifying text only where thought is unavoidable. Prefer self-evident over self-explanatory.

---

## 2. How we really use the Web

**Principle.** Users scan rather than read, satisfice rather than optimize, and muddle through rather than learn the system.

**Review questions.**
- Would this work if the user only glanced at it for two seconds?
- Is the most likely desired action the most obvious, low-effort path?
- Does anything depend on the user reading instructions, help text, or a manual?
- Does the design punish experimentation, or make trying things safe and reversible?

**Common violations.** Critical information in body paragraphs; important actions buried below the fold; relying on onboarding tooltips to explain core UI; requiring users to "read the docs first".

**Fixes.** Surface the primary path. Use visual cues, not prose. Make destructive actions reversible. Assume nobody reads anything.

---

## 3. Billboard Design 101

**Principle.** Design for scanning, not reading, the way a billboard works at highway speed. Use a clear visual hierarchy, define page areas, make clickable things obviously clickable, keep noise low, and format text for scanning.

**Review questions.**
- **Prominence**: are the most important elements the most visually prominent (size, color, position)?
- **Grouping**: are related things visually grouped, and unrelated things separated?
- **Nesting**: is it clear which elements belong to which others?
- Are page regions (header, nav, main, sidebar, footer) clearly delineated?
- Is it obvious what is clickable, via shape, location, and formatting?
- Is the page free of visual noise that competes with the message?

**Common violations.** Flat hierarchy where everything shouts equally; links that look like plain text; buttons that look like labels; ten "call to actions" competing; decoration and ad-like banners that dilute focus.

**Fixes.** Establish one dominant element per screen. Use white space to group and separate. Follow clickability conventions (color, underline, button shape, cursor, hover/focus states). Cut ornamentation that does not aid comprehension.

---

## 4. Mindless choices

**Principle (Second Law).** The number of clicks matters far less than the certainty of each click. Users tolerate many clicks if each one is painless and clearly moves them toward the goal. Links must give off a strong "scent of information".

**Review questions.**
- Does every link or button name its destination clearly and unambiguously?
- If a user clicks, will they be confident they are on the right track?
- Are options meaningfully distinct, or do several sound the same?
- Is any choice genuinely a coin flip (for example, two similar plan names)?

**Common violations.** Vague link labels ("Learn more", "Click here", "Read more"); menu items that overlap in meaning; navigation that requires trial and error; truncated labels.

**Fixes.** Make labels specific ("See pricing", "Book a demo"). Distinguish options by outcome, not internal structure. Reduce the number of plausible alternatives. Reinforce scent with consistent naming from link to destination.

---

## 5. Omit needless words

**Principle (Third Law).** Get rid of half the words on the page, then get rid of half of what is left. Words that do not earn their place add noise and dilute what matters.

**Review questions.**
- Can this heading, sentence, or label be cut in half without losing meaning?
- Is there **happy talk** (self-congratulatory filler, "Welcome to our award-winning platform")?
- Are there **instructions** the user will never read?
- Can paragraphs become bullets or a single line?
- Do headings act as an outline the user can scan?

**Common violations.** Marketing throat-clearing; duplicated messaging; long empty value statements; "Please note that..." preambles; instructions needed because the UI is unclear (fix the UI instead).

**Fixes.** Delete happy talk. Replace instructions with clearer UI. Use short paragraphs, bulleted lists, and descriptive headings. Front-load the point. Keep long-form, content-driven articles out of scope for this law.

---

## 6. Street signs and breadcrumbs

**Principle.** Navigation must answer the user's constant questions: Where am I? Where should I start? What are the major sections? What are my options here? and How do I get back? Persistent, consistent navigation plus "you are here" cues make this effortless.

**Review questions.**
- Is there persistent navigation on every page?
- Can the user always tell **what site** this is (logo/site ID)?
- Is there a clear **page name**, prominent and matching the link that was clicked?
- Are the **major sections** listed consistently?
- Is there a **"you are here"** indicator (active nav state, highlighted section)?
- Is **search** present and easy to find, when the content volume warrants it?
- Are **breadcrumbs** present in deep hierarchies?

**Common violations.** Navigation that moves or changes per page; page title missing or buried; active section not indicated; no way back to a section index; search hidden in a footer; logo not linked home.

**Fixes.** Freeze navigation structure. Make the page name the largest clear text in the content area. Highlight the current section. Provide breadcrumbs for depth. Repeat navigation at the foot of long pages. Make the logo a home link.

---

## 7. The home page

**Principle.** The home page makes a first impression and answers three questions fast: What is this? What can I do here? Why should I be here and not somewhere else? The first two are mandatory; the third is where value propositions compete.

**Review questions.**
- Does the page clearly say **what this is** and **what I can do** above the fold?
- Is there a **tagline** that explains the value (clear, not clever)?
- Is there a short **welcome blurb** for context?
- Is the main entry point to the product or sign-up obvious?

**Common violations.** A vague slogan instead of a description; hero imagery that communicates nothing; "learn more" mazes; value proposition hidden far below the fold; a tagline that is a riddle.

**Fixes.** State what it is in plain language. Pair a short tagline with a one or two sentence blurb. Put the primary action in the hero. Make the value clear to someone with zero context.

---

## 8. Usability debates

**Principle.** Most arguments about usability are really arguments about taste and cannot be won with opinions. The productive move is to test, and to prefer small accumulated improvements over grand relaunches.

**Review questions (for the skill's own behaviour).**
- Is this disagreement testable, or is it aesthetic?
- Is the proposed fix a single risky overhaul, or a sequence of small safe improvements?
- Are we arguing from internal knowledge rather than observed user behaviour?

**Guidance.** When a claim cannot be resolved by principle or evidence, recommend a quick test with a few users (Ch. 9) rather than escalating the opinion. Suggest shipping small, reversible improvements continuously rather than a big-bang redesign.

---

## 9. Usability testing

**Principle.** Testing is cheap and worth doing regularly. A few users, a few times a month, catches most problems. Focus groups are not usability tests.

**Review questions.**
- Has this been watched with even three to four real users?
- Are we testing representative tasks, not asking for opinions?
- Do the findings feed a regular, lightweight cadence rather than a one-off event?

**Common violations.** Relying on internal opinion or focus groups; testing too late; big, infrequent tests; defending a design instead of observing.

**Fixes.** Recommend a "morning a month" rhythm with three to four participants running realistic tasks. Keep it informal and repeatable. Iterate on the worst problems first.

---

## 10. Mobile

**Principle.** The same usability principles apply, under tighter constraints. Physical affordances, reach, and screen size change the execution, not the fundamentals.

**Review questions.**
- Are tap targets large enough and adequately spaced?
- Is essential content reachable within the natural thumb zone on common phone sizes?
- Does anything rely on hover, which does not exist on touch?
- Do forms use appropriate input types, and does the layout hold up on small screens?
- Is navigation reachable and uncluttered on mobile, not a shrunken desktop nav?

**Common violations.** Tiny tap targets; critical actions at the top corners; hover-only tooltips; cramped multi-column desktop layouts; pinch-to-zoom text; fixed widths causing horizontal scroll.

**Fixes.** Enlarge and space interactive elements. Keep primary actions reachable. Replace hover affordances with click/tap equivalents. Test the small viewport, not just the desktop.

---

## 11. Reservoir of goodwill

**Principle.** Users arrive with a reservoir of goodwill. Good experiences replenish it; annoyances drain it. When it runs out, they leave. Treat the product like a courteous person would.

**Drainers.**
- Hiding information users want (pricing, contact, shipping, limits, status).
- Punishing users for not doing things your way (rigid input formats, forced flows).
- Asking for unnecessary or premature information (signup walls, phone number).
- Forcing users through mazes, interstitials, or dead ends.
- Placing content where it is not expected.
- Making users wait, or work to recover, with no explanation.

**Replenishers.**
- Make the things users most want obvious and easy.
- Tell them what they want to know, up front.
- Save steps wherever possible.
- Make error recovery easy and forgiving.
- Explain and apologize in plain language when something goes wrong.

**Review questions.**
- Is any convenience for the business being paid for out of the user's goodwill?
- Do errors and empty states treat the user as a person, or blame them?
- Is information deliberately withheld that users would obviously want?

**Fixes.** Surface the info users want. Prefill and validate instead of scolding. Ask only for what is needed, when it is needed. Write human error messages that say what happened and what to do next.

---

## 12. Accessibility

**Principle.** Accessibility is part of usability. Fix accessibility problems early, because they are far cheaper to fix during design than to retrofit.

**Review questions.**
- Is the whole interface usable by keyboard alone, with a visible focus indicator?
- Do images and icon buttons have meaningful accessible names?
- Is contrast sufficient for text and meaningful UI?
- Does the structure (headings, landmarks, labels) make sense to a screen reader?
- Are form fields properly labeled and errors announced?

**Common violations.** Divs used as buttons; missing labels; focus outlines removed; color as the only signal; dynamic content that is not announced.

**Fixes.** Use semantic elements. Label controls. Preserve focus styles. Meet contrast requirements. Structure headings logically. Announce important state changes.

---

## The trunk test

A fast way to evaluate navigation and orientation. Imagine a user is dropped onto a random page with no context, then check whether the page answers all of these:

1. **What site is this?** (site ID / logo)
2. **What page am I on?** (page name, prominent)
3. **What are the major sections of this site?** (primary nav)
4. **What are my options at this level?** (local nav or in-page nav)
5. **Where am I in the scheme of things?** ("you are here" cues, breadcrumbs)
6. **How can I search?** (search box, when content volume warrants it)

Any question the page cannot answer is a navigation finding. Use the answers verbatim in the "Trunk test" section of a review.
