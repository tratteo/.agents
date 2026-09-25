# Checkout flow: Nimbus Pro (current implementation)

Observed drop-off is about 60% at the payment step. Below is what the user
experiences today, step by step.

## Entry
- User clicks "Upgrade" in the app. A modal opens with no title and no progress
  indicator.

## Step 1: Account
- User is required to create an account to continue. Guest checkout is not
  offered.
- Fields, all required: Full name, Work email, Password, Company name, Job
  title, Phone number, Team size.
- Password rules: "8+ chars, 1 upper, 1 lower, 1 number, 1 symbol, no spaces,
  not one of your last 5 passwords."
- There is a large, colorful "Add coupon code" field at the top of the form.
- Primary button says "Continue". A visually identical button next to it says
  "Cancel".

## Step 2: Plan
- Three cards: "Starter", "Pro", "Pro Plus". The differences are a paragraph of
  small text on each card. "Pro Plus" is highlighted with a "Most popular" badge,
  but "Pro" is preselected.
- Tax and total are not shown yet; the page says "Taxes calculated at checkout".

## Step 3: Payment
- Fields: Card number, Expiry, CVC, Billing address, VAT ID (optional),
  "How did you hear about us?" (required dropdown).
- Shipping cost of $9.99 appears here for the first time, with no explanation.
- If any field is wrong, the form clears all fields and shows a red banner at
  the top reading "Invalid input. Please try again."
- The submit button says "Submit".

## Session behavior
- The modal times out after 5 minutes and closes. All entered data is lost and
  the user is returned to the app with no message.

## Confirmation
- After payment, a plain page reads: "Transaction complete. Reference:
  NMB-2026-00417." No email confirmation is sent. There is no link back to the
  dashboard.
