import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';;
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
          src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAgCAMAAADZqYNOAAAA6lBMVEVHcEynUhCGi6FIYJBfDAoAO4AAACoAAFIIDlynWghtZYC+hDZQTm6TiZW2jbijPS1nSZTSqtCoX4S+dw+MR3u9g8yZRm60RAC2bRKrNgCZFwClgaYAPHCvkarNnT5sdJF1fpzOoUSkdjXnuwDxxwC8bQjLhgDTjwPYmQb7ywL+5gDJSRjrqUPufADru1L3lwCLW0l1UmLwqgDwzGjNbgrUgADx0AD78XHEbkWajn2ydD/BX0yaUoDacwCySTzUWCCwU3PSkB7HZwD5vgCZbHK7dBL42gDJgVaZZj7+81/GbS7x3IH67Y2YUFX9WlebAAAAI3RSTlMAjMGMLzgEDRRl5ve77z6iL7CY4WJigqG4ckzIX/rfuLnX81RadVcAAADHSURBVCiR3Y/FFsIwFESDVKC4uyVVpIUWd/f//x2KLtKEPcxqzrvnnZkB4F/EfoP80Oe88W8XFHmMcYGD8LJu0YXBgiH1TO5hPSMRg8xG3mn9RxpjSI7UwB5qx9I9oS3HnT3LA6idvQD4JcVLmOE+oX4VVLYwQ4D2l9W71ASocETKtrsIIYiv+RS/KqoqU6C9dNBRlzTIgmJ33SDH3pVfdVqkPU9NLL2Vo0F+MdXNLI0mZ81mI02j0fG8Xg/TaCiWSkSopX5EN7VQEdbEal6JAAAAAElFTkSuQmCC"
          width="24"
          height="24"
          alt="YAKE Logo"
          style={{ marginRight: '8px' }}
        />
        YAKE!
      </>
    ),
  },
};