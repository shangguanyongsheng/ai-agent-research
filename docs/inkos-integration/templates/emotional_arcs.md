# Emotional Arcs

Tracks the emotional journey of characters throughout the story.

## Format
Each entry follows this structure:
- character_name: [Character name]
  arcs:
    - arc_id: [Unique identifier for the emotional arc]
      description: [Brief description of the emotional journey]
      start_chapter: [Chapter where arc begins]
      end_chapter: [Chapter where arc concludes or current chapter if ongoing]
      key_moments:
        - chapter: [Chapter number]
          emotion: [Primary emotion]
          trigger: [Event or interaction that caused the emotion]
          intensity: [1-10 scale]
      current_state: [Current emotional state]

## Example
- character_name: Alice
  arcs:
    - arc_id: alice-grief-recovery
      description: Processing grief over loss of mentor and finding new purpose
      start_chapter: 3
      end_chapter: null
      key_moments:
        - chapter: 3
          emotion: despair
          trigger: Discovery of mentor's death
          intensity: 9
        - chapter: 7
          emotion: determination
          trigger: Finding mentor's final message
          intensity: 7
      current_state: cautiously hopeful