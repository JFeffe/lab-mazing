# Localization

`Main.gd` and gameplay JSON keep canonical French text and stable identifiers.
`data/en.json` maps French source strings to English. Update this dictionary
when adding any UI text or narrative field. Answers, requirements, object IDs,
coordinates and map references must not be translated.

`Localization.gd` handles exact lookup and longest-first composition for journal
entries, prefixes and item labels. Matching reads the original input once, so
translated fragments are never substituted again in the same pass. Formatted
numeric templates are translated before interpolation. Labels and buttons retain
their source text as metadata so the HUD can refresh immediately.

Journal data remains canonical French for compatibility with existing version 4
saves. Language preference is stored separately in `user://language.cfg`.
`choose_language` refreshes the UI and never reloads the level. Test mode does
not write language preferences. The persistence regression restores the prior
settings file after checking a fresh localization instance.

Run `tests/verify_localization.gd` for coverage, old journal rendering, actual
menu callbacks, unchanged state, dial behavior and preference persistence.
Existing progression tests accept `-- --english` for the English interface.
