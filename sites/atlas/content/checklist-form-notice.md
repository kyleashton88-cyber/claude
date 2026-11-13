---
title: Grid Bot Starter Checklist sign-up notice
slug: checklist-form-notice
category: legal
level: beginner
related:
  - privacy
  - terms
  - disclaimer
last_reviewed: 2026-11-10
status: draft
---

DRAFT: legal wording needs Stewart's sign-off. Entity name and ABN to be confirmed by Stewart against ASIC. The contact email contact@stewartcrowncrypto.com is pending Stewart's confirmation. Not for publishing or deployment. (New file, staged 10 Nov 2026 from Legal Ops review item P13 and the house checkbox wording in FORM_NOTICES_2026-10-26.)

# Checklist sign-up: collection notice, opt-in and unsubscribe

**Why this is a separate file:** the Atlas build on `cursor/atlas-library-buildout` has no checklist sign-up form yet (no `<form>` or email field in any `sites/atlas` page, checked 10 Nov 2026). This is general information and the drop-in copy for whichever page or platform hosts the form. The public address of The Grid Bot Starter Checklist is [CHECKLIST LINK] until Stewart publishes it. It depends on Stewart confirming the checklist funnel (review decision 6).

## Fields

- Name
- Email (required: without it we can't send the checklist)
- Country

## Opt-in checkbox (unticked by default, optional)

> ☐ Yes, send me educational emails and program updates from Market Pros Proprietary Limited. I can unsubscribe anytime.

Rule: the checklist must be sent whether or not the box is ticked. No box ticked = the checklist delivery email only. Never pre-tick the box.

## APP 5 collection notice (under the submit button)

> Market Pros Proprietary Limited (ABN 19 679 270 387) collects your name, email and country so we can send you The Grid Bot Starter Checklist. If you tick the box above, we'll also send you educational emails about grid bots and our programs. Some of our providers store data overseas, including in the US. You can unsubscribe at any time, and ask to access or correct your details at contact@stewartcrowncrypto.com. If you don't give your email, we can't send the checklist. Full details, including how to complain: [PRIVACY_URL].

## Unsubscribe

Every email sent to someone who ticked the box identifies Market Pros Proprietary Limited and has a working unsubscribe link. Opt-outs are actioned within 5 business days (matches privacy.md, review item P6). No emails beyond the checklist delivery to anyone who did not tick the box.

## Reference markup (for the developer; not live)

```html
<!-- DRAFT: legal wording needs Stewart's sign-off. Not for deployment. -->
<form class="checklist-form" action="[FORM_ENDPOINT]" method="post">
  <label for="cl-name">Name</label>
  <input id="cl-name" name="name" type="text" autocomplete="name">
  <label for="cl-email">Email</label>
  <input id="cl-email" name="email" type="email" autocomplete="email" required>
  <label for="cl-country">Country</label>
  <input id="cl-country" name="country" type="text" autocomplete="country-name">
  <div class="checklist-optin">
    <input id="cl-optin" name="marketing_opt_in" type="checkbox" value="yes">
    <label for="cl-optin">Yes, send me educational emails and program updates from Market Pros Proprietary Limited. I can unsubscribe anytime.</label>
  </div>
  <button type="submit">Send me the checklist</button>
  <p class="form-notice">Market Pros Proprietary Limited (ABN 19 679 270 387) collects your name, email and country so we can send you The Grid Bot Starter Checklist. If you tick the box above, we'll also send you educational emails about grid bots and our programs. Some of our providers store data overseas, including in the US. You can unsubscribe at any time, and ask to access or correct your details at contact@stewartcrowncrypto.com. If you don't give your email, we can't send the checklist. Full details, including how to complain: <a href="[PRIVACY_URL]">[PRIVACY_URL]</a>.</p>
</form>
```

The checkbox has no `checked` attribute, so it is unticked by default.
