-- Applied to Project GPT OS Supabase on 2026-10-18.
-- Private NOLOGIN role with access to an allowlisted, read-only inventory function.
-- Do NOT grant this role to anon/authenticated or expose the internal schema publicly.
CREATE SCHEMA IF NOT EXISTS gpt_os_internal;
REVOKE ALL ON SCHEMA gpt_os_internal FROM PUBLIC;
DO $$ BEGIN
 IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'gpt_os_registry_reader') THEN
  CREATE ROLE gpt_os_registry_reader NOLOGIN;
 END IF;
END $$;
GRANT USAGE ON SCHEMA gpt_os_internal TO gpt_os_registry_reader;
CREATE OR REPLACE FUNCTION gpt_os_internal.source_inventory()
RETURNS TABLE(provider text, external_id text, name text, external_url text, source_path text)
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = pg_catalog AS $$
 SELECT r.provider, r.external_id, i.name, r.external_url, r.source_path
 FROM public.registry_external_refs r
 JOIN public.registry_items i ON i.id = r.registry_item_id
 WHERE i.item_type = 'source'
$$;
REVOKE ALL ON FUNCTION gpt_os_internal.source_inventory() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION gpt_os_internal.source_inventory() TO gpt_os_registry_reader;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM gpt_os_registry_reader;
