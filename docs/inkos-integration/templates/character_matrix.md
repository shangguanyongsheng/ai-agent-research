# Character Interaction Matrix

This file tracks relationships, interactions, and dynamics between characters in your story.

## Format

Each character has their own section with relationship details to other characters.

```yaml
characters:
  - name: "Character Name"
    description: "Brief description of the character"
    traits: ["trait1", "trait2", "trait3"]
    relationships:
      - with: "Other Character Name"
        type: "relationship type (friend, enemy, family, etc.)"
        status: "current status of relationship"
        history: "key interactions or events that shaped this relationship"
        tension_level: 0-10 # Scale of conflict or harmony
        shared_secrets: ["secret1", "secret2"]
        unresolved_issues: ["issue1", "issue2"]
  
  # Add more characters as needed
```

## Example

```yaml
characters:
  - name: "Alice Chen"
    description: "Protagonist, investigative journalist with a sharp mind"
    traits: ["curious", "determined", "skeptical", "loyal"]
    relationships:
      - with: "Marcus Wei"
        type: "colleague/friend"
        status: "strained but supportive"
        history: "Worked together on the Riverstone case; Marcus saved Alice from danger"
        tension_level: 4
        shared_secrets: ["knowledge of the underground network"]
        unresolved_issues: ["Alice suspects Marcus is hiding information about her father"]
      
      - with: "Dr. Elena Petrov"
        type: "mentor"
        status: "distant but respectful"
        history: "Elena taught Alice investigative techniques at university"
        tension_level: 2
        shared_secrets: []
        unresolved_issues: ["Elena's sudden departure from the university"]
```

## Usage Guidelines

- Update this file whenever significant character interactions occur
- Track changes in relationship dynamics over time
- Note any shifts in trust levels or power dynamics
- Record shared knowledge that could impact future plot points
- Document emotional undercurrents that aren't explicitly stated in dialogue