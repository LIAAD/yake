import { Metadata } from 'next';
import { basePath } from '../config';
import './global.css';

export const metadata: Metadata = {
  title: {
    template: '%s | YAKE!',
    default: 'YAKE! Documentation',
  },
  description: 'Documentation for YAKE!',
  // Ajuste para caminhos absolutos que respeitam o basePath
  icons: {
    icon: `${basePath}/favicon.ico`,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}