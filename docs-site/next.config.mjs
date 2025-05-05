import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  output: 'export',
  // Configuração para GitHub Pages
  basePath: process.env.NODE_ENV === 'production' ? '/yakerf' : '',
  // Para garantir que as imagens sejam exportadas corretamente para páginas estáticas
  images: {
    unoptimized: true,
  },
  // Desabilitar trailing slash para compatibilidade com GitHub Pages
  trailingSlash: false,
};

export default withMDX(config);