<!--
  Profile README. Every panel is an animated SVG in assets/readme/, in a light and a dark version;
  <picture> shows the one that matches the viewer's GitHub theme. Text inside the SVGs uses embedded Geist subsets.
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/hero-dark.svg">
  <img src="assets/readme/hero-light.svg" width="100%" alt="Varad Shajith, AI / research engineering, Nashik, CS &#x27;28. I build systems that refuse to lie to their users. A system that fails loudly is fixable. One that returns a confident, well-formed, wrong answer is not; you never know to look. Most of my work is making the second kind impossible.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/now-dark.svg">
  <img src="assets/readme/now-light.svg" width="100%" alt="Right now. Building foreman: runs K agents in parallel, keeps the one that passes (19 tests, 0.72 s, no network). Running the clinic system: live for a real practice, 3-person team, I own security (845 tests, 20 migrations, Postgres 17). Offline mockmate-gemma: local model on a 6 GB card, network off, never invents a score (2.3 s per 30 s clip, ~4,201 of 6,141 MB VRAM).">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/stack-marquee-dark.svg">
  <img src="assets/readme/stack-marquee-light.svg" width="100%" alt="What I build with: llama.cpp, Gemma 4 E4B, Groq, Gemini, Claude, Whisper, Piper TTS, bge-small, FastAPI, SQLAlchemy, Postgres 17, SQLite, Celery, Redis, Flutter, Firebase, React 19, Chrome MV3, Podman, Fedora.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/work-dark.svg">
  <img src="assets/readme/work-light.svg" width="100%" alt="Selected work, 01 to 03: three systems that show their work.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/foreman-dark.svg">
  <img src="assets/readme/foreman-light.svg" width="100%" alt="01 foreman, building: verification that isn&#x27;t an opinion. Each task fans out to K CLI workers in isolated git worktrees; the first diff that applies, compiles and passes the task&#x27;s own verify_cmd wins. No model grades another model&#x27;s work. Beta posteriors per (task type, worker) learn the routing. 19 tests, 0.72 s, no network. Animated diagram: five workers race through applies, compiles and passes-verify_cmd gates; failures are crossed out, the first to pass merges, late passers are discarded.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/clinic-dark.svg">
  <img src="assets/readme/clinic-light.svg" width="100%" alt="02 clinic system, running, private: backups the server cannot read. Three-person team, live for a real practice; I own the security lane. Backups wrap a data key under X25519, HKDF-SHA256 and AES-256-GCM for two offline key-holders, with the header bound as associated data, so stripping a recipient breaks the tag. No decrypt function exists anywhere in app/; restore happens offline, by hand. 45k lines of backend Python, 845 tests, 20 migrations, CI against Postgres 17.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/mockmate-dark.svg">
  <img src="assets/readme/mockmate-light.svg" width="100%" alt="03 mockmate-gemma, offline: bugs that produced confident, wrong output. Offline interview coach, local Gemma 4 E4B on a 6 GB card, network off; the model that grades is the model that listened. Pipeline: pw-record, Smart Turn v3, Gemma 4 E4B via llama-server, Piper TTS; bge-small memory. Replayed log: a grader at temperature above 0 scored 65, 75, 75 on identical input; at 0.0 there is 0-point variance. A regression test rebuilt its own copy of the prompt. An embedding server without --pooling mean compared [CLS] tokens. Audio past 30 s was silently dropped. Measured on an RTX 4050 Mobile: 2.3 s per 30 s clip, 5/5 rubric slot detection, 27 ms memory retrieval at 50 entries, ~4,201 of 6,141 MB VRAM.">
</picture>

<p align="center"><a href="https://github.com/varadshajith/mockmate-gemma"><code>mockmate-gemma</code></a></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/shipped-dark.svg">
  <img src="assets/readme/shipped-light.svg" width="100%" alt="Also shipped. PromptPilot: rewrites your prompt before it reaches the model and never auto-submits; if validation fails your original text is left alone. recall_telegram_bot: voice note in, structured brief out. Gram-yatra: a city shown the way a local would show it, 18 screens, team lead. fastf1-visuals: Formula 1 telemetry, lap, sector and tyre-strategy analysis. GitSwipe: repo discovery with a guided path to a first PR, about 18% built, shelved. solnova: Smart India Hackathon microgrid monitoring, I owned the software. Also eight ML notebooks, MNIST through ResNet50 at 98.9% accuracy.">
</picture>

<p align="center">
  <a href="https://github.com/varadshajith/PromptPilot">PromptPilot</a> ·
  <a href="https://github.com/varadshajith/recall_telegram_bot">recall_telegram_bot</a> ·
  <a href="https://github.com/varadshajith/Gram-yatra">Gram-yatra</a> ·
  <a href="https://github.com/varadshajith/fastf1-visuals">fastf1-visuals</a> ·
  <a href="https://github.com/varadshajith/GitSwipe">GitSwipe</a> ·
  <a href="https://github.com/varadshajith/solnova">solnova</a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/how-dark.svg">
  <img src="assets/readme/how-light.svg" width="100%" alt="How I work. Read plans against the repo: I grep the file:line a ticket cites before trusting it. One review turned up fifteen discrepancies, including a ticket ID that did not exist. Write down what I rejected: Rejected decisions sit next to the kept ones. Redis, Kafka and Kubernetes are on that list: unnecessary at clinic scale. Counts come from run output: Test counts come from actual test output, never from counting def test_ in source. An audit claim needs a file:line, or it says NOT FOUND. Cut ceremony that finds nothing: The full ticket lifecycle ate ~50% of working time and caught very few real bugs. It became a 42-line RULES.md: a PATCH lane and a BUILD lane. Agents read, I commit: Coding agents get read-only git: status, diff, log. Every commit and every push is mine, by hand. No invented numbers: A missing measurement is reported as missing. When an agent reported predicted behaviour as observed results, the rules were rewritten to forbid it.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/next-dark.svg">
  <img src="assets/readme/next-light.svg" width="100%" alt="Next on the bench. A cache-first coding-agent harness: its own agent loop talking to model APIs directly, with prompt- and KV-cache-aware prefixes and compaction, and a beginner layer on top. Exocortex: a personal AI chief of staff, local-first on a Fedora laptop, reached over Tailscale; a Discord bot and a pilot CLI, SQLite plus a markdown vault.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/stack-dark.svg">
  <img src="assets/readme/stack-light.svg" width="100%" alt="Stack. Daily: Fedora, Claude Code, Podman, git by hand. Backend: Python, FastAPI, SQLAlchemy 2.0 async, Alembic, Postgres, SQLite, Celery. Apps: Flutter, React 19, Vite, TypeScript, Chrome MV3. Models: llama.cpp, Gemma, Groq, Gemini, Claude, Whisper, Piper. Off the keyboard: motorsport; Formula 1 telemetry is the reason fastf1-visuals exists.">
</picture>

<a href="mailto:varadshajith@gmail.com">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/contact-dark.svg">
  <img src="assets/readme/contact-light.svg" width="100%" alt="Say hello: varadshajith@gmail.com. Varad Shajith, Nashik, CS &#x27;28.">
</picture>
</a>

<p align="center">
  <a href="mailto:varadshajith@gmail.com">Email</a> ·
  <a href="https://www.linkedin.com/in/varad-shajith-410347369">LinkedIn</a> ·
  <a href="https://github.com/varadshajith">GitHub</a>
</p>
