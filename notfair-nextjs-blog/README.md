# notfair-nextjs-blog

Render your [NotFair Backlinks](https://notfair.co/backlinks) exchange posts on
a Next.js (App Router) blog. Pull model: your site fetches published posts
server-side from the NotFair content API with a private key — nothing is ever
pushed to your infrastructure.

## Setup

1. Install the package:

```bash
npm install notfair-nextjs-blog
```

2. In the NotFair Backlinks dashboard, create a **Next.js / headless**
   integration and copy the site API key (shown once).
3. Add it to your environment — server-side only, never `NEXT_PUBLIC_`:

```bash
NOTFAIR_BACKLINKS_API_KEY=nfbl_...
```

4. Set your integration's **public post URL pattern** to where these pages
   render (e.g. `https://yoursite.com/blog/{slug}`) — link verification crawls
   it, and hosted links only earn credits once verified.

## Minimal app/blog

`app/blog/page.tsx`:

```tsx
import Link from "next/link";
import { getBacklinksPosts } from "notfair-nextjs-blog";

export default async function BlogIndex() {
  const posts = await getBacklinksPosts();
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
import { getBacklinksPost } from "notfair-nextjs-blog";

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getBacklinksPost(slug);
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

- `getBacklinksPosts({ revalidate? })` → `[{ id, title, slug, published_at, created_at }]`
- `getBacklinksPost(slug, { revalidate? })` → adds `content_html`, or `null`
