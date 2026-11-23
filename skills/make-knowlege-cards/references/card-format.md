# Card format reference

## Fields

Deck level:

| field    | required | meaning                                                        |
|----------|----------|----------------------------------------------------------------|
| `title`  | yes      | Title of the deck, shown as page heading                       |
| `source` | no       | Author, publication or URL of the article                      |
| `lang`   | no       | Language code of the cards (`en`, `de`, `zh`, …), default `en` |
| `cards`  | yes      | List of cards; 5–8 is the target, fewer is allowed             |

Card level:

| field          | required | meaning                                         | soft limit      |
|----------------|----------|-------------------------------------------------|-----------------|
| `title`        | yes      | Short name of the piece of information          | 60 characters   |
| `knowledge`    | yes      | The main knowledge in one or two sentences      | 240 characters  |
| `introduction` | no       | Explanation and context from the article        | 500 characters  |
| `example`      | no       | One concrete example from the article           | 400 characters  |

The build script stops on missing required fields, wrong data types and empty
strings. It only warns when a soft limit is exceeded, when a deck has more than
eight cards, and when two cards share the same example.

## Markdown layout

Used by `--md` and for replies when no code execution is available:

```markdown
# Deck title

Source: author, publication or URL

## 1. Card title

**Main knowledge:** The one important statement in one or two sentences.

**Introduction:** Explanation and context from the article.

**Example:** One concrete example from the article.
```

Lines for fields a card does not have are left out. The labels are written in
the language of the deck.
