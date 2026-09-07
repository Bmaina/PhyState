# PhyState: Physical Reality Assurance Engine

---

## 📌 Executive Overview

**PhyState** acts as an independent physical assurance layer for AI agents operating in agricultural finance, supply chain compliance, and asset management. By cross-referencing and reconciling multi-modal physical evidence streams—including **Synthetic Aperture Radar (Sentinel-1 SAR)**, **optical vegetation indices (Sentinel-2 NDVI)**, and **ERA5 climate data**—PhyState verifies whether digital assertions reflect ground reality before capital is deployed.

> **Key Value Proposition:** Prevents autonomous agents from disbursing funds or triggering workflows based on stale, incomplete, or compromised database claims.

---

## ⚡ System Architecture

PhyState intercepts proposed agent actions, parses required physical state assumptions, queries spatial evidence streams, and emits a machine-readable **Assurance Object**.

```text
┌─────────────────────────┐
│     Proposed Action     │  (e.g., Disburse Loan Tranche for Farm X)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    Claim Parser Engine  │  (Extracts boundaries, crop phenology, temporal bounds)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐     ┌───────────────────────────────────────────────┐
│   Evidence Reconciler   │ ◄───┤ • Sentinel-1 SAR (VV/VH Backscatter)          │
│  (Multi-Sensor Fusion)  │     │ • Sentinel-2 Optical (NDVI Surface Refl)      │
└────────────┬────────────┘     │ • ERA5 Climate & CHIRPS Anomaly Grids         │
             │                  └───────────────────────────────────────────────┘
             ▼
┌─────────────────────────┐
│    Assurance Object     │  ==> [ SUPPORTED | CONFLICTED | UNDERDETERMINED ]
└─────────────────────────┘

```

---

## 🚦 Decision State Protocol

PhyState enforces strict deterministic guardrails to evaluate physical claims:

| Decision State | Trigger Condition | System Action |
| --- | --- | --- |
|  | Multi-sensor physical evidence confirms required physical assumptions within confidence thresholds. | **PROCEED:** Agent executes proposed transaction. |
|  | Independent physical evidence directly contradicts the claim (e.g., bare soil during peak season). | **FLAG:** Transaction blocked; escalated to risk officer. |
|  | Cloud obstruction ($>80\%$), stale sensor latency ($>20\text{ days}$), or high signal noise. | **ABSTAIN:** Action halted due to physical uncertainty. |

---

## 📊 Phase 1 Benchmark Results

The Phase 1 synthetic validation suite evaluates multi-sensor phenology divergence across 5 core agricultural scenarios:

```text
================================================================================
          PHYSTATE: PHYSICAL REALITY ASSURANCE ENGINE (BENCHMARK)
================================================================================

+─────────────────────────────────+──────────────────+──────────────────+
| Scenario Name                   | Target State     | Evaluation Result|
+─────────────────────────────────+──────────────────+──────────────────+
| SUPPORTED_NORMAL_CROP           | SUPPORTED        | 100% Match       |
| CONFLICTED_CROP_FAILURE         | CONFLICTED       | 100% Match       |
| CONFLICTED_UNPLANTED_LAND       | CONFLICTED       | 100% Match       |
| UNDERDETERMINED_HIGH_CLOUD      | UNDERDETERMINED  | 100% Match       |
| UNDERDETERMINED_SENSOR_LATENCY  | UNDERDETERMINED  | 100% Match       |
+─────────────────────────────────+──────────────────+──────────────────+

[Validation Metric] Multi-Sensor Separation Macro ROC-AUC: 1.0000

```

---

## 📁 Repository Structure

```text
PhyState/
├── .gitignore             # Production Git ignore rules
├── README.md              # System Architecture & Documentation
├── requirements.txt       # Dependencies (NumPy, Scikit-Learn, Tabulate)
└── src/
    ├── __init__.py        # Module initialization
    ├── engine.py          # Evidence Reconciliation Engine & ROC-AUC evaluator
    ├── generator.py       # Multi-sensor temporal evidence generator
    └── main.py            # Main execution CLI entry point

```

---

## 🚀 Quickstart Guide

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/PhyState.git
cd PhyState

# Install dependencies
pip install -r requirements.txt

```

### 2. Run Validation Suite

```bash
python src/main.py

```

---

## 💻 API Integration Example

```python
from src.engine import AssuranceEngine

# Initialize PhyState Engine with custom enterprise guardrails
engine = AssuranceEngine(cloud_threshold=0.80, max_age_days=20.0)

# Agent submits incoming physical claim payload
evidence_payload = {
    "claim_id": "CLM-2026-8891",
    "asset_id": "FARM-KE-4022",
    "ndvi_mean": 0.72,
    "sar_vv_vh": -10.5,
    "rain_anomaly": 0.95,
    "cloud_cover": 0.12,
    "data_age_days": 2.5
}

# Evaluate claim against physical ground truth
assurance_object = engine.evaluate_claim(evidence_payload)

if assurance_object["decision_state"] == "SUPPORTED":
    # Autonomous agent proceeds with execution
    execute_transaction(evidence_payload["claim_id"])

```

---

## 🗺️ Product Roadmap

* [x] **Phase 1: Synthetic Prototype Validation**
* Multi-sensor simulation framework.
* Deterministic decision engine logic ($\text{ROC-AUC} \approx 1.000$).


* [ ] **Phase 2: Live Copernicus STAC Integration**
* Direct API integration with Sentinel-1/2 planetary data.
* Real-time satellite query pipeline for bounding box geometry.


* [ ] **Phase 3: Agentic Framework SDKs**
* Native connectors for LangChain, AutoGen, and LlamaIndex agent workflows.



---

## 📜 License

This project is open-source under the **MIT License**.

---

