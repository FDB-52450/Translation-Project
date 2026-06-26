import numpy as np
import json


def writeToFile(results):
    clean_results = extract_clean_ocr(results)
    json_safe_results = make_json_safe(clean_results)

    with open("rawData.json", "w") as f:
        json.dump(json_safe_results, f, indent=4)


def extract_clean_ocr(results):
    clean = []

    for page in results:
        clean.append({
            "rec_texts": page.get("rec_texts", []),
            "rec_scores": page.get("rec_scores", []),
            "rec_polys": page.get("rec_polys", [])
        })

    return clean


def make_json_safe(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    return obj