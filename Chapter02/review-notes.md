# Chapter 2 review notes

Technical review of "The Economics of Agency". Section numbers follow the manuscript.

Chapter 2 has one code listing and it's illustrative rather than working code, so there's
nothing to add to the repo. These are notes only.

## Listing 2.1

**The payback guard hides the answer that matters most.**

```python
payback_months = dev_cost / max(net_gain, 1e-9)
```

The `max(..., 1e-9)` presumably avoids dividing by zero, but it also swallows the negative
case. An architecture that loses money every month never pays back. Instead of saying so,
this divides by 1e-9 and returns roughly 2e14 months, which reads as a big but finite
number. In a chapter arguing that autonomy has to earn its cost, that's the one figure a
reader is likely to construct for themselves.

Suggested:

```python
payback_months = dev_cost / net_gain if net_gain > 0 else float("inf")
```

All three configurations in the listing are profitable, so the printed output doesn't
change and the prose in 2.3.2 still holds.

**The code doesn't compute the formula printed above it.**

2.3.2 gives `ROI ≈ (Value per task × Frequency × Longevity) ÷ Lifecycle cost`. The function
computes `net_gain / monthly_cost`. There's no longevity term and `dev_cost` never enters
the denominator. What comes back is a monthly operating ratio, not lifecycle ROI.

**The narrative describes a crossover the model can't produce.**

2.3.2 says agents "can eventually surpass the others when volume or automation intensity is
high". Because the returned ROI is a flat monthly ratio, the agent's 1.14 stays below the
other two indefinitely. A crossover needs cumulative ROI over time, which is what Figure
2.10 shows. So the figure and the listing disagree.

## Figures and tables

**Figure 2.4's caption belongs to a different figure.** The text introduces a radar chart
across the five evaluation axes. The caption describes broad-versus-narrow ROI, which is
Chapter 1's Figure 1.2.

**Table 2.4 is titled "When Agentic Ambitions Backfire"** but one of its three rows is
JPMorgan, which the chapter presents as the success case.

## Draft notes left in the finished text

2.2.1 says "A figure could depict this as a gradient from 'closed box' on the left to
'open, explainable system' in the middle to 'multi-actor network' on the right". No figure
follows.

2.3.4 says "Figure 2.11 could depict these two trajectories" three lines above Figure
2.11's actual caption.

## Sourcing

**The 2.4.1 case studies have no citations.** Forward, Babylon Health and JPMorgan are named
with specific factual claims: Forward shut down in late 2024, Babylon entered administration
by 2023, JPMorgan's LLM Suite reached 200,000 employees and won an award in 2025.

The bigger issue is that the causal reading is asserted rather than sourced. Babylon is said
to have failed because "governance overhead neutralized autonomy" and Forward because its
"autonomy never scaled enough to offset upkeep". The public record points substantially at
unit economics, consumer adoption, hardware reliability and funding conditions. These may be
consistent with the chapter's thesis, but the chapter states them as the cause. Worth either
softening to "consistent with" or backing each row of Table 2.4 with a reference. Given these
are named real companies, it may be worth a legal read as well as an editorial one.

**2.1 also says "Recent research has shown that combining retrieval with fine-tuning can
outperform either approach alone"** with no citation.

## Language

2.1.4, missing a verb: "When designing an AI system, at the non-agentic end of the table and
move toward agentic architectures only as the task demands greater autonomy."

2.1.3 repeats a sentence twice in one paragraph: "In this sense, agency is not a separate
technology but an organizing layer that turns isolated intelligence into purposeful
behavior."

"faster than its compounds cost" appears in 2.3.4, again in 2.4.2, and in the summary. Should
be "than it compounds cost".

2.3.3 writes "50 000 tasks per month" where the listing and surrounding prose use 50,000.

## Structure

**2.2 restates 2.1 before adding anything.** The opening two paragraphs recap the three
approaches and the trade-off triangle, which 2.1.4 has already summarised.

**Four competing mental models in a few pages.** The triangle (Figure 2.1), the
scalpel/library/assistant metaphor, three concentric circles in 2.1.1, and the radar chart
(Figure 2.4) all describe the same distinction. The concentric circles appear once and are
never illustrated.

**The closing promise doesn't match Chapter 3.** 2.4.2 says the next chapter will show "how
planning, memory, and tool use interact". Chapter 3 covers planning only; memory is Chapter 4
and tool use is Chapter 5.
