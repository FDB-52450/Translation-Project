# Este archivo tendra como objetivo limpiar el texto obtenido por el OCR, lo que incluye:
# - Eliminar resultados de baja confianza
# - Eliminar caracteres no deseados (como saltos de línea, tabulaciones, etc.)
# - Normalizar tipos np (numpy) a tipos nativos de Python (como convertir np.int64 a int, np.float64 a float, etc.)
# - Convertir el texto a un formato más limpio y estructurado para facilitar su posterior procesamiento por el modelo de lenguaje.

def normalize_results(raw_results):
    clean_results = []
    
    for page in raw_results:
        rec_texts = page.get("rec_texts", [])
        rec_scores = page.get("rec_scores", [])
        rec_polys = page.get("rec_polys", [])
        
        clean_page = {
            "rec_texts": [],
            "rec_scores": [],
            "rec_polys": []
        }
        
        for text, score, poly in zip(rec_texts, rec_scores, rec_polys):
            if score >= 0.5:  # Filtrar por confianza
                clean_page["rec_texts"].append(text.strip())  # Eliminar espacios extra
                clean_page["rec_scores"].append(float(score))  # Convertir a float nativo
                clean_page["rec_polys"].append(poly)  # Mantener las coordenadas tal cual
        
        clean_results.append(clean_page)
    
    return clean_results

