import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  output: 'export',
  basePath: '/docs-site',         // nome do repositório
  assetPrefix: '/docs-site',      // garante que os estilos/scripts carregam corretamente
};

export default withMDX(config);
