from generator import EvidenceGenerator
from engine import AssuranceEngine
from tabulate import tabulate

def run_prototype_validation():
    print("==================================================================")
    print("   PHYSTATE: PHYSICAL REALITY ASSURANCE ENGINE (PROTOTYPE TEST)  ")
    print("==================================================================\n")

    # 1. Generate Synthetic Scenarios
    generator = EvidenceGenerator(seed=42)
    dataset, y_true = generator.generate_scenario_data(n_samples_per_scenario=100)
    
    # 2. Evaluate with Engine
    engine = AssuranceEngine(cloud_threshold=0.80, max_age_days=20.0)
    y_pred, y_scores = engine.evaluate_dataset(dataset)

    # 3. Compute Metrics
    auc = engine.calculate_auc(y_true, y_scores)
    
    # 4. Summary Table
    scenario_counts = {}
    for sample, pred in zip(dataset, y_pred):
        scen = sample["scenario_name"]
        if scen not in scenario_counts:
            scenario_counts[scen] = {"EXPECTED": sample["true_label"], "SUPPORTED": 0, "CONFLICTED": 0, "UNDERDETERMINED": 0}
        scenario_counts[scen][pred] += 1

    table_data = []
    for scen, counts in scenario_counts.items():
        table_data.append([
            scen,
            counts["EXPECTED"],
            counts["SUPPORTED"],
            counts["CONFLICTED"],
            counts["UNDERDETERMINED"]
        ])

    headers = ["Scenario Name", "Target State", "Pred: SUPPORTED", "Pred: CONFLICTED", "Pred: UNDERDETERMINED"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\n[Validation Result] Multi-Sensor Separation Macro ROC-AUC Score: {auc:.4f}")
    
    if auc >= 0.99:
        print("[SUCCESS] Algorithmic reconciliation logic verified. AUC ~1.0 achieved.\n")

if __name__ == "__main__":
    run_prototype_validation()