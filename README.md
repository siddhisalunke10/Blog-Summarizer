# Blog Summarizer

A Python program that fetches a blog article from a given URL, cleans the extracted text, and generates a concise summary (under 300 words / 20 sentences) using the Gemini API.

## Approach

The program follows a simple pipeline:

1. **Fetch** — `requests` downloads the raw HTML of the blog page.
2. **Clean** — `BeautifulSoup` parses the HTML and strips out non-content elements (navbars, footers, headers, scripts, styles, asides) so only the actual article text remains.
3. **Summarize** — the cleaned text is sent to Google's Gemini API (`gemini-2.5-flash`) with a prompt instructing it to:
   - Stay within 300 words and 20 sentences
   - Write in paragraph form (no bullet points)
   - Preserve concrete details such as exact commands, version numbers, and statistics, rather than vaguely describing them
4. **Validate** — the generated summary is automatically checked against the word and sentence limits, and a warning is printed if either limit is exceeded.
5. **Save** — the final summary is written to `summary.txt`.

### Why Gemini?

Gemini's free tier was used to avoid API costs for a single-summary task like this. The code is written so the AI provider is isolated to one function (`summarize()`), making it easy to swap in another model (Claude, OpenAI, etc.) by changing just that function.

## Libraries Used

| Library | Purpose |
|---|---|
| `requests` | Fetch the blog page over HTTP |
| `beautifulsoup4` | Parse HTML and extract clean text |
| `google-genai` | Call the Gemini API for summarization |
| `python-dotenv` | Load the API key from a `.env` file instead of hardcoding it |

## How to Run

1. Install dependencies:
   ```
   pip install requests beautifulsoup4 google-genai python-dotenv
   ```
2. Create a `.env` file in the project folder with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the script:
   ```
   python summarizer.py
   ```
4. The summary will be printed to the terminal and saved to `summary.txt`.

## Edge Cases Handled

- **Failed fetch**: if the blog URL returns a non-200 status code, the program raises a clear error instead of silently failing.
- **Noisy HTML**: navigation bars, footers, scripts, and other non-article elements are stripped before summarization so they don't pollute the summary.
- **Length constraints**: the output is automatically validated against the 300-word and 20-sentence limits, with a warning printed if exceeded, rather than trusting the model blindly.
- **API key safety**: the API key is loaded from a `.env` file (excluded from version control via `.gitignore`) rather than hardcoded into the script.

## Files

- `summarizer.py` — main program
- `summary.txt` — generated output summary
- `.env` — stores the API key (not included in submission for security)
- `README.md` — this file