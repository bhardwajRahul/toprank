/**
 * notfair-nextjs-blog — server-side client for the NotFair SEO
 * content API (the "Next.js / headless" integration).
 *
 * Usage: set NOTFAIR_SEO_API_KEY in your environment (server-only —
 * never expose it to the client bundle), then call these from Server
 * Components or route handlers. See README.md for a copy-paste app/blog.
 */

const API_BASE = process.env.NOTFAIR_SEO_API_URL ?? "https://notfair.co/api/seo/content";

export type SeoPostSummary = {
  id: number;
  title: string;
  slug: string;
  meta_description: string | null;
  tags: string[];
  /** Generated title-card image (1200×630) — thumbnail / og:image. */
  image_url: string;
  reading_time_minutes: number | null;
  published_at: string | null;
  created_at: string;
};

export type SeoPost = SeoPostSummary & { content_html: string };

function apiKey(): string {
  const key = process.env.NOTFAIR_SEO_API_KEY;
  if (!key) {
    throw new Error(
      "notfair-nextjs-blog: NOTFAIR_SEO_API_KEY is not set. Create the key in your NotFair SEO dashboard (Integrations → Next.js).",
    );
  }
  return key;
}

/** Next.js extends fetch's RequestInit with `next` — typed locally so the
 *  package builds standalone without Next's global type augmentation. */
type NextFetchInit = RequestInit & { next?: { revalidate: number } };

async function contentFetch(path: string, revalidate: number): Promise<Response> {
  const init: NextFetchInit = {
    headers: { authorization: `Bearer ${apiKey()}` },
    // Cached server-side; posts publish on a schedule, hourly is plenty.
    next: { revalidate },
  };
  return fetch(`${API_BASE}${path}`, init);
}

/** List published exchange posts (no bodies — cheap for blog indexes). */
export async function getSeoPosts(
  opts: { revalidate?: number } = {},
): Promise<SeoPostSummary[]> {
  const res = await contentFetch("", opts.revalidate ?? 3600);
  if (!res.ok) return [];
  const body = (await res.json().catch(() => null)) as { posts?: SeoPostSummary[] } | null;
  return body?.posts ?? [];
}

/** Fetch one published post with its full HTML body. Returns null if the
 *  slug doesn't exist or isn't published. */
export async function getSeoPost(
  slug: string,
  opts: { revalidate?: number } = {},
): Promise<SeoPost | null> {
  const res = await contentFetch(`?slug=${encodeURIComponent(slug)}`, opts.revalidate ?? 3600);
  if (!res.ok) return null;
  const body = (await res.json().catch(() => null)) as { post?: SeoPost } | null;
  return body?.post ?? null;
}
