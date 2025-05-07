import { Metadata } from 'next';
import { basePath } from './config';
import './global.css';

import { RootProvider } from 'fumadocs-ui/provider';
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: {
    template: '%s | YAKE!',
    default: 'YAKE! Documentation',
  },
  description: 'Documentation for YAKE!',
  icons: {
    icon: `<docs-site />yakelogo.png`,
    shortcut: `<docs-site />yakelogo.png`,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className} suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider>{children}</RootProvider>
      </body>
    </html>
  );
}
