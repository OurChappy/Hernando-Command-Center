-- SELECT only. Export the single snapshot value privately; never commit live rows.
-- Use an existing authorized read-only connection. No roles or schema are changed.
select jsonb_build_object(
  'schema_version', 1,
  'observed_at', current_timestamp,
  'projects', (select coalesce(jsonb_agg(jsonb_build_object('id', id, 'project_code', project_code)), '[]'::jsonb) from public.projects),
  'registry_items', (select coalesce(jsonb_agg(jsonb_build_object('id', id, 'project_id', project_id, 'status', status)), '[]'::jsonb) from public.registry_items),
  'registry_external_refs', (select coalesce(jsonb_agg(jsonb_build_object('registry_item_id', registry_item_id, 'provider', provider, 'external_id', external_id)), '[]'::jsonb) from public.registry_external_refs),
  'registry_dependencies', (select coalesce(jsonb_agg(jsonb_build_object('source_item_id', source_item_id, 'target_item_id', target_item_id, 'dependency_type', dependency_type)), '[]'::jsonb) from public.registry_dependencies)
) as snapshot;
