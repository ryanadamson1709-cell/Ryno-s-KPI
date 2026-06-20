name: Daily share briefing

on:
  schedule:
    # Runs at 06:00 UTC every day. Edit this to change the time.
    - cron: '0 6 * * *'
  workflow_dispatch: {}

permissions:
  contents: write

jobs:
  update-briefings:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Fetch briefings
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python scripts/fetch_briefings.py

      - name: Commit updated data
        run: |
          git config user.name "ledger-bot"
          git config user.email "ledger-bot@users.noreply.github.com"
          git add data/briefings.json
          git diff --quiet --cached || git commit -m "Daily briefing update: $(date -u +%Y-%m-%d)"
          git push
