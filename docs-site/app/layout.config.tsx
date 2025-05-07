import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { basePath } from './config';
import Image from 'next/image';

/**
 * Shared layout configurations
 *
 * you can customise layouts individually from:
 * Home Layout: app/(home)/layout.tsx
 * Docs Layout: app/docs/layout.tsx
 */
export const baseOptions: BaseLayoutProps = {
  nav: {
    title: (
      <>
        <Image
          src={`${basePath}/public/yakelogo.png`}
          width={24}
          height={24}
          alt="YAKE Logo"
          style={{ marginRight: '8px' }}
        />
        YAKE!
      </>
    ),
  },
};