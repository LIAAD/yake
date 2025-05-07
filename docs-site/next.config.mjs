import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

const REPO_NAME = 'yakerf'; 

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  output: 'export',
  // Configuração para GitHub Pages
  basePath: process.env.NODE_ENV === 'production' ? `/${REPO_NAME}` : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? `/${REPO_NAME}/` : '',
  images: {
    unoptimized: true,
  },
  // Desabilitar trailing slash para compatibilidade com GitHub Pages
  trailingSlash: false,
};

export default withMDX(config);