# Few-Shot Examples

Before/after examples for the most common failures. Use them to recognize patterns and to show the user what the fix looks like. Keep code in the project's own idiom; the snippets here are illustrative.

## 1. Eliminating happy talk

**Bad:**
```html
<div class="header">
  <h1>Project Settings</h1>
  <p>Welcome to the project settings page. Here you can change the name of your
     project, update the description, and manage the team members who have access
     to this workspace. Please make sure to click "Save" when you are done!</p>
</div>
```

**Good:**
```html
<div class="header">
  <h1>Project Settings</h1>
  <!-- Happy talk removed. The UI should make the features obvious. -->
</div>
```

Why: the paragraph is happy talk plus instructions. Both are signs the interface should explain itself.

## 2. Unambiguous button copy

**Bad:**
```html
<!-- Modal for deleting a database -->
<h2>Are you sure?</h2>
<p>Do you really want to delete this database? This cannot be undone.</p>
<button class="btn-grey">Cancel</button>
<button class="btn-blue">Yes</button>
```

**Good:**
```html
<!-- Modal for deleting a database -->
<h2>Delete Database?</h2>
<p>This action cannot be undone. All tables and data will be permanently lost.</p>
<button class="btn-ghost">Cancel</button>
<button class="btn-danger">Delete Database</button>
```

Why: the heading states the action, the body states the consequence, and each button names its outcome. No user has to read a sentence to know what "Delete Database" does.

## 3. Forgiving forms and accessible labels

**Bad:**
```jsx
<div className="input-group">
  {/* Fails accessibility, label disappears on type, punishes formatting */}
  <input
    type="text"
    placeholder="Phone Number (e.g. 555-555-5555)"
    pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
  />
  <p className="error">You must include dashes!</p>
</div>
```

**Good:**
```jsx
<div className="input-group">
  <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
    Phone Number
  </label>
  <input
    id="phone"
    type="tel"
    placeholder="555 555 5555"
    className="mt-1 block w-full rounded-md border-gray-300"
    // Parsing and stripping of spaces/dashes happens in onChange.
    // The user is NOT punished for how they type it.
  />
</div>
```

Why: a persistent visible label, the right mobile keyboard, and forgiving parsing. The strict format was the interface's problem, not the user's.

## 4. Empty states that guide

**Bad:**
```html
<div class="table-container">
  <table>{/* headers */}</table>
  <div class="empty">0 Records Found.</div>
</div>
```

**Good:**
```html
<div class="table-container">
  <div class="empty-state text-center p-8">
    <svg class="icon-empty-folder" aria-hidden="true">...</svg>
    <h3 class="text-lg font-medium">No invoices yet</h3>
    <p class="text-sm text-gray-500">Get started by creating your first invoice.</p>
    <button class="mt-4 btn-primary">Create Invoice</button>
  </div>
</div>
```

Why: an empty state is a teaching moment. It says what is missing, what to do, and gives one obvious action.

## 5. Action-specific button labels

**Bad:**
```html
<button>Submit</button>
<button>OK</button>
<button>Go</button>
```

**Good:**
```html
<button>Create Project</button>
<button>Save Changes</button>
<button>View Report</button>
```

Why: "Submit" forces the user to recall what the form was for. The label should name the outcome.

## 6. Primary navigation on desktop

**Bad:**
```html
<header>
  <button class="hamburger" aria-label="Menu">&#9776;</button>
</header>
```

**Good:**
```html
<header class="flex items-center justify-between">
  <a href="/" class="logo">Acme</a>
  <nav class="hidden md:flex gap-6">
    <a href="/dashboard">Dashboard</a>
    <a href="/reports">Reports</a>
    <a href="/settings">Settings</a>
  </nav>
  <input type="search" placeholder="Search" class="hidden md:block" />
</header>
```

Why: primary navigation should be visible on desktop, not hidden a click away. Keep the hamburger for small screens only.

## 7. One dominant action

**Bad:**
```html
<div class="actions">
  <button class="btn">Save</button>
  <button class="btn">Preview</button>
  <button class="btn">Duplicate</button>
  <button class="btn">Archive</button>
  <button class="btn">Delete</button>
</div>
```

**Good:**
```html
<div class="actions flex items-center gap-3">
  <button class="btn-primary">Save Changes</button>
  <button class="btn-ghost">Preview</button>
  <a href="#" class="link">Archive</a>
  <button class="btn-danger-ghost">Delete</button>
</div>
```

Why: equal-weight buttons make every choice feel equally important, which means none is. Establish one primary and demote the rest.

## 8. Human error messages

**Bad:**
```html
<div class="error">Error 500: Null reference exception at line 42.</div>
```

**Good:**
```html
<div class="error" role="alert">
  We couldn't save your project. Check your connection and try again.
  <button class="link">Retry</button>
</div>
```

Why: users cannot act on an error code. Tell them what happened and what to do next, and keep a path forward.

## 9. Distinct links

**Bad:**
```html
<p style="color:#333">
  To manage roles, visit the settings page and open user roles.
</p>
```

**Good:**
```html
<p style="color:#333">
  To manage roles, open <a href="/settings/roles" class="link">User Roles</a>.
</p>
```

Why: a link that looks like body text hides the action. Links need a clear, conventional affordance.

## 10. Scannable dashboard cards

**Bad:**
```html
<div class="dashboard">
  <p>This month your revenue was $42,000 with 1,204 signups and a churn of
     2.1%. Compared to last month, revenue is up, signups are down, and churn
     is slightly worse.</p>
</div>
```

**Good:**
```html
<div class="dashboard grid grid-cols-3 gap-4">
  <div class="metric-card">
    <div class="text-3xl font-semibold">$42,000</div>
    <div class="text-sm text-gray-500">Revenue this month</div>
  </div>
  <div class="metric-card">
    <div class="text-3xl font-semibold">1,204</div>
    <div class="text-sm text-gray-500">Signups this month</div>
  </div>
  <div class="metric-card">
    <div class="text-3xl font-semibold text-yellow-600">2.1%</div>
    <div class="text-sm text-gray-500">Churn, needs attention</div>
  </div>
</div>
```

Why: a dashboard answers "what needs my attention now?" Scannable metric cards beat a paragraph, and status color is reserved for the metric that needs action.

## 11. Data table alignment

**Bad:**
```html
<table class="grid-with-heavy-borders">
  <tr><th>Customer</th><th>Revenue</th><th>Invoices</th></tr>
  <tr><td>Acme</td><td>$1,200</td><td>4</td></tr>
</table>
```

**Good:**
```html
<table class="w-full text-sm">
  <thead class="text-left border-b">
    <tr><th class="py-2">Customer</th><th class="py-2 text-right">Revenue</th><th class="py-2 text-right">Invoices</th></tr>
  </thead>
  <tbody class="divide-y">
    <tr><td class="py-2">Acme</td><td class="py-2 text-right">$1,200</td><td class="py-2 text-right">4</td></tr>
  </tbody>
</table>
```

Why: right-aligned numbers compare at a glance; light dividers reduce noise compared to heavy grid lines.

## 12. Fortifying a destructive confirm

**Bad:**
```html
<h2>Are you sure?</h2>
<p>Do you really want to proceed? This action cannot be undone.</p>
<button>Cancel</button>
<button>Yes</button>
```

**Good:**
```html
<h2>Delete Workspace?</h2>
<p>This permanently deletes "Acme Inc", all projects, and all team access. This cannot be undone.</p>
<button class="btn-ghost">Cancel</button>
<button class="btn-danger">Delete Workspace</button>
```

Why: name the action and the object, show the consequence, and label both buttons by outcome. A generic "Are you sure?" makes the user think.
