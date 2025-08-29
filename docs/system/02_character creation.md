# Character Creation (Councillor Creation)

## Overview
Players create a single Councillor to represent their agent in *Space TEM 3*. The Councillor belongs to a faction, has a profession, attributes, traits, and a starting location (Earth). The `/create_councillor` Discord command handles this interactively using select menus and buttons, generating a Councillor object saved to the game database. Resources (e.g., Money, Influence) are tracked per player, aggregated from attributes (if applicable), Traits, and Orgs, and displayed in the character sheet with an income breakdown.

## Mechanics

### Flow
1. **Command Invocation**: Player runs `/create_councillor [name]` (name is unique per player).
2. **Faction Selection**: Bot responds with a select menu (dropdown) listing factions from `factions.json` and a "Select" button. Selection updates the message with the faction description (e.g., "The Initiative: Driven by corporate power..."). Player must click Select to confirm.
3. **Profession Selection**: After faction confirmation, bot updates with a select menu listing core professions from `professions.json`, plus:
   - Profession description (e.g., "Spy: A covert operative skilled in gathering secrets and subterfuge.").
   - Starting missions (e.g., Spy: Investigate, Hostile Takeover).
   - Attribute ranges preview (e.g., Espionage: 6-6).
   - A "Select" button to confirm the profession.
4. **Confirmation**: After profession confirmation, bot shows a preview embed with faction, profession, and name, plus "Create" and "Cancel" buttons. Timeout after 60 seconds.
5. **Generation and Display**: On Create, bot generates attributes and traits, saves the Councillor, and displays a character sheet embed with income breakdown.

### Inputs
- **Command**: `/create_councillor [name]`
  - **Name**: Unique string per player (Discord ID). Duplicates rejected.
- **Interactive**: Faction and profession selected via dropdowns, each confirmed with a Select button.

### Attribute Generation
- Attributes (Persuasion, Investigation, Espionage, Command, Security, Science, Administration) are randomly rolled within the profession’s ranges from `professions.json` (GDD Section 9.3.1).
- Example: For Spy, Espionage is always 6, Persuasion is random between 2 and 6.

### Trait Selection
- One random positive Trait with 0 XP cost from `positive_traits.json` (GDD Section 9.4.1).
- 20% chance for an additional random negative or mixed Trait from `negative_traits.json` or `mixed_traits.json` (GDD Sections 9.4.2, 9.4.3).
- Traits contribute to income (e.g., +20 Money/month from Wealthy) or mission rolls (e.g., +1 Persuasion). Effects displayed in the character sheet with income impact.
- **Future Extension**: Missions may add/remove Traits (e.g., *Public Campaign* failure adding *Pariah*). See `mission_outcomes.json` (TBD).

### Faction Assignment
- Selected via dropdown and confirmed with Select button. One faction per player; no multi-faction support.
- Factions have no starting resource bonuses until defined in balance testing.

### Resource Tracking
- Resources (Money, Influence, Operations, Research, Boost) tracked per player, starting at 0 (or faction-based, pending balance).
- Income calculated as: Base (from attributes, TBD) + Trait bonuses (e.g., +20 Money/month from Wealthy) + Org bonuses (starting 0).
- Displayed in character sheet with breakdown (e.g., Money: 0 base + 20 Wealthy + 0 Orgs = 20/month).
- **Future Extension**: Players can send/receive resources via `/transfer_resource [target_player] [amount] [type]` (e.g., Money). Tracked in the database and updated in sheets.

### Output (Character Sheet)
- A Discord embed displays:
  - Councillor name, faction, profession, Discord username.
  - Attributes (e.g., Persuasion: 4, Investigation: 5).
  - Traits with descriptions and effects (e.g., Beloved: Popular regardless of their loyalties. (+1 Persuasion for Public Campaign, +0 income)).
  - Available Missions: List from profession’s `missions` field (e.g., Investigate, Hostile Takeover).
  - Income Breakdown: For each resource (e.g., Money: 0 base + 20 Wealthy + 0 Orgs = 20/month).
  - Controlled Orgs: Empty (starting value).
- The Councillor object is saved to the database with:
  - `discord_id`: Player’s Discord ID.
  - `character_name`: Chosen name.
  - `faction`: Selected faction.
  - `profession`: Selected profession.
  - `xp`: 0 (starting value).
  - `attributes`: Generated attribute values.
  - `traits`: Selected trait names.
  - `location`: "Earth" (default).
  - `controlled_orgs`: Empty array.
  - `resources`: JSON object with balances (starting 0) and income rates.

### Validation
- Faction and profession must exist in `factions.json` and `professions.json`.
- Name must be unique for the player’s Discord ID.
- One Councillor per player: Command rejected if a Councillor exists for the Discord ID.
- Timeout: Interactive elements (dropdowns, buttons) expire after 60 seconds, canceling the process.

### Example
**Command**: `/create_councillor Jane Doe`  
**Step 1 (Faction Select)**: Embed with dropdown: "Choose a Faction: The Academy, Humanity First..." + Select button.  
**Step 2 (Faction Confirm)**: On Select, embed updates: "The Initiative: Driven by corporate power... Choose a Profession: Spy, Diplomat..." + Select button.  
**Step 3 (Profession Select)**: On Select, embed updates: "Spy: A covert operative skilled in gathering secrets and subterfuge. Missions: Investigate, Hostile Takeover. Attributes: Espionage: 6-6, etc." + Create/Cancel buttons.  
**Step 4 (On Create)**:  
