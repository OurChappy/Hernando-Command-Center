-- Read-only acceptance baseline for Project GPT OS.
-- Run before and after any separately approved controlled-write test.
-- No mutations, no elevated grants, no scheduling.
SELECT
  (SELECT count(*) FROM public.registry_items WHERE item_type='source') AS source_items,
  (SELECT count(*) FROM public.registry_external_refs) AS external_refs,
  (SELECT count(*) FROM public.registry_external_refs r LEFT JOIN public.registry_items i ON i.id=r.registry_item_id WHERE i.id IS NULL) AS dangling_refs,
  (SELECT count(*) FROM (
    SELECT provider,external_id FROM public.registry_external_refs GROUP BY 1,2 HAVING count(*)>1
  ) duplicates) AS duplicate_provider_ids,
  (SELECT count(*) FROM (
    SELECT item_type,item_code FROM public.registry_items GROUP BY 1,2 HAVING count(*)>1
  ) duplicates) AS duplicate_item_codes;
-- Baseline verified on 2026-10-18: 50, 50, 0, 0, 0.
-- For an approved *new* test source, expect 51/51 then 51/51 on rerun,
-- unless another legitimate inventory change occurred. Investigate all deviations.
