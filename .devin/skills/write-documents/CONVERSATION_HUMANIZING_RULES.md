# Conversation Humanizing Rules

Rules for writing draft emails, WhatsApp messages, and other text AS the user. Goal: MECT/APAPALAN precision as baseline plus 1-5% humanizing, so drafts match the user's individual writing style and avoid detectable AI patterns.

## Rule Index

Humanizing (HM)
- CV-HM-01: Override Scope - MECT/APAPALAN baseline + 1-5% humanizing for user-voice drafts
- CV-HM-02: Consistency Anchoring - extract and replicate user's writing profile from History
- CV-HM-03: Orthographic Consistency - per-conversation SPELLING_VARIANTS, same word = same spelling
- CV-HM-04: Discourse Markers - include user's discourse markers at observed frequency
- CV-HM-05: Sentence Rhythm - vary sentence length (burstiness), no 3+ similar-length consecutive sentences
- CV-HM-06: Opening/Closing Repertoire - use user's habitual greeting/closing per context, never invent or mechanically rotate
- CV-HM-07: Native Naturalness - drafts in any language read as written by a native speaker, never as translated English

## Anti-Pattern Index

LLM-introduced noise patterns. Each violates a rule above - scan every draft against this list:

- No humanizing applied: no greeting, no voice texture, reads as agent-generated - CV-HM-01
- Over-humanizing: vague times, topics, commitments - CV-HM-01, AP-CM-01
- Humanizing in structural sections (Log, Todos, Status) - CV-HM-01
- Question or call-to-action buried inside a paragraph, unlabeled, or not self-contained ("Sound good?" without context) - AP-CM-02
- Question in own paragraph but missing `Question:`/`Frage:` label prefix ("Does Tuesday work?" instead of "Question: Does Tuesday work?") - AP-CM-02, GLOB-FL-0053
- Bare period reference ("Q2", "next quarter") without year - AP-CM-03
- Locale date formats ("March 24", "24.3."), missing weekday or timezone - CV-DT-01, AP-CM-03
- Wrong timezone abbreviation: CET in summer (should be CEST) or CEST in winter (should be CET) - AP-CM-03, GLOB-FL-0054
- Vague commitment without deliverable and timing - AP-CM-01
- Ignoring the user's extracted profile, or extracting without applying - CV-HM-02
- Randomized spelling variants between or within drafts - CV-HM-03
- Zero discourse markers, forced marker stuffing, or wrong register - CV-HM-04
- Uniform sentence lengths or artificial choppiness - CV-HM-05
- Dropped subject pronouns or articles in full sentences (telegram style) - CV-HM-01, CV-HM-07
- Impersonal event descriptions: AI describes what happened ("Discussed X for an hour"), humans describe what THEY did ("We discussed X for about an hour") - CV-HM-07
- Invented greetings/closings or mechanical per-draft rotation - CV-HM-06
- Translated-English phrasing (translationese) - CV-HM-07
- High-frequency LLM vocabulary, formal connectives in casual context - Vocabulary Avoidance, Connective Register

## Override Scope

When writing AS the user (draft emails, WhatsApp replies, messages to third parties), apply Minimal Explicit Consistent Terminology (MECT) and As Precise As Possible, As Little As Necessary (APAPALAN) as baseline. Add 1-5% humanizing (CV-HM-02 through CV-HM-06): greeting/closing, occasional discourse marker or hedge, natural sentence rhythm.

**NEVER sacrifice clarity, disambiguation, explicit intent, or structure for humanization.** Humanizing ADDS style - it never dilutes effectiveness.

**Complete natural grammar in drafts** (CV-HM-07): keep subject pronouns and articles - "I had a look at the contract", never "Had a look at contract". People like to talk about themselves; dropping pronouns and articles reads robotic. APAPALAN brevity rule AP-BR-02 (sacrifice grammar) applies to agent documents, NEVER to user-voice drafts. Fragments are allowed only as reactions and follow-ups (CV-HM-05).

Structural sections (Log, Context, Links, Todos, Status, MNF) remain pure MECT/APAPALAN with zero humanizing.

**Precision survives humanizing**: accountable commitments (AP-CM-01), labeled self-contained asks in own paragraphs (AP-CM-02), and time precision with weekday + ISO date + timezone (AP-CM-03) apply to every draft in every language. Humanizing never weakens them. Write "Tuesday, 2026-03-24 14:00 CET", never "Tuesday-ish" - unless the user's intent is genuinely undecided.

**BAD** (pure MECT, no humanizing - reads as machine-generated):
```
Subject: Re: Meeting

Confirmed. Tuesday, 2026-03-24 14:00 CET. Agenda: Q2 2026 review, budget allocation, hiring timeline.
```

**BAD** (over-humanized, precision lost):
```
Subject: Re: Meeting

Hi Sarah,

yeah so I was thinking we could maybe do Tuesday around 2ish? I mean we should
probably talk about the Q2 stuff and you know the budget thing and all that.
Let me know!

Best,
Max
```
Precision lost: no date (which Tuesday?), vague time ("around 2ish"), vague topics ("Q2 stuff", "budget thing"), vague call-to-action ("Let me know!"), question buried inside paragraph.

**GOOD** (MECT/APAPALAN baseline + 1-5% humanizing):
```
Subject: Re: Meeting

Hi Sarah,

sounds good, let's do Tuesday, 2026-03-24 14:00 CET. I think we should focus
on the Q2 2026 numbers, but we can also cover budget and hiring if there's time.

Question: Anything else you want on the agenda?

Best,
Max
```

**BAD** (humanizing bleeding into structural sections):
```
## Log
- well, we basically talked about the Q2 2026 timeline on 2026-03-17
```

**GOOD** (MECT/APAPALAN for structural sections):
```
## Log
- **2026-03-17 14:30** - Discussed Q2 2026 timeline adjustments
  - Decision: Move milestone 2 to Wednesday, 2026-04-15
```

## Consistency Anchoring

On first draft for a conversation, analyze the user's prior messages in History. Extract and replicate:

1. **Sentence length distribution** - ratio of short (1-10 words), medium (11-20), long (21+)
2. **Greeting/closing patterns** - exact forms used, including punctuation and capitalization
3. **Punctuation habits** - comma frequency, dash style (-- vs -), exclamation marks, ellipsis usage
4. **Discourse marker preferences** - which markers, which positions (sentence-initial, mid-sentence)
5. **Habitual phrases** - recurring word sequences (e.g., "sounds good", "let me know", "ich denke mal")

Store extracted profile in the Humanizing Settings section of the conversation file. Subsequent drafts MUST conform to this profile.

**BAD** (ignoring user's established style):
```
History shows user writes: "Hi Thomas, kurze Frage - ..."
Draft produces: "Dear Thomas, I would like to inquire about ..."
```

**BAD** (analyzing but not applying):
```
User consistently writes short sentences (8-12 words avg).
Draft produces 25-word compound sentences.
```

**GOOD** (style replicated from History):
```
History shows user writes:
- "Hi Thomas," (greeting)
- short sentences, avg 10 words
- uses "kurze Frage" as opener
- closes with "LG" or "Beste Grüße"

Draft:
Hi Thomas,

kurze Frage - hast du die Rechnung RE-2026-0142 schon überwiesen?

Ich hab noch nichts auf dem Konto gesehen.

LG
Max
```

**Insufficient History**: If fewer than 3 prior user messages exist in History, skip anchoring and apply only CV-HM-04 through CV-HM-06 with default settings. Note `ANCHORING: INSUFFICIENT_HISTORY` in the draft.

## Orthographic Consistency

Maintain a per-conversation SPELLING_VARIANTS list in Humanizing Settings. Same word = same variant every time. Never randomize.

Applies to:
- Regional orthographic variants (German ß/ss, Brazilian/European Portuguese fato/facto, British/American colour/color)
- Spelling reform variants (French connaître/connaitre)
- Informal abbreviations (u/you, thx/thanks)
- Punctuation conventions (... vs .., ! vs !!)

**BAD** (inconsistent ß/ss within same draft):
```
Vielen Dank für die Rückmeldung. Das weiß ich zu schätzen.
Ich schicke die Grüsse später.
```
"weiß" uses ß but "Grüsse" uses ss. Same draft must use same convention.

**BAD** (randomized between drafts):
```
Draft 1: "weiß", "Straße", "Grüße"
Draft 2: "weiss", "Strasse", "Grüsse"
```

**GOOD** (consistent per SPELLING_VARIANTS):
```
SPELLING_VARIANTS: [ß_PREFER: weiß, Straße, Grüße, müssen]

Draft 1: "weiß", "Grüße"
Draft 2: "weiß", "Grüße"
Draft 3: "weiß", "Grüße"
```

**Extraction rule**: On first draft, scan user's prior messages for spelling patterns. If the user writes "Grüsse" (Swiss ss) vs "Grüße" (standard ß), record the preference. If no prior messages exist, use standard orthography and update SPELLING_VARIANTS when the user corrects a draft.

## Discourse Markers

Include the user's discourse markers at their observed frequency. Discourse markers signal informal register and thinking-in-progress - their absence is a top-5 Large Language Model (LLM) detection signal.

Draw from the user's established set. If no prior messages exist, use 1-2 markers per draft from the language-appropriate default set.

Default marker sets by language (use only as fallback):
- **English**: well, actually, basically, I mean, you know, right, so, anyway
- **German**: na ja, halt, eigentlich, also, sozusagen, naja, quasi
- **Spanish**: bueno, pues, la verdad, o sea, es que, en fin, vamos
- **French**: bon, enfin, en fait, du coup, bref, donc, voilà
- **Portuguese**: bom, na verdade, tipo, enfim, aliás, pois é

**Hedges and qualifiers** (same function as discourse markers - soften declarative statements):
- **English**: I think, probably, not sure but, might be, I guess, kind of, seems like, though
- **German**: denke ich, vielleicht, glaube ich, wahrscheinlich, bin mir nicht sicher aber, irgendwie
- **Spanish**: creo que, probablemente, quizás, no estoy seguro pero, me parece que
- **French**: je pense que, probablement, peut-être, je ne suis pas sûr mais, il me semble
- **Portuguese**: acho que, provavelmente, talvez, não tenho certeza mas, me parece que

LLMs produce declarative statements; humans hedge. "The terms are acceptable" reads as AI. "I think the terms are fine, though I'd want to double-check the payment bit" reads as human.

**BAD** (no discourse markers in casual email):
```
I reviewed the contract. The terms are acceptable. I will sign tomorrow.
```

**BAD** (too many markers, forced):
```
Well, actually, I basically reviewed the contract, you know, and I mean
the terms are, well, basically acceptable. So anyway I'll sign tomorrow.
```

**BAD** (wrong register - formal markers in casual context):
```
Furthermore, upon reviewing the contract, I find the terms to be acceptable.
Consequently, I intend to sign tomorrow.
```

**GOOD** (natural frequency, matches user profile):
```
I had a look at the contract - actually the terms are fine.

I'll send it back signed tomorrow (Friday, 2026-07-17).
```

**GOOD** (German, natural frequency):
```
Ich hab mir den Vertrag angeschaut und denke, die Konditionen passen so.

Ich schicke den Vertrag dann morgen (Freitag, 2026-07-17) unterschrieben zurück.
```

**GOOD** (Spanish, natural frequency):
```
Le eché un vistazo al contrato, la verdad las condiciones están bien.

Te lo mando firmado mañana (viernes, 2026-07-17).
```

**Tracking**: Record observed markers in DISCOURSE_MARKERS variable. Format: `[marker1, marker2, marker3 | approx_frequency: N per message]`

## Sentence Rhythm

Vary sentence length within each draft. Human writing has high "burstiness" - alternating between short emphatic statements and longer flowing sentences. LLM output has uniform sentence lengths, which is a primary detection signal.

Rules:
- No 3+ consecutive sentences of similar word count (within 5 words of each other)
- Mix fragments (1-3 words), short (4-10 words), medium (11-20 words), and long (21-35 words) sentences
- Use fragments for reactions, confirmations, and follow-ups: "Sounds good.", "Passt.", "Will do.", "Geht klar.", "Not sure yet."
- Questions and calls-to-action in own paragraphs, labeled (Question:/Request:), fully self-contained (AP-CM-02)
- Match the user's observed burstiness profile from History

**BAD** (uniform sentence length - AI pattern):
```
I reviewed the contract terms yesterday afternoon. The payment schedule
looks reasonable and fair to me. I think we should proceed with the signing.
The deadline for the first payment is next month. Please confirm when you
are available to meet and discuss.
```
Five sentences, all 8-12 words. Monotonic rhythm.

**BAD** (artificially choppy, dropped pronouns and articles):
```
Contract. Reviewed. Terms fine. Sign tomorrow. Done.
```

**GOOD** (natural burstiness, question and commitment in own paragraphs):
```
I had a look at the contract. The payment schedule works - first installment
would be next month (August 2026), then quarterly. Which gives us enough room.

Question: I'd like to push the first appointment out by two weeks. Does that work?

I'll send the contract back signed tomorrow (Friday, 2026-07-17).
```
6 sentences: 7, 14, 5, 11, 3, 9 words. Natural variation.

**GOOD** (German, natural burstiness, question in own paragraph):
```
Also der Vertrag sieht gut aus. Die Zahlungskonditionen passen auch.

Frage: Ich würde den ersten Termin gerne um zwei Wochen verschieben. Geht das? Ruf mich kurz an, wenn du morgen (Freitag, 2026-07-17) Zeit hast.
```
5 sentences: 6, 4, 10, 2, 12 words.

**GOOD** (French, natural burstiness, question and commitment in own paragraphs):
```
J'ai regardé le contrat. Les conditions sont bonnes, premier versement
en août 2026 puis trimestriel, ça nous laisse assez de marge.

Question : Je voudrais décaler le premier rendez-vous de deux semaines. C'est possible ?

Je renvoie le contrat signé demain (vendredi 2026-07-17).
```
5 sentences: 5, 17, 9, 2, 8 words.

## Opening/Closing Repertoire

People are consistent with their greeting and closing habits. Use the user's habitual forms from History. Variation exists only when History shows a contextual pattern (register, thread type, recipient). Mechanical per-draft rotation is LLM-introduced noise and itself a detection signal.

- Use the user's dominant greeting/closing for the given recipient and register
- Vary ONLY when History shows a contextual pattern (e.g., "Hi" in quick replies, formal form in new threads)
- Never invent forms not in the user's repertoire
- Never rotate per draft to simulate variety

**BAD** (inventing new greeting style):
```
History shows user always writes "Hi [Name]," and "Beste Grüße"
Draft produces: "Dear [Name]," and "Kind regards,"
```

**BAD** (mechanical rotation to simulate variety):
```
History shows user writes "Hi Thomas," ... "LG" in 9 of 10 emails.

Draft 1: "Hallo Thomas," ... "Beste Grüße"
Draft 2: "Thomas," ... "Viele Grüße"
Draft 3: "Hi Thomas," ... "LG"
```

**GOOD** (habitual forms, variation only by context):
```
GREETING_VARIANTS: [Hi [Name], (dominant) | Hallo [Name], (new threads)]
CLOSING_VARIANTS: [LG (dominant) | Beste Grüße (formal topics)]

Draft 1 (reply): "Hi Thomas," ... "LG"
Draft 2 (reply): "Hi Thomas," ... "LG"
Draft 3 (new thread, contract topic): "Hallo Thomas," ... "Beste Grüße"
```

**Register matching**: If the user uses different greetings for different formality levels (e.g., "Hi" for peers, "Sehr geehrte/r" for formal), match the register to the recipient.

## Native Naturalness

Drafts in any language must read as written by a native speaker. Never compose in English and translate literally - English sentence structure, idioms, and word choice carry over and read as machine-translated. Compose from the intent directly in the target language.

**Verification test**: Would a native speaker write this sentence exactly this way? If unsure, rephrase from the intent, not from the English wording.

**Subject pronoun test**: Every sentence describing an action or event must have a personal subject (ich, wir, er, sie). AI defaults to impersonal event descriptions (noun phrases, participial constructions). Humans talk about themselves first - the subject pronoun is what makes text sound like a person, not a report.

**BAD** (German, impersonal event description - reads as AI summary):
```
Eine Stunde lang über das Projekt gesprochen.
Richtig produktives Gespräch zum Thema Migration.
```
No subject pronoun. Reads like a calendar note or log entry, not a person writing.

**GOOD** (German, personal subject - reads as human):
```
Wir haben ca. eine Stunde über das Projekt gesprochen.
Ich fand das Gespräch zum Thema Migration richtig produktiv.
```

**BAD** (English, same pattern):
```
Great call. Discussed the project scope for an hour.
```

**GOOD** (English, same pattern):
```
We had a great call. We discussed the project scope for about an hour.
```

**BAD** (German, formal calque from English):
```
Ich habe den Vertrag angeschaut und finde die Konditionen akzeptabel.
```
"akzeptabel" is a formal calque of English "acceptable" - no native speaker uses it in casual email. Native alternatives: "passen", "sind OK", "gehen klar", "sind in Ordnung".

**GOOD** (German, native phrasing of the same intent):
```
Ich hab mir den Vertrag angeschaut und denke, die Konditionen passen so.
```

**BAD** (Spanish, calqued English politeness formula):
```
Estoy escribiendo para preguntar sobre el estado de mi factura.
```
Calque of "I am writing to ask about". Spanish does not use the progressive here.

**GOOD** (Spanish, native phrasing):
```
Te escribo para preguntarte por el estado de mi factura.
```

## Vocabulary Avoidance

Never use high-frequency LLM vocabulary in user-voice drafts. These words are statistically over-represented in AI output and trigger detection.

**Avoid**: delve, crucial, pivotal, nuanced, multifaceted, landscape (non-geographic), tapestry, realm, myriad, foster, leverage, navigate (non-physical), underscore, "It's important to note that," "It's worth mentioning," "In today's [X] landscape"

**Avoid**: Formal conjunctive adverbs in casual context: Moreover, Furthermore, Additionally, Nevertheless, Consequently, Nonetheless

**Use instead**: Natural equivalents - but, so, and, still, also, plus, anyway, though

**BAD:**
```
Moreover, I would like to underscore the crucial importance of navigating
the multifaceted challenges we currently face.
```

**GOOD** (same content, natural vocabulary, self-contained ask in own paragraph):
```
I think all problems at once is too much for this conversation.

Question: Are you OK with going through the problems one by one?
```

**GOOD** (German, self-contained ask in own paragraph):
```
Also - ich denke das ist zu viel auf einmal, um es hier zu besprechen.

Frage: Können wir die Probleme einzeln durchgehen?
```

## Connective Register

Use informal connectives in casual communication. Formal connectives (However, Nevertheless, Furthermore) are appropriate only when the user's History shows them.

**BAD** (formal connectives in WhatsApp):
```
Furthermore, I will not be available on Thursday. Consequently, we should
reschedule. Nevertheless, I remain committed to the project timeline.
```

**GOOD** (German, natural connectives, question in own paragraph):
```
Donnerstag (2026-07-23) geht leider nicht bei mir.

Frage: Können wir den Termin auf Freitag, 2026-07-24 verschieben?

Am Zeitplan ändert sich dadurch aber nichts.
```

**GOOD** (Spanish, natural connectives, question in own paragraph):
```
El jueves (2026-07-23) no me viene bien.

Pregunta: ¿Podemos pasar la reunión al viernes, 2026-07-24?

El calendario no cambia por eso.
```

## Humanizing Settings Template

Add this section to CONVERSATION_[COUNTERPARTY].md between Translation Settings and Status. Values are populated from CV-HM-02 (Consistency Anchoring) analysis or set manually by the user.

```
## Humanizing Settings

- **SPELLING_VARIANTS**: [ß_PREFER: weiß, Straße, Grüße, heißt]
- **DISCOURSE_MARKERS**: [actually, well, basically | na ja, halt, eigentlich]
- **GREETING_VARIANTS**: [Hi [Name], (dominant) | Hallo [Name], (new threads)]
- **CLOSING_VARIANTS**: [LG (dominant) | Beste Grüße (formal topics)]
- **SENTENCE_LENGTH_PROFILE**: [short: 40%, medium: 35%, long: 25%]
- **ANCHORING**: [PROFILE_EXTRACTED | INSUFFICIENT_HISTORY | MANUAL]
```

**Default values** (when no History exists):
```
## Humanizing Settings

- **SPELLING_VARIANTS**: [standard orthography]
- **DISCOURSE_MARKERS**: [use language defaults, 1-2 per message]
- **GREETING_VARIANTS**: [extract from first user message]
- **CLOSING_VARIANTS**: [extract from first user message]
- **SENTENCE_LENGTH_PROFILE**: [short: 30%, medium: 40%, long: 30%]
- **ANCHORING**: INSUFFICIENT_HISTORY
```
