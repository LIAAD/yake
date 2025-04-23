import { defineDocs, defineConfig, defineCollections } from 'fumadocs-mdx/config';

// Options: https://fumadocs.vercel.app/docs/mdx/collections#define-docs
export const docs = defineCollections({
  type: 'doc',
  dir: 'content/docs',
});

export const meta = defineCollections({
  type: 'meta',
  dir: 'content/docs',
});


export default defineConfig({
  mdxOptions: {
    // MDX options
  },
});
