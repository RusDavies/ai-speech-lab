# Goal

Create an open source text-to-speech engine that generates expressive, natural
speech from text with optional intonation/prosody control and authorized voice
adaptation.

## Product Goal

AI Speech Lab should:

- Receive text to convert into speech.
- Optionally receive intonation or prosody information.
- Synthesize suitable intonation when no prosody input is supplied.
- Sound as expressive and natural as current Alexa-class speech.
- Be capable of sounding like a target speaker when the user provides an
  authorized voice sample.
- Ultimately achieve interactive low latency below 200 ms.

## First Useful Outcome

The first useful outcome is a runnable research prototype that:

- accepts text input;
- accepts optional prosody metadata;
- produces speech output;
- records latency measurements;
- supports repeatable comparison against selected quality baselines;
- documents which final-goal capabilities are still missing.

## Non-Goals For The First Prototype

- Claiming Alexa-level quality before comparative evidence exists.
- Public release before licensing, dataset, consent, and misuse boundaries are
  clear.
- Optimizing to sub-200 ms latency before the measurement harness exists.
