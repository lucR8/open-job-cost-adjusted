-- fct_offer_enriched : à remplacer par de vraies jointures (offres × loyers × IPC)
select o.dummy_id as offer_id, 1.0 as adjusted_salary_index
from {{ ref("stg_offers") }} o
