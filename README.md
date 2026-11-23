# make-knowlege-cards

An open-source Agent Skill that cuts an article into 5–8 knowledge cards.

## 1. The problem it solves

Long articles are read once and mostly forgotten. The few statements worth
keeping are buried between anecdotes, repetition and transitions, and pulling
them out by hand takes time.

Asking an AI model for "the key points" without further guidance has typical
weaknesses:

- several ideas end up mixed in one point, so none of them sticks
- the number of points is padded to look complete, even when the article is thin
- examples and explanations are invented that the article never contained
- the result is a wall of text that is hard to review or pass on

This skill gives the model fixed rules for exactly these cases, so the result
is a small set of cards that can be read in a few minutes, reviewed later and
shared without the original article.

## 2. Main functions

- **Extracts the important information** from an article the user pastes or
  attaches, and ignores filler.
- **Cuts it into 5–8 cards.** Each card has four parts: title, main knowledge,
  introduction and example.
- **One piece of information per card.** If a card would need a second idea, it
  becomes two cards.
- **Never forces content.** If the article holds fewer than five important
  points, there are fewer cards. A card gets no example or introduction when the
  article gives none. Nothing is added from outside the article.
- **Keeps the article's language** (the HTML labels exist in English, German and
  Chinese).
- **Builds one HTML file** that works offline, adapts to light and dark mode and
  prints cleanly. Markdown is an optional second output.
- **Checks the deck** before building: missing fields stop the build; overlong
  cards, more than eight cards and reused examples produce warnings.

## 3. Installation

The skill is the folder `skills/make-knowlege-cards`. Get it by downloading or
cloning this repository.

### Claude app (web and desktop)

1. Make sure code execution and file creation is enabled in your settings; the
   skill needs it to build the HTML file.
2. Zip the folder so that the ZIP contains `make-knowlege-cards/` as its top
   level, with `SKILL.md` directly inside it.
3. Open **Customize > Skills**, click **+**, choose **Create skill**, then
   **Upload a skill**, and select the ZIP file.
4. Check that the skill is switched on in the list.

Menu names change from time to time. The current steps are in Anthropic's help
article [Use Skills in Claude](https://support.claude.com/en/articles/12512180).

### Claude Code

Copy the folder into one of the skill directories. No ZIP is needed.

| Scope           | macOS / Linux                         | Windows                                           |
|-----------------|---------------------------------------|---------------------------------------------------|
| All projects    | `~/.claude/skills/make-knowlege-cards` | `%USERPROFILE%\.claude\skills\make-knowlege-cards` |
| One project     | `<project>/.claude/skills/make-knowlege-cards` | `<project>\.claude\skills\make-knowlege-cards` |

```bash
# macOS / Linux
cp -r skills/make-knowlege-cards ~/.claude/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse skills\make-knowlege-cards "$env:USERPROFILE\.claude\skills\"
```

### Other agents

Any agent that supports the Agent Skills format (a folder with a `SKILL.md`)
can load the folder as it is.

### Requirements

Python 3.8 or newer for the build script. No additional packages.

## 4. Usage

### With an agent

Paste the article into the chat, or attach it as a file, and ask for cards:

- "Make knowledge cards from this article."
- "Mach aus diesem Artikel Wissenskarten."
- "把这篇文章做成知识卡片。"

The skill is picked up automatically. To be explicit, name it: "Use the
make-knowlege-cards skill on this article."

Options you can state in the same message:

| You say                               | Effect                                              |
|---------------------------------------|-----------------------------------------------------|
| "in English" / "auf Deutsch"          | Cards in that language instead of the article's     |
| "only 4 cards"                        | Your number replaces the 5–8 target                 |
| "also as Markdown"                    | A `.md` file in addition to the HTML                |

You get back one HTML file. Open it in any browser; the Print button prints the
cards two per row.

### The script on its own

The agent writes the cards as JSON and runs the script. You can run it yourself
with any deck file:

```bash
cd skills/make-knowlege-cards
python scripts/build_cards.py examples/spaced-repetition.cards.json -o cards.html
python scripts/build_cards.py examples/spaced-repetition.cards.json -o cards.html --md cards.md
```

| Argument        | Meaning                                         |
|-----------------|-------------------------------------------------|
| `deck`          | Path to the deck JSON file (required)           |
| `-o`, `--output`| HTML output path, default `cards.html`          |
| `--md`          | Also write the deck as Markdown to this path    |

The script exits with code 1 and writes nothing if the deck has errors.

## 5. Input and output example

The complete example is in `skills/make-knowlege-cards/examples/`:

| File                             | What it is                             |
|----------------------------------|----------------------------------------|
| `spaced-repetition.article.md`   | Input: the article (about 400 words)   |
| `spaced-repetition.cards.json`   | The six cards the skill made from it   |
| `spaced-repetition.html`         | Output: the finished deck              |

### Input (excerpt from the article)

> Ebbinghaus also found the remedy. Every time material is reviewed, it is
> forgotten more slowly than before. This is why the same amount of study time
> works better when it is spread out. Four sessions of 15 minutes over two weeks
> leave more in memory than one full hour on the evening before the test.
> Researchers call this the spacing effect. The gaps between sessions can grow
> as the material becomes familiar.

### Intermediate step (one card in the deck JSON)

```json
{
  "title": "Spacing effect",
  "knowledge": "The same amount of study time works better when it is spread over several sessions than when it is spent in one block.",
  "introduction": "Researchers call this the spacing effect. It follows from the fact that each review slows forgetting. The gaps between sessions can grow as the material becomes familiar.",
  "example": "Four sessions of 15 minutes over two weeks leave more in memory than one full hour on the evening before the test."
}
```

### Output (the same card as it appears in the deck)

> **Card 3 / 6**
>
> ### Spacing effect
>
> **Main knowledge:** The same amount of study time works better when it is
> spread over several sessions than when it is spent in one block.
>
> **Introduction:** Researchers call this the spacing effect. It follows from
> the fact that each review slows forgetting. The gaps between sessions can grow
> as the material becomes familiar.
>
> **Example:** Four sessions of 15 minutes over two weeks leave more in memory
> than one full hour on the evening before the test.

The excerpt holds two pieces of information, so the skill made two cards from
it. The second one, "Each review slows forgetting", has no example, because the
article gives none for it:

> **Card 2 / 6**
>
> ### Each review slows forgetting
>
> **Main knowledge:** Every time material is reviewed, it is forgotten more
> slowly than before.
>
> **Introduction:** Ebbinghaus found this remedy in the same experiments that
> produced the forgetting curve. It is the reason why returning to material pays
> off more than learning it once.

All six cards of the example: Forgetting curve, Each review slows forgetting,
Spacing effect, Testing effect, Leitner system, One answer per flashcard.

## Repository layout

```
README.md
LICENSE
skills/
  make-knowlege-cards/
    SKILL.md                    instructions for the agent
    scripts/build_cards.py      JSON deck -> HTML / Markdown
    assets/deck-template.html   HTML template used by the script
    references/card-format.md   field reference and Markdown layout
    examples/                   sample article, its deck and the built HTML
```

## Contributing

Issues and pull requests are welcome. Please keep the script free of
third-party dependencies and run it against the example deck before submitting.

## License

MIT, see [LICENSE](LICENSE).
