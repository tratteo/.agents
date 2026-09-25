# Strict UX/UI Rules

The operational rule set. Each rule states what to do, why it matters, and what a violation looks like. Use it to build and to justify review findings.

## Visual hierarchy and billboard design

**Rule of prominence.** The most important action on a page must be the most visually prominent (size, color, contrast). A screen with no dominant element forces the user to think about where to look.

**Rule of grouping.** Things related logically must be grouped visually, using whitespace, borders, or background cards. Grouping communicates relationship without a word of explanation.

**Rule of nesting.** Visual nesting must show what is part of what. Indentation, containment, and scale tell the user how the hierarchy is organized.

**Rule of clickability.** Buttons and links must look unmistakably clickable. On desktop use hover states; on mobile use standard button shapes and shadows, because there is no hover.

**Rule of noise reduction.** Assume every visual element is noise until proven essential. Remove borders, lines, and colors that do not convey information. Decoration that competes with the message is a defect.

## Navigation and the trunk test

A user dropped into any page of the app must instantly be able to answer:

1. **What site is this?** Site ID or logo, conventionally top left.
2. **What page am I on?** A clear, prominent page H1.
3. **What are the major sections?** Persistent primary navigation.
4. **What are my options at this level?** Local or secondary navigation.
5. **Where am I in the scheme of things?** Active state highlighted in the nav.
6. **How can I search?** A search box, top right or clearly visible, where content volume warrants it.

**Navigation directives.**
- Include breadcrumbs for pages nested three or more levels deep (for example `Settings > User Roles > Edit Admin`).
- Always provide a clear way back to Home or the Dashboard.
- Do not hide primary navigation behind a hamburger on desktop. Hamburger menus are a mobile constraint, not a desktop convenience.
- Keep the page name consistent with the link that brought the user there. A page called "Reports" reached from a link called "Insights" is a question mark.

## Omit needless words (copywriting)

- **Kill happy talk.** Remove introductory fluff, welcome paragraphs, and self-congratulation. "Welcome to the user portal! Here you can..." becomes nothing. The H1 and the interface do the explaining.
- **Kill instructions.** If an interface requires instructions, redesign the interface. If instructions are unavoidable, cut them to the bare minimum.
- **Clear labeling.** A button's text must explicitly state what it does. "Create Project", not "Submit". "Delete User", not "Yes".
- **Front-load the point.** The first words of a heading or label carry the meaning. Users scan the left edge and the first line.

## Buttons, links, and choices

- One primary action per screen. Give it solid, filled, high-contrast treatment.
- Secondary actions are ghost buttons or plain text links. Never present five buttons of equal visual weight.
- Links must be visually distinct from body text (color, underline, or both). Never make a link the same color as body copy.
- Destructive actions use danger styling and name the object: "Delete Database", not "Yes".
- Labels name outcomes. If a user must read the surrounding paragraph to understand a button, the label has failed the mindless choice test.

## Forms and forgiveness

- **No placeholders as labels.** Never rely on the `placeholder` attribute as the only label. It disappears when the user types. Always use a real `<label>` above the input.
- **Forgiving formats.** Accept any reasonable format for phone numbers, credit cards, and dates. Strip spaces and dashes programmatically. Never punish a user for how they type.
- **Immediate validation.** Validate inline on blur, not only on submit. Preserve entered values on error. Never clear a whole form because one field failed.
- **Ask only for what is needed, when it is needed.** Every extra required field is a withdrawal from goodwill and a drop-off risk.
- **Constrain by design, not by scolding.** Prefill, use sensible defaults, and use the right input types (`type="tel"`, `type="email"`, `inputmode="numeric"`) so mobile users get the right keyboard.
- **Group related fields** and keep password or format rules visible and live (a checklist that fills in as the user types) rather than as a post-submit error.

## Errors and recovery

- Errors are human. Say what happened and what to do next: "We couldn't save your project. Try again.", never "Error 500: Null reference".
- Mark the specific offending field and keep everything the user already entered.
- Never dead-end. Offer retry, an alternative path, or a fallback.
- Explain and apologize in plain language when something breaks. Treat the user like a person, not an error code.

## Empty states and onboarding

- Design empty states as guidance, not absence. An icon, a short heading, one line of direction, and the action to start. Never a bare "0 records found".
- Onboarding teaches by letting the user act, using empty states and defaults. It is not a five-step modal walkthrough that nobody reads.
- Make optional onboarding steps first-class skippable. A trapped user is a churned user.
- Move value before commitment. Let the user see the product work before asking for payment, invites, or configuration.

## Dashboards and data tables (SaaS)

**Dashboards.**
- A dashboard must answer "What needs my attention right now?" immediately.
- Lead with high-level metric cards. Use color (red/green/yellow) sparingly, only to denote status or required action, never as decoration.
- Every number is scannable at a glance: large value, small label, clear unit.

**Data tables.**
- Make scanning effortless. Align numbers to the right, text to the left.
- Do not use heavy grid lines. Use subtle zebra striping or light bottom borders.
- Always include bulk actions (row checkboxes) and clear pagination.
- Make column headers explicit and sortable where it helps. Truncate with a tooltip or expandable row, never silently.

## Do's and don'ts

| Category | Do not (the Krug sins) | Do (the Krug virtues) |
| :--- | :--- | :--- |
| **Buttons** | Use generic labels like "Submit", "OK", "Go". | Use action-specific labels like "Create Project", "Delete User". |
| **Forms** | Put labels inside text inputs (placeholders). | Put real labels above the input. |
| **Forms** | Throw an error if a user adds a space in a credit card. | Strip the spaces programmatically behind the scenes. |
| **Forms** | Validate only on submit and clear the form on error. | Validate inline on blur and preserve entered values. |
| **Copy** | Write welcoming paragraphs explaining the page. | Use a clear H1 and get straight to the data and actions. |
| **Nav** | Hide primary navigation under a hamburger on desktop. | Expose primary navigation clearly on desktop. |
| **Choices** | Provide five buttons of equal visual weight. | Provide one solid primary button and the rest as ghost or text links. |
| **Errors** | Show technical jargon: "Error 500: Null reference". | Show human errors: "We couldn't save your project. Try again." |
| **Links** | Make links the same color as body text. | Make links visually distinct (color, underline, or both). |
| **Empty states** | Show a bare "0 Records Found." | Show an icon, a heading, one line of guidance, and a primary action. |
| **Dashboards** | Decorate with color everywhere. | Use color only for status or required action. |
| **Onboarding** | Force a modal tour before the user can act. | Teach through real empty states and defaults. |
| **Destructive** | "Are you sure?" with "Cancel" and "Yes". | "Delete Database?" with "Cancel" and "Delete Database". |
| **Tables** | Heavy grid lines and left-aligned numbers. | Subtle striping, right-aligned numbers, clear pagination. |

## Copywriting punctuation

Do not use em dashes as punctuation. Use commas, colons, semicolons, or parentheses instead. Em dashes are acceptable only inside compound words.
