# The Social Collapse — working notes

- Live site: https://the-social-collapse.pages.dev (Cloudflare Pages project `the-social-collapse`, connected to this repo).
- Cloudflare deploys automatically on every push to `main`, serving the `public/` folder (no build command).
- Edit the game in `src/template.html` (and `src/intro.html` for the boot/intro/loading screens), then run `python3 src/build.py` to regenerate `public/index.html`. Never hand-edit `public/index.html`.
- Versions: `VERSION` file, numbered 0.0.x (bump the last number per ship unless told otherwise). Also offer a zip named `The-Social-Collapse-vX.Y.Z.zip` of `public/` if a download is wanted.
- "Ship it" = build, bump VERSION, commit, push to `main`, then open the live site and check the intro, loading screen, map and icons work.
- Only ship when the user says "Ship it".
- SpinBot AI: `functions/api/spinbot.js` is a Cloudflare Pages Function that calls Workers AI (binding name `AI`, model llama-3.1-8b-instruct). The game sends the question, recent chat and a summary of the game state. If the endpoint is unavailable (e.g. in the claude.ai preview), the game falls back to built-in answers in `aiAnswer()`.
