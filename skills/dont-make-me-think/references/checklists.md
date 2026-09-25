# Checklists

The five tests are a hard gate: run them before presenting any output. The other checklists are working aids for review and build modes.

## The five tests (mandatory gate)

If any test fails, refactor the output before presenting it. Do not merely note the failure; fix it.

### 1. The Squint Test
**Question:** If I squint at the UI, does the primary call to action stand out clearly?
**Checks:** Visual hierarchy and prominence. One dominant element per screen.
**Failure looks like:** Everything has similar weight; several buttons compete; the eye does not know where to land.
**Fix:** Enlarge and increase contrast on the primary action; demote everything else to ghost buttons, text links, or smaller type.

### 2. The Trunk Test
**Question:** Does the navigation clearly indicate what this is, where I am, and what my options are?
**Checks:** Site ID, page H1, persistent primary nav, local nav, active state, search.
**Failure looks like:** A bare page with no title, no active nav state, and no route home.
**Fix:** Add the site ID, a prominent page name matching the clicked link, a persistent nav with a highlighted current section, breadcrumbs for depth, and a visible search where warranted.

### 3. The Word Count Test
**Question:** Did I include any paragraph of text? If yes, can I delete it or turn it into a three-bullet list?
**Checks:** Law 3, omitting needless words. Happy talk and instructions removed.
**Failure looks like:** A welcome paragraph, a wall of explanation, or instructions for a self-explanatory interface.
**Fix:** Delete happy talk. Replace instructions by clarifying the UI. Convert any surviving paragraph into a short heading plus up to three bullets.

### 4. The Forgiveness Test
**Question:** If this is a form, is the user protected from being punished for spaces, dashes, or mixed capitalization?
**Checks:** Forgiving input handling, real labels, inline validation, preserved values.
**Failure looks like:** A phone or card field that demands a specific format; placeholder-only labels; a form that clears on error.
**Fix:** Parse input leniently, add real `<label>` elements, validate on blur, and keep entered values on failure.

### 5. The Mindless Choice Test
**Question:** Are the labels explicit enough that the user does not have to read surrounding text to know what a control does?
**Checks:** Action-specific labels, no generic "Submit"/"OK"/"Yes", links that name their destination.
**Failure looks like:** "Submit", "Continue" in a destructive context, "Learn more", or a confirm dialog with "Yes".
**Fix:** Rename every control by its outcome: "Create Project", "Delete Database", "See Pricing".

## Review checklist

Work top to bottom, then map each hit to a principle (see `rules.md` and `principles.md`).

**Orientation**
- [ ] Site ID present and recognizable.
- [ ] Page has a clear, prominent name matching the link that led here.
- [ ] Active section highlighted; breadcrumbs for three-plus levels of depth.
- [ ] A route back to the dashboard or home.
- [ ] Search visible where content volume warrants it.

**Hierarchy and layout**
- [ ] One dominant primary action; no pack of equal-weight buttons.
- [ ] Related elements grouped; unrelated elements separated.
- [ ] Regions clearly delineated (header, nav, main, aside, footer).
- [ ] Noise removed: no borders, lines, or colors that convey nothing.

**Clickability**
- [ ] Buttons look like buttons; links are visually distinct from body text.
- [ ] Hover and focus states exist on desktop; touch targets are large enough on mobile.
- [ ] Every link names its destination.

**Words**
- [ ] No happy talk, no welcome paragraphs.
- [ ] No instructions the interface should not need.
- [ ] No paragraph that could be a heading plus three bullets.
- [ ] Button and link labels name outcomes.

**Forms**
- [ ] Real labels above inputs; no placeholder-only labels.
- [ ] Only necessary fields, asked at the right time.
- [ ] Forgiving formats; right mobile keyboards.
- [ ] Inline validation on blur; values preserved on error; human error messages.

**States and data**
- [ ] Empty states teach and offer an action.
- [ ] Loading and error states are designed, not blank.
- [ ] Tables align numbers right and text left; light dividers; bulk actions and pagination.
- [ ] Dashboards lead with scannable metric cards; status color used sparingly.

**Goodwill**
- [ ] No hidden pricing, costs, or important information.
- [ ] No unnecessary or premature information demands.
- [ ] Error recovery is easy; nothing dead-ends.

## Build (pre-ship) checklist

Run before outputting any generated interface.

- [ ] One primary action, visually dominant, in a consistent position.
- [ ] Real `<label>` elements for every input.
- [ ] Lenient parsing for phone, card, and date inputs.
- [ ] Inline validation on blur, with preserved values and human messages.
- [ ] Action-specific button labels; no generic verbs.
- [ ] Links visually distinct from body copy.
- [ ] Persistent desktop navigation; no desktop hamburger; active state highlighted.
- [ ] Empty states with icon, heading, one line, and an action.
- [ ] Destructive actions named and styled as danger, with a clear confirm.
- [ ] No happy talk, no instructions, no paragraph that should be bullets.
- [ ] Semantic elements, visible focus, keyboard operable, sufficient contrast.
- [ ] All five tests pass.

## Quick code scan

When skimming a diff or a file for Krug violations, look for these fast signals.

| Signal | Likely violation |
| :--- | :--- |
| `placeholder="..."` with no `<label>` | Placeholder used as the only label |
| `>Submit<`, `>OK<`, `>Yes<`, `>Go<` | Generic button label |
| `pattern=` on phone/card/date inputs | Punishing input format |
| `color` same as body text on `<a>` | Link not visually distinct |
| `<button>` count of five or more with equal classes | No visual hierarchy |
| Long `<p>` inside a page header | Happy talk or instructions |
| `0 records` / `No data` alone | Bare empty state |
| `Error \d+` / stack traces in the UI | Technical error message |
| Hamburger visible at desktop breakpoints | Hidden primary navigation on desktop |
| Heavy `border` on table cells | Grid-line noise in data tables |
