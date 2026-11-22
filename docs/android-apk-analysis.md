# Android APK analysis: Machines at War 3 v3.1.12

Status: static inspection only, no modified APK executed.

Source APK: user-supplied third-party distribution. Authenticity and safety are not verified.
SHA-256: f068602c66f68af58f2c00fd8f5be0be57995b37f5f3ac27b8978bcfc3ec54af

## Key findings

- APK: 94,899,219 bytes; 493 ZIP entries; ZIP CRC check passed.
- assets/schema.xml: 252,315 bytes. Its schema section contains 180 top-level unit definitions, including resources, stats and actual units.
- It has multiple top-level XML sections. Do not autoformat with a single-root XML formatter.
- Editable-looking unit attributes include Cost, Attack, MaxHealth, Range, Speed, RepeatRate, and BuildTime.
- Example existing Humvee values: Cost=175; Attack=28; MaxHealth=263; Speed=90.
- Other readable XML: players.xml, terrain.xml, terrainobjects.xml, envobjects.xml, gui.xml, campaign.xml, tutorial.xml.
- ARM native library references schema.xml and the message FAILED to load schema.xml, indicating that the native game code likely reads this file.
- Game bundles native SDL2 libraries. This is not a Unity package.
- assets/data.pak: 81,948,274 bytes; proprietary archive. Index parsed successfully: 4,508 assets (2,354 BMP, 1,267 TGA, 573 OGG, 282 JPG, 32 TXT); no XML.
- PAK index begins with uint32 little-endian count (4508) and marker 01. Per-file name bytes are XOR FF with NUL terminator; per-file size/offset are uint32 values XOR FFFFFFFF. All offsets valid; sample bitmap payloads start with BM.
- Repacking the PAK has NOT been tested.
- APK signing certificate self-identifies as Isotope 244 LLC, but a certificate name alone does not authenticate a third-party download.

## First test on Android (MT Manager)

1. Back up APK and saved game data. Do not remove the installed game until backup is secure.
2. Open a copy of the APK, then open assets/schema.xml as text.
3. Find the unit tag whose Name is Humvee; change only Cost="175" to Cost="100" in that tag.
4. Avoid wholesale file reformatting and leave everything else untouched.
5. Save, rebuild and sign a separate test APK. Different signer cannot overwrite the same installed package name; plan installation safely.
6. When installation is safe, try an offline skirmish and check whether the Humvee build cost is 100.

This is an untested proposal, not a verified working mod.

## Future work

- Gameplay balancing and parameters: schema.xml.
- Graphics/audio: custom data.pak unpack/repack tooling, with careful asset compatibility.
- New units: may require ID, class, menu/tech-tree, sprite references and native engine support, not yet verified.

Public repo policy: never upload the original APK, extracted proprietary assets, complete original schema, saves, or signing keys. Store only original tools, notes, and lawful patches.
