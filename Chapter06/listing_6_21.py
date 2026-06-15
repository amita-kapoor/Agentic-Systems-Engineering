@dataclass
class AgentResult:  #A
    final_report: DraftReport
    final_signal: ValidationSignal
    plan: Plan
    iterations: int
    history: list[dict]
    termination: Literal["acceptable", "converged", "exhausted"]


class ComplianceAgent:
    def __init__(self, framework, validator, memory, max_inner_iters=3, max_outer_iters=2):
        self.framework = framework  #B
        self.validator = validator  #C
        self.memory = memory  #D
        self.max_inner_iters = max_inner_iters
        self.max_outer_iters = max_outer_iters

    def run(self, product_description: str) -> AgentResult:
        task_signature = f"compliance_report::{product_description[:60]}"  #E
        relevant = self.framework.retrieve_relevant(product_description)  #F
        past = self.memory.retrieve(task_signature)  #G
        memory_block = self.memory.as_prompt_block(past)  #H

        plan = planner({"product_description": product_description, "clauses": relevant})  #I

        history: list[dict] = []
        previous_draft: Optional[DraftReport] = None
        signal = ValidationSignal()
        critique: Critique = {"status": "needs_revision", "issues": [], "feedback": ""}
        previous_issues: set[str] = set()
        total_iters = 0

        for outer in range(self.max_outer_iters):  #J
            for inner in range(self.max_inner_iters):  #K
                total_iters += 1
                draft = generator({  #L
                    "product_description": product_description,
                    "clauses": relevant,
                    "memory_block": memory_block,
                    "previous_draft": previous_draft,
                    "validator_signal": signal if previous_draft else None,
                    "critique_feedback": critique["feedback"] if previous_draft else None,
                })
                signal = self.validator.validate(draft)  #M
                critique = critic({"clauses": relevant}, draft, signal)  #N
                current_issues = set(critique["issues"])

                history.append({  #O
                    "outer": outer,
                    "inner": inner,
                    "coverage": signal.coverage_ratio,
                    "status": critique["status"],
                    "issues": sorted(current_issues),
                })

                if critique["status"] == "acceptable":  #P
                    self.memory.store(EpisodicRecord(
                        task_signature=task_signature,
                        outcome="success",
                        insight=f"Clean report in {total_iters} iterations.",
                    ))
                    return AgentResult(
                        final_report=draft,
                        final_signal=signal,
                        plan=plan,
                        iterations=total_iters,
                        history=history,
                        termination="acceptable",
                    )

                if previous_draft is not None and current_issues and current_issues == previous_issues:  #Q
                    self.memory.store(EpisodicRecord(
                        task_signature=task_signature,
                        outcome="success",
                        insight=f"Converged with stable open issues after {total_iters} iterations: {sorted(current_issues)}",
                    ))
                    return AgentResult(
                        final_report=draft,
                        final_signal=signal,
                        plan=plan,
                        iterations=total_iters,
                        history=history,
                        termination="converged",
                    )

                previous_draft = draft  #R
                previous_issues = current_issues

            plan = planner({  #S
                "product_description": product_description,
                "clauses": relevant,
                "previous_plan": plan,
                "execution_feedback": critique["feedback"],
            })

        self.memory.store(EpisodicRecord(  #T
            task_signature=task_signature,
            outcome="failure",
            insight=f"Exhausted iterations. Last issues: {sorted(previous_issues)}",
        ))
        return AgentResult(
            final_report=previous_draft or DraftReport(summary="", clauses=[]),
            final_signal=signal,
            plan=plan,
            iterations=total_iters,
            history=history,
            termination="exhausted",
        )
