USE "pix";

CREATE OR REPLACE VIEW vw_pix_cad AS
SELECT
    DataGraficosPix AS reference_data_cad,
    *
FROM "main"."raw_cadastre"
WHERE DataGraficosPix >= '2025-01-01 00:00:00'

