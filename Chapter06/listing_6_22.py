agent = ComplianceAgent(  #A
    framework=FRAMEWORK,
    validator=VALIDATOR,
    memory=MEMORY,
    max_inner_iters=3,
    max_outer_iters=2,
)

product = (  #B
    "PayLite is a small payments service that stores customer card numbers "
    "and processes transactions. Cardholder data is encrypted with AES-256. "
    "Access is logged to an internal SIEM. The team has not formally documented "
    "data retention or cross-border transfer practices."
)

result = agent.run(product)  #C

print(f"\nFinished in {result.iterations} iterations.")
print(f"Termination: {result.termination}")
print(f"Final coverage: {result.final_signal.coverage_ratio}")
print(f"Validator clean: {result.final_signal.is_clean}\n")

print("Iteration history")
print("-" * 80)

for row in result.history:  #D
    issues = row["issues"] if row["issues"] else "none"
    print(
        f"outer={row['outer']} inner={row['inner']} "
        f"coverage={row['coverage']} status={row['status']} "
        f"issues={issues}"
    )

print()
print("Final report")
print("-" * 80)
print(json.dumps(result.final_report.model_dump(), indent=2))  #E
