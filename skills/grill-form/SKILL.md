---
name: grill-form
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
disable-model-invocation: true
---

Resolve links relative to this SKILL.md, including when installed in a plugin cache. When composing questions or explanations, read [writing style](../writing-style/SKILL.md) once
per context. Keep the round format defined below.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't
heard yet. Ask the whole frontier in one round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next
round.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), use an available sub-agent to find it when
delegation is permitted; otherwise investigate it directly. Do not ask the
user for anything you could look up yourself. A running exploration is an unsettled prerequisite: only questions downstream of it wait for the result; ask the rest of the frontier
now. The _decisions_ are the user's: put each to them and wait.

## Deliver each round as an HTML questionnaire

A round is an HTML page the user opens in any browser, not a list of questions in the chat. The page shows every question with its options as checkboxes (several may apply), a
fixed "The question is unclear" option, a free-text box for the user's own answer, and a folded **Context** section for background that would otherwise bloat the question. When
done, the user presses **Generate**; the page shows the answers as Markdown in a selectable text box, and the user pastes that into the chat.

All rendering lives in the bundled `grill.js` next to this SKILL.md. You never write HTML or JavaScript: a round file is this stub with the round JSON filled in, and nothing else.

Per round:

1. Write `.grill/<slug>/round-<NN>.html` under the workspace root (`<slug>` from the topic, `<NN>` zero-padded from `01`). Copy the bundled `grill.js` from this skill directory
   next to the round HTML; use the relative `src` below. Refresh the copy when generating a round.

   ```html
   <!DOCTYPE html>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <script id="grill-data" type="application/json">
   {
     "topic": "SellBot dashboard",
     "slug": "sellbot-dashboard",
     "round": 1,
     "intro": "One short paragraph: what this round settles and what it unblocks. Optional.",
     "questions": [
       {
         "id": "Q1",
         "title": "Who reads the dashboard?",
         "body": "Short question body. Paragraphs split on blank lines; `code`, **bold**, `- ` lists and ``` fences render.",
         "context": "Folded by default. Everything you looked up, the trade-offs, why this decision matters. As long as it needs to be.",
         "options": [
           {"id": "a", "label": "Only me, during the trading day", "detail": "Optional one-line consequence of picking this.", "recommended": true},
           {"id": "b", "label": "The whole desk"}
         ]
       }
     ]
   }
   </script>
   <script src="grill.js"></script>
   ```

   Every question needs at least one concrete option; `recommended: true` marks the answer you would give (usually one, several when the options combine). The "unclear" option
   and the free-text box are added by the page; don't put them in `options`. Question ids stay unique across the whole session (`Q1`… keeps counting across rounds) so later
   rounds can refer back to them. Inside JSON strings write `<\/` instead of `</`, or the browser ends the data block early.

2. In the chat, report only: the clickable link to open (a markdown link with the absolute path, plus the `file://` URL as a fallback; never a relative path), the round number, how
   many questions it holds and what it unblocks. Do not repeat the questions in the chat. Then wait.

3. The user pastes the generated Markdown: one `## Qn — title` section per question with `Selected:`, `The question is unclear` and `Own answer:` lines, or `(no answer)`. Fold
   it into the tree. A free-text answer may settle the question differently from every option: treat it as the decision. "The question is unclear" is your mistake to repair: in
   the next round, ask the same decision again with a rephrased body, richer context and options the user can tell apart. Write the next round at `round-<NN+1>` from the
   recomputed frontier.

Suggest adding `.grill/` to `.gitignore` the first time you create it, unless the user wants the rounds versioned.

If the user asks for chat mode, or no browser can reach the file (remote sessions without file access), fall back to asking the round in the chat with this format:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Close by writing the settled decisions in the chat as a
tree, one line per decision with the round and question that settled it. Do not act on it until the user confirms you have reached a shared understanding.
