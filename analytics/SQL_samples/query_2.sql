/*
QUERY 2
*/
SELECT
        tx.client_id
    ,   SUM(CASE WHEN p_nm.product_type in ('MEUBLE') THEN (tx.prod_price * tx.prod_qty) ELSE NULL END) as ventes_meuble
    ,   SUM(CASE WHEN p_nm.product_type in ('DECO') THEN (tx.prod_price * tx.prod_qty) ELSE NULL END) as ventes_deco
FROM `TRANSACTION` as tx
LEFT JOIN `PRODUCT_NOMENCLATURE` as p_nm on p_nm.product_id = tx.prop_id
WHERE 
        tx.date >= '2019-01-01'
    AND tx.date < '2020-01-01'
GROUP BY 1
;