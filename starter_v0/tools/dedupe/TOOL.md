---
name: dedupe
track: core
kind: local_formatter
requires_env: []
inputs: [items, key]
outputs: [items, item_count, removed_count, skipped_invalid]
side_effect: false
---
# dedupe

Removes duplicate items from a list that was already collected (for example the
combined results of `lookup` and `social_search`). It does not fetch any data.

- `key=url` (default): two items are the same if their URLs point to the same page.
  Scheme, `www.`, `#fragment`, trailing slash, host case and `utm_*` tracking
  params are ignored.
- `key=title`: two items are the same if their titles match ignoring case and
  extra whitespace.
- The first occurrence is kept and the original order is preserved.
- An item with no value for `key` cannot be compared, so it is always kept.
- Entries that are not objects are dropped and counted in `skipped_invalid`.
- Bad input (`key` outside the enum, `items` not a list) returns an error dict
  (`{"tool": "dedupe", "error": ..., "message": ...}`) and never raises.
