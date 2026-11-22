USE "pix";

CREATE OR REPLACE VIEW vw_pix_economic AS
SELECT 
    STRPTIME(AnoMes::VARCHAR, '%Y%m')::DATE AS data_referencia,
    SUM(qtpagador) AS total_pagadores,
    SUM(qtrecebedor) AS total_recebedores,
    SUM(qtlanliq) AS total_transacoes,
    SUM(vllanliq) AS valor_total,
    SUM(vlcompra) AS valor_compra,
    SUM(vldinespec) AS valor_especie
FROM raw_economic_activity
GROUP BY data_referencia
ORDER BY data_referencia;
