# notfair-nextjs-blog

Render your [NotFair SEO](https://notfair.co/seo) exchange posts on
a Next.js (App Router) blog. Pull model: your site fetches published posts
server-side from the NotFair content API with a private key — nothing is ever
pushed to your infrastructure.

## Setup

1. Install the package:

```bash
npm install notfair-nextjs-blog
```

2. In the NotFair SEO dashboard, create a **Next.js / headless**
   integration and copy the site API key (shown once).
3. Add it to your environment — server-side only, never `NEXT_PUBLIC_`:

```bash
NOTFAIR_SEO_API_KEY=nfbl_...
```

4. Publish NotFair posts under `/blog/{slug}`. The dashboard derives the
   verification URL automatically. If `/blog` already exists, merge NotFair
   into it as an additional source rather than replacing the route.

## Minimal app/blog

`app/blog/page.tsx`:

```tsx
import Link from "next/link";
import { getSeoPosts } from "notfair-nextjs-blog";

export default async function BlogIndex() {
  const posts = await getSeoPosts();
  return (
    <main>
      <h1>Blog</h1>
      {posts.map((p) => (
        <article key={p.slug}>
          <Link href={`/blog/${p.slug}`}>{p.title}</Link>
        </article>
      ))}
    </main>
  );
}
```

`app/blog/[slug]/page.tsx`:

```tsx
import { notFound } from "next/navigation";
import { getSeoPost } from "notfair-nextjs-blog";

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getSeoPost(slug);
  if (!post) notFound();
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content_html }} />
    </article>
  );
}
```

Responses revalidate hourly by default (`{ revalidate }` option to change).

## Existing `/blog`

Keep your current blog queries, components, metadata, and styling. Native posts
win slug collisions; NotFair fills only the remaining index entries and slugs.

For the index, fetch both sources in parallel and merge them without reshaping
your existing post type:

```tsx
import { getSeoPosts, mergeBlogPosts } from "notfair-nextjs-blog";

const [existingPosts, seoPosts] = await Promise.all([
  getExistingPosts(),
  getSeoPosts(),
]);
const posts = mergeBlogPosts(existingPosts, seoPosts);

// Branch on item.source and render each source with the site's existing cards.
// Every item still links to /blog/${item.post.slug}.
```

For `app/blog/[slug]/page.tsx`, resolve the existing source first and call
NotFair only as a fallback:

```tsx
import { notFound } from "next/navigation";
import { getBlogPostWithSeoFallback } from "notfair-nextjs-blog";

const result = await getBlogPostWithSeoFallback(slug, getExistingPost);
if (!result) notFound();

if (result.source === "existing") {
  return <ExistingPost post={result.post} />;
}

return (
  <article>
    <h1>{result.post.title}</h1>
    <div dangerouslySetInnerHTML={{ __html: result.post.content_html }} />
  </article>
);
```

Apply the same native-first lookup in `generateMetadata`. Do not call
`notFound()` until both sources return no post.

## API

- `getSeoPosts({ revalidate? })` → `[{ id, title, slug, published_at, created_at }]`
- `getSeoPost(slug, { revalidate? })` → adds `content_html`, or `null`
- `mergeBlogPosts(existing, seo)` → discriminated list; existing slugs win
- `getBlogPostWithSeoFallback(slug, getExistingPost, { revalidate? })` →
  `{ source, post }`, or `null`
