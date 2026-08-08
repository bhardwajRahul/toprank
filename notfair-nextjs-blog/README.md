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

4. Set your integration's **public post URL pattern** to where these pages
   render (e.g. `https://yoursite.com/blog/{slug}`) — link verification crawls
   it, and hosted links only earn credits once verified.

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

## API

- `getSeoPosts({ revalidate? })` → `[{ id, title, slug, published_at, created_at }]`
- `getSeoPost(slug, { revalidate? })` → adds `content_html`, or `null`
