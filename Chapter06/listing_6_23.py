product_2 = (  #A
    "QuickPay is a payment gateway for small merchants. It encrypts data with AES-256, "
    "logs all access events, retains data for 60 days, and does not perform cross-border "
    "transfers."
)

result_2 = agent.run(product_2)  #B

print(f"\nSecond run finished in {result_2.iterations} iterations.")
print(f"Coverage: {result_2.final_signal.coverage_ratio}, "
      f"clean={result_2.final_signal.is_clean}\n")
print("Episodic memory now contains:")
print("-" * 80)

for rec in MEMORY._records:  #C
    print(f"[{rec.outcome}] {rec.task_signature}")
    print(f"  insight: {rec.insight}\n")
