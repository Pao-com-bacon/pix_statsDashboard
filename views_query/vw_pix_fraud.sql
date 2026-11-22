USE "pix";

CREATE OR REPLACE VIEW "main"."vw_pix_fraud" AS
SELECT
    STRPTIME(AnoMes::VARCHAR, '%Y%m')::DATE AS reference_data_frauds,
    * EXCLUDE(AnoMes)
FROM "main"."raw_frauds"
WHERE reference_data_frauds >= '2025-01-01 00:00:00'
