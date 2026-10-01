# Security Policy

AI Speech Lab is early-stage research software. The security-sensitive parts of this
project include voice adaptation, provenance, model execution, downloaded
artifacts, and any future service API.

## Reporting A Vulnerability

Please use GitHub private vulnerability reporting or a private GitHub security
advisory for security issues. Do not include exploit details, private voice
samples, credentials, or identity-sensitive audio in public issues.

If private reporting is unavailable, open a minimal public issue saying that you
have a security concern and avoid sensitive details until a private channel is
available.

## Scope

Security-relevant issues include:

- unsafe handling of voice samples;
- impersonation or consent-bypass risks;
- unsafe model or artifact download behavior;
- command injection or unsafe benchmark-wrapper behavior;
- leakage of generated audio, prompts, paths, tokens, or environment details;
- future API authentication, authorization, or isolation problems.

## Current Status

There is no production service yet. The current repository contains research
docs, benchmark cases, and a local benchmark harness. Treat all future runtime
interfaces as experimental until explicitly documented otherwise.
