# Chapter 04 - Building a Persistent Learning Agent

This folder contains the listings extracted from the revised Chapter 4 PDF, `01-Ch04_kapoor-Google-Docs-1-.pdf`.

The chapter mixes three kinds of material:

- executable-looking Python snippets
- intentionally simplified pseudocode
- compact structured memory examples
- small diagnostic examples that rely on surrounding chapter context

## Contents

- `listings/dynamic_context_assembly.pseudo` - Listing 4.1
- `listings/semantic_memory_architecture_summary.txt` - Listing 4.2
- `listings/episodic_memory_prior_incident_summary.txt` - Listing 4.3
- `listings/external_artifact_recent_deployment_and_logs.txt` - Listing 4.4
- `listings/retrieval_as_reasoning_pipeline.pseudo` - Listing 4.5
- `listings/engineering_agent.py` - Listing 4.6
- `listings/case_1_memory_supports_reasoning.py` - Listing 4.7a
- `listings/case_1_remove_episodic_memory.py` - Listing 4.7b
- `listings/case_2_memory_distorts_reasoning.py` - Listing 4.7c
- `listings/case_2_remove_episodic_memory.py` - Listing 4.7d
- `listings/memory_ablation_harness.py` - Listing 4.8
- `listings/temporal_decay.py` - Listing 4.9
- `listings/importance_scoring.py` - Listing 4.10
- `listings/memory_pruning.py` - Listing 4.11
- `listings/episodic_reset.py` - Listing 4.12
- `listings/intentional_forgetting_tools.py` - Listing 4.13
- `listings/final_retrieval_score.py` - Listing 4.14

## Notes

- The structured memory examples in Listings 4.2, 4.3, and 4.4 are preserved as plain text because they are labeled listings in the PDF but are not source code.
- The pseudocode files are preserved as pseudocode rather than converted into runnable Python.
- Several Python snippets are illustrative rather than complete applications. For example, `EngineeringAgent` assumes an `llm` callable, `logs` input, and an episodic store interface supplied by surrounding code.
- `listings/intentional_forgetting_tools.py` references `time.time()` exactly as shown in the chapter. The import is not present in the source listing and was not added here.
