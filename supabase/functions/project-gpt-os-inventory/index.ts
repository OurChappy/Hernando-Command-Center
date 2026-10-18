// Supabase Edge Function: private inventory for one approved GitHub Actions workflow.
// verify_jwt MUST be false: GitHub OIDC is not a Supabase-issued JWT.
// No route is public without signature and immutable workload-identity validation.
import { createRemoteJWKSet, jwtVerify } from "npm:jose@6";
import { createClient } from "npm:@supabase/supabase-js@2";

const issuer = "https://token.actions.githubusercontent.com";
const audience = "project-gpt-os-registry-reader";
const repositoryId = "1366820544";
const workflowRef = "OurChappy/Hernando-Command-Center/.github/workflows/project-gpt-os-bootstrap.yml@refs/heads/main";
const jwks = createRemoteJWKSet(new URL(issuer + "/.well-known/jwks"));
const reply = (status: number, message: string) =>
  Response.json({ error: message }, { status, headers: { "Cache-Control": "no-store" } });

export async function handler(req: Request): Promise<Response> {
  if (req.method !== "GET") return reply(405, "Method not allowed");
  const match = /^Bearer (\S+)$/.exec(req.headers.get("authorization") ?? "");
  if (!match) return reply(401, "Missing bearer token");
  try {
    const { payload } = await jwtVerify(match[1], jwks, {
      issuer, audience, algorithms: ["RS256"], clockTolerance: 30,
    });
    if (payload.repository_id !== repositoryId ||
        payload.job_workflow_ref !== workflowRef && payload.workflow_ref !== workflowRef ||
        payload.ref !== "refs/heads/main" ||
        payload.repository !== "OurChappy/Hernando-Command-Center") {
      return reply(403, "Unapproved workflow identity");
    }
  } catch {
    return reply(401, "Invalid workload identity");
  }
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) return reply(503, "Service unavailable");
  const client = createClient(url, key, { auth: { persistSession: false } });
  const output: Array<{provider:string;external_id:string;name:string;external_url:string|null;source_path:string|null}> = [];
  // Privileged credential exists only server-side. Explicitly select allowlisted fields.
  for (let start = 0; start < 100000; start += 500) {
    const { data, error } = await client.from("registry_external_refs")
      .select("provider,external_id,external_url,source_path,registry_items!inner(name,item_type)")
      .eq("registry_items.item_type", "source")
      .order("provider").order("external_id").range(start, start + 499);
    if (error) return reply(503, "Inventory unavailable");
    for (const row of data ?? []) {
      const item = row.registry_items as unknown as { name: string };
      output.push({ provider: row.provider, external_id: row.external_id, name: item.name,
        external_url: row.external_url, source_path: row.source_path });
    }
    if ((data ?? []).length < 500) break;
  }
  return Response.json({ schema_version: "1", sources: output }, {
    headers: { "Cache-Control": "no-store", "Content-Type": "application/json" },
  });
}

Deno.serve(handler);
