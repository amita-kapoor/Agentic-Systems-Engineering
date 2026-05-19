# Chapter 5 Listings

This folder contains the extracted code listings for Chapter 5, "The Action Engine".

Source PDFs:
- `01-ch05_kapoor-Google-Docs.pdf`
- `02-ch05_kapoor-Google-Docs-2-.pdf`

The two uploaded PDFs were byte-for-byte identical, so the chapter was extracted once and organized here using the repository's flat `listing_5_x.*` naming convention.

| Listing | File | Description |
|---|---|---|
| 5.1 | [`listing_5_1.py`](listing_5_1.py) | Defining a structured interface for a customer lookup action and handling the outcomes returned by the action |
| 5.2 | [`listing_5_2.py`](listing_5_2.py) | A minimal typed tool with structured inputs and outputs |
| 5.3 | [`listing_5_3.json`](listing_5_3.json) | MCP JSON schema |
| 5.4a | [`listing_5_4a.py`](listing_5_4a.py) | Tool metadata with policy enforcement |
| 5.4b | [`listing_5_4b.py`](listing_5_4b.py) | Tool metadata and result structures |
| 5.4c | [`listing_5_4c.py`](listing_5_4c.py) | Tool implementation with controlled execution |
| 5.5 | [`listing_5_5.py`](listing_5_5.py) | Enforcing policy constraints through tool metadata |
| 5.6 | [`listing_5_6.py`](listing_5_6.py) | Registering tools and retrieving candidates semantically |
| 5.7 | [`listing_5_7.py`](listing_5_7.py) | Filtering tools by risk before semantic retrieval |
| 5.8 | [`listing_5_8.py`](listing_5_8.py) | Versioning a tool contract through metadata |
| 5.9 | [`listing_5_9.py`](listing_5_9.py) | Adapting an older tool contract to a newer implementation |
| 5.10 | [`listing_5_10.py`](listing_5_10.py) | Generating a deterministic idempotency key |
| 5.11 | [`listing_5_11.py`](listing_5_11.py) | Idempotent executor with result caching |
| 5.12 | [`listing_5_12.py`](listing_5_12.py) | Circuit breaker for tool execution |
| 5.13 | [`listing_5_13.py`](listing_5_13.py) | Saga pattern with compensation stack |
| 5.14 | [`listing_5_14.py`](listing_5_14.py) | Evaluating execution policy from tool metadata |
| 5.15 | [`listing_5_15.py`](listing_5_15.py) | Making idempotent execution composable |
| 5.16 | [`listing_5_16.py`](listing_5_16.py) | Sequencing policy, validation, idempotency, and circuit breaking |
| 5.17 | [`listing_5_17.py`](listing_5_17.py) | Coordinating retrieval and execution in the action engine |
| 5.18 | [`listing_5_18.py`](listing_5_18.py) | Running the complete action engine end to end |
| 5.19 | [`listing_5_19.py`](listing_5_19.py) | A minimal browser automation tool using page interaction |
| 5.20 | [`listing_5_20.py`](listing_5_20.py) | Allowlisted and constrained shell execution |

## Notes

- Listing 5.3 is preserved as JSON because the chapter presents it as a schema rather than Python code.
- Listings 5.4a, 5.4b, and 5.4c are kept as separate files because they are presented as separate sub-listings in the chapter.
- Several files are intentionally partial examples from the book and are preserved as chapter snippets rather than expanded into standalone runnable modules.
- Obvious PDF artifacts were normalized only where the intent was clear, including indentation recovery from the monospace layout and conversion of typographic punctuation to plain ASCII where needed.
- The duplicated `from playwright.async_api import async_playwright` line in Listing 5.19 was preserved because it appears that way in the source PDF.
