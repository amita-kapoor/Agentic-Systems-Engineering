# Chapter 3 review notes

Technical review of "From task decomposition to strategic foresight". Section numbers follow
the manuscript.

## The framework listings

Chapter 3 shipped the same flight-booking example three times, once each in LangGraph,
AutoGen and CrewAI. This PR removes all three notebooks. The reasoning, in case you disagree
with any of it:

**Readers can get this from the projects' own docs.** Each listing is close to what the
framework's quickstart already shows. There isn't much a reader gets here that they can't get
faster, and more up to date, from the source.

**It's the part that ages fastest.** Microsoft put AutoGen into maintenance mode when Agent
Framework 1.0 reached GA on 3 April 2026. It still gets bug fixes and security patches but no
new features, and new users are pointed at Agent Framework. That happened after the chapter
was written, and it will happen again to whichever framework you pick. The rest of the
chapter doesn't have this problem.

**It contradicts the book's own positioning.** Chapter 1 says: "This book is principle-first,
not framework-first. You won't find a step-by-step tutorial on one tool." Section 3.2 is three
step-by-step tutorials on three tools.

**The rest of the chapter is the part worth keeping.** Decomposition, HTNs, Firby's three-tier
model, the design patterns in 3.3.1 and the trade-off tensions in Figure 3.11 aren't in
anyone's quickstart. That material is the chapter's actual contribution and none of it depends
on the listings.

If you do want a worked implementation, LangGraph is the one I'd keep. It ran cleanly against
langgraph 1.2 when I tested it, it makes no LLM call at all so it costs nothing to run, and
its graph is a plain state machine rather than a vendor agent abstraction that will get
renamed. AutoGen and CrewAI both route through framework-specific agent classes.

## The multi-framework architecture in 3.4

Separate from the listings, and in my view the more important thing in this chapter.

The Research Orchestration Agent in 3.4, drawn in Figure 3.12, is presented as a reference
architecture that runs LangGraph for planning, AutoGen for the reasoning agents, CrewAI for
coordination, MCP for shared state and A2A for messaging. Figure 3.1 sets up the same
arrangement earlier in the chapter.

I'd recommend cutting this, for a few reasons.

**It's advice nobody should follow.** LangGraph, AutoGen and CrewAI are three orchestration
frameworks that solve the same problem in three different ways. Running all three in one
system means three dependency trees, three sets of breaking changes to track, three
execution models to reason about when something hangs, and three places to look when a task
goes missing. The coordination cost the chapter warns about in 3.3 is precisely what this
architecture creates.

**It has already broken.** AutoGen's move to maintenance mode means this reference
architecture, as printed, now includes a component readers are being told to migrate away
from. That happened within months of writing. A design whose correctness depends on three
vendors' roadmaps staying aligned is not a reference architecture.

**It's the clearest case of framework-first drift in the book.** Chapter 1 promises
principles that "outlast today's APIs". This section names five specific products in a
single diagram.

**The underlying idea is fine and doesn't need any of them.** Planner, executor, critic and
coordinator are roles. Shared state and message passing are interfaces. Every point 3.4
makes about the Plan-Act-Observe-Reflect loop moving through those roles holds without
naming a single product, and it would then still be true in three years. If a concrete
implementation is wanted, one framework can fill all the roles, which is a much easier thing
to defend and to maintain.

My suggestion would be to redraw Figures 3.1 and 3.12 with roles instead of product names,
and keep 3.4's walkthrough as it is. The step-by-step sequence from user query through
planning, execution, evaluation and replanning is good, and it doesn't depend on which tool
runs each step.

## What this leaves without code

- 3.2.2, the subsection "AutoGen: conversations as planning loops"
- Listing 3.2 and Figure 3.7
- Listing 3.3 and Figure 3.8
- 3.2.1, 3.2.3 and 3.3.1, which compare the three frameworks by name
- 3.4 and Figure 3.12, where the Research Orchestration Agent names "AutoGen reasoning agents"
  and a "CrewAI coordinator" as components
- The Chapter 3 summary, and one mention in Chapter 1's list of prerequisites

## One thing not to cut

If dropping the whole chapter is on the table, planning is load-bearing for Chapter 6.
Double-loop learning is defined there as feedback revising the plan rather than the output.
Listing 6.3 takes a planner as an argument and the compliance agent's outer loop calls it.
Without the planning material, Chapter 6's central distinction has nothing underneath it.

## Other findings

**Figure 3.1's caption contradicts the body text.** The caption says "MCP provides shared
memory accessible to all components". Section 3.2.3 says, correctly, "MCP itself is a stateless
protocol. It does not store memory or manage agent state." The chapter summary then repeats the
caption's version. The body text is the right one, so the caption and summary should follow it.

**3.3.1 points at the wrong figure.** It says "As shown in Figure 3.12, these patterns can be
viewed as a spectrum" where it means Figure 3.10. Figure 3.12 is the Research Orchestration
Agent, several pages later.

**Listing 3.1 is fine as printed.** I initially thought calling `set_entry_point` before
`add_node` was a bug. It isn't. LangGraph validates at `compile()`, not at call time, and the
notebook runs. Noting it here so nobody goes looking for a problem that isn't there.

## Language

3.3.1: "jusgement" should be "judgement".

3.2.2: "Each agent execute its assigned task independently" should be "executes".

3.2.2 repeats a sentence back to back: "This distinction reflects a broader engineering
principle: This distinction reflects a broader engineering principle:".
