from typing import Dict, Any
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import label_binarize
import numpy as np

class AssuranceEngine:
    """PhyState Evidence Reconciliation and Decision State Engine."""

    def __init__(self, cloud_threshold: float = 0.80, max_age_days: float = 20.0):
        self.cloud_threshold = cloud_threshold
        self.max_age_days = max_age_days

    def evaluate_claim(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Reconciles evidence and emits decision state with confidence score."""
        
        # 1. Check Data Freshness and Obstruction Guardrails
        if evidence["cloud_cover"] >= self.cloud_threshold or evidence["data_age_days"] > self.max_age_days:
            return {
                "decision_state": "UNDERDETERMINED",
                "confidence_score": 0.20,
                "reason": "Excessive cloud obstruction or evidence latency limit exceeded."
            }

        # 2. Reconcile Multimodal Phenology Divergence
        ndvi = evidence["ndvi_mean"]
        sar = evidence["sar_vv_vh"]
        
        # Expectation for active healthy crop claim: NDVI > 0.60 AND SAR > -14.0 dB
        if ndvi >= 0.60 and sar >= -14.0:
            confidence = min(0.99, 0.5 * (ndvi + (sar + 20) / 10))
            return {
                "decision_state": "SUPPORTED",
                "confidence_score": confidence,
                "reason": "Multimodal evidence supports expected crop vigor."
            }
        else:
            confidence = min(0.99, 1.0 - ndvi)
            return {
                "decision_state": "CONFLICTED",
                "confidence_score": confidence,
                "reason": "Physical evidence diverges significantly from claim."
            }

    def evaluate_dataset(self, dataset):
        results = []
        confidence_scores = []
        
        for sample in dataset:
            res = self.evaluate_claim(sample)
            results.append(res["decision_state"])
            
            # Map state to probability score for multi-class AUC calculation
            if res["decision_state"] == "SUPPORTED":
                score = [0.0, 0.0, res["confidence_score"]]
            elif res["decision_state"] == "CONFLICTED":
                score = [res["confidence_score"], 0.0, 0.0]
            else:
                score = [0.0, 1.0 - res["confidence_score"], 0.0]
            confidence_scores.append(score)

        return results, np.array(confidence_scores)

    @staticmethod
    def calculate_auc(y_true, y_score):
        """Calculates macro-averaged ROC-AUC score across decision states."""
        classes = ["CONFLICTED", "UNDERDETERMINED", "SUPPORTED"]
        y_true_bin = label_binarize(y_true, classes=classes)
        auc = roc_auc_score(y_true_bin, y_score, average="macro", multi_class="ovr")
        return auc