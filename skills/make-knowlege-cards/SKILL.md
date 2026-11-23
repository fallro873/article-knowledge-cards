---
name: make-knowlege-cards
description: Cut an article the user pastes or attaches into 5-8 knowledge cards. Each card carries exactly one important piece of information with a title, the main knowledge, an introduction and an example, and the deck is rendered as one self-contained, printable HTML file (optionally also Markdown). Use this skill whenever the user asks for knowledge cards, Wissenskarten, 知识卡片, learning cards or study cards from a text, or wants the key points of an article extracted, condensed or "cut into cards", even if they only paste an article and say "make cards".
license: MIT
---

# Make knowledge cards

Take the article the user copied into the conversation (or attached) and cut it
into 5–8 knowledge cards. A card holds one important piece of information from
the article in a form a reader understands in half a minute without having read
the article.

## What a card contains

| field          | what goes in it                                                                 |
|----------------|---------------------------------------------------------------------------------|
| `title`        | A short name for the piece of information, at most about 60 characters          |
| `knowledge`    | The main knowledge: the one important statement, in one or two full sentences   |
| `introduction` | Two to four sentences that explain it: what it means, why it holds, the context the article gives |
| `example`      | One concrete example from the article that shows the knowledge in use           |

## Workflow

1. **Read the whole article before writing anything.** Cards written while
   reading follow the order of the paragraphs and miss what the article is
   actually about.
2. **Extract the important information.** List every statement a reader should
   keep: findings, rules, causes, definitions, recommendations. Leave out
   anecdotes, repetition, transitions and marketing.
3. **Choose 5–8 of them**, the ones the article itself puts weight on. If two
   candidates say the same thing, merge them; if one candidate contains two
   things, split it.
4. **Write the cards** following the rules below.
5. **Save the deck as JSON and build it:**

   ```bash
   python scripts/build_cards.py cards.json -o cards.html
   python scripts/build_cards.py cards.json -o cards.html --md cards.md   # optional
   ```

   The script uses only the Python standard library. It checks the deck and
   prints warnings; fix what it reports and rebuild.
6. **Check against the article once more:** is every sentence on every card
   supported by the article, and does each card make sense on its own? Then hand
   over `cards.html` and say in one line how many cards there are. If there are
   fewer than five, or some cards have no example, say why in one sentence.

If no code execution is available, write the cards directly in the reply using
the Markdown layout in `references/card-format.md`.

## Rules

**One important piece of information per card.** Cards are read one at a time,
so a second idea on the same card gets skipped. A quick test: if the title
needs an "and", or `knowledge` needs a third sentence, it is two cards.

**Never force content.** This is the rule that matters most, because cards get
passed on without the article and readers take them as fact.

- If the article holds fewer than five important pieces of information, make
  fewer cards. Three solid cards are a correct result; five cards of which two
  are padding are not.
- If the article gives no example for a piece of information, leave `example`
  out. Do not invent one and do not reuse another card's example.
- If the article states something without explaining it, keep `introduction`
  short or leave it out rather than explaining it from general knowledge.
- Add nothing the article does not say: no extra facts, numbers or conclusions.

More than eight important pieces of information: keep the eight that carry the
article and drop the rest, instead of squeezing two into one card. If the user
names a different number of cards, their number wins, but the "never force"
rule still applies.

**Each card stands alone.** Replace "this method" or "the study mentioned above"
with what it is. Explain a term the card depends on in a few words.

**`knowledge` is a statement, not a topic.** "Spaced repetition" is a topic.
"Reviewing at growing intervals keeps material in memory with less total study
time than cramming" is knowledge.

**Keep the article's precision.** Carry over its numbers, names and qualifiers
("in most cases", "in this study") unchanged. Where the article is unsure, the
card is unsure too.

**Write in the language of the article** unless the user asks for another, and
set `lang` to match (`en`, `de`, `zh`, …); the HTML labels follow it.

## Deck format

```json
{
  "title": "Title of the deck, usually the article's title",
  "source": "Author, publication or URL, if the user gave one",
  "lang": "en",
  "cards": [
    {
      "title": "Short name of the piece of information",
      "knowledge": "The one important statement in one or two sentences.",
      "introduction": "Two to four sentences of explanation taken from the article.",
      "example": "One concrete example from the article."
    }
  ]
}
```

Required are `title`, `cards` and, per card, `title` and `knowledge`. Omit
`introduction`, `example` or `source` when the article gives nothing for them;
do not write empty strings or placeholders such as "n/a".

`examples/` contains a sample article, the deck made from it and the built HTML.
