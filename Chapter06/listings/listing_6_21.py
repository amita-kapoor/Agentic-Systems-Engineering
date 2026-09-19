@dataclass
# Captures the final report, validation signal, plan, trace, and termination state
class AgentResult:
    final_report: DraftReport
    final_signal: ValidationSignal
    plan: Plan
    iterations: int
    history: list[dict]
    termination: Literal["acceptable", "converged", "exhausted"]


class ComplianceAgent:
    def __init__(self, framework, validator, memory, max_inner_iters=3, max_outer_iters=2):
        # Semantic memory: stable regulatory framework used to retrieve relevant clauses
        self.framework = framework
        self.validator = (
            validator  # Observation layer: deterministic validator that produces grounded signals
        )
        self.memory = memory  # Episodic memory: stores lessons from prior runs
        self.max_inner_iters = max_inner_iters
        self.max_outer_iters = max_outer_iters

    def run(self, product_description: str) -> AgentResult:
        # Create a task signature used for episodic memory retrieval and storage
        task_signature = f"compliance_report::{product_description[:60]}"
        relevant = self.framework.retrieve_relevant(
            product_description
        )  # Retrieve relevant regulatory clauses for this product
        past = self.memory.retrieve(
            task_signature
        )  # Retrieve prior reflection records for similar tasks
        memory_block = self.memory.as_prompt_block(
            past
        )  # Convert memory records into prompt context

        plan = planner(
            {"product_description": product_description, "clauses": relevant}
        )  # Generate the initial plan before drafting

        history: list[dict] = []
        previous_draft: Optional[DraftReport] = None
        signal = ValidationSignal()
        critique: Critique = {"status": "needs_revision", "issues": [], "feedback": ""}
        previous_issues: set[str] = set()
        total_iters = 0

        for outer in range(self.max_outer_iters):  # Outer loop enables planning-level reflection
            for inner in range(self.max_inner_iters):  # Inner loop performs output-level reflection
                total_iters += 1
                draft = generator(
                    # Generate a draft using clauses, memory, prior draft, validator signal, and
                    # critique feedback
                    {
                        "product_description": product_description,
                        "clauses": relevant,
                        "memory_block": memory_block,
                        "previous_draft": previous_draft,
                        "validator_signal": signal if previous_draft else None,
                        "critique_feedback": critique["feedback"] if previous_draft else None,
                    }
                )
                signal = self.validator.validate(
                    draft
                )  # Validate the draft with deterministic checks
                critique = critic(
                    {"clauses": relevant}, draft, signal
                )  # Evaluate the draft using the validator signal and rule-based model judgment
                current_issues = set(critique["issues"])

                history.append(
                    {  # Record iteration history for observability and debugging
                        "outer": outer,
                        "inner": inner,
                        "coverage": signal.coverage_ratio,
                        "status": critique["status"],
                        "issues": sorted(current_issues),
                    }
                )

                if (
                    critique["status"] == "acceptable"
                ):  # Stop when the report satisfies the evaluator and store a success memory
                    self.memory.store(
                        EpisodicRecord(
                            task_signature=task_signature,
                            outcome="success",
                            insight=f"Clean report in {total_iters} iterations.",
                        )
                    )
                    return AgentResult(
                        final_report=draft,
                        final_signal=signal,
                        plan=plan,
                        iterations=total_iters,
                        history=history,
                        termination="acceptable",
                    )

                if (
                    previous_draft is not None
                    and current_issues
                    and current_issues == previous_issues
                    # Convergence check: unchanged blockers indicate oscillation rather than
                    # improvement
                ):
                    self.memory.store(
                        EpisodicRecord(
                            task_signature=task_signature,
                            outcome="success",
                            insight=(
                                f"Converged with stable open issues after {total_iters} "
                                f"iterations: {sorted(current_issues)}"
                            ),
                        )
                    )
                    return AgentResult(
                        final_report=draft,
                        final_signal=signal,
                        plan=plan,
                        iterations=total_iters,
                        history=history,
                        termination="converged",
                    )

                previous_draft = (
                    draft  # Carry the current draft and issues into the next reflection iteration
                )
                previous_issues = current_issues

            plan = planner(
                {  # Revise the plan when the inner loop cannot resolve the issues
                    "product_description": product_description,
                    "clauses": relevant,
                    "previous_plan": plan,
                    "execution_feedback": critique["feedback"],
                }
            )

        self.memory.store(
            # Store a failure memory when both output-level and planning-level reflection are
            # exhausted
            EpisodicRecord(
                task_signature=task_signature,
                outcome="failure",
                insight=f"Exhausted iterations. Last issues: {sorted(previous_issues)}",
            )
        )
        return AgentResult(
            final_report=previous_draft or DraftReport(summary="", clauses=[]),
            final_signal=signal,
            plan=plan,
            iterations=total_iters,
            history=history,
            termination="exhausted",
        )
