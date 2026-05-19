# Chapter 04 - Building a Persistent Learning Agent

This folder contains the code and pseudocode listings extracted from `01-Ch_04_kapoor-Google-Docs.pdf`.

The chapter mixes three kinds of material:

- executable-looking Python snippets
- intentionally simplified pseudocode
- small diagnostic examples that rely on surrounding chapter context

## Contents

- `dynamic_context_assembly.pseudo` - pseudocode block from section 4.2.3
- `retrieval_as_reasoning_pipeline.pseudo` - Listing 4.1
- `engineering_agent.py` - Listing 4.2
- `case_1_memory_supports_reasoning.py` - Listing 4.3a
- `case_1_remove_episodic_memory.py` - Listing 4.3b
- `case_2_memory_distorts_reasoning.py` - Listing 4.3c
- `case_2_remove_episodic_memory.py` - Listing 4.3d
- `memory_ablation_harness.py` - first Listing 4.4 in section 4.3.2
- `temporal_decay.py` - second Listing 4.4 in section 4.4.1
- `importance_scoring.py` - Listing 4.5
- `memory_pruning.py` - Listing 4.6
- `episodic_reset.py` - Listing 4.7
- `intentional_forgetting_tools.py` - Listing 4.8
- `final_retrieval_score.py` - Listing 4.9

## Notes

- The manuscript contains two different snippets both labeled `Listing 4.4`. They are stored here under descriptive filenames to avoid a collision.
- The pseudocode files are preserved as pseudocode rather than converted into runnable Python.
- Several Python snippets are illustrative rather than complete applications. For example, `EngineeringAgent` assumes an `llm` callable, `logs` input, and an episodic store interface supplied by surrounding code.
- `intentional_forgetting_tools.py` references `time.time()` exactly as shown in the chapter. The import is not present in the source listing and was not added here.
