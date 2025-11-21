# PWA Icons Required

The following icon files need to be created and placed in `public/`:

1. **icon-192.png** - 192x192 pixels
   - Purpose: App icon for Android and iOS
   - Format: PNG with transparency
   - Location: `public/icon-192.png`

2. **icon-512.png** - 512x512 pixels
   - Purpose: App icon for Android and iOS (high resolution)
   - Format: PNG with transparency
   - Location: `public/icon-512.png`

## Icon Design Guidelines

- Use the Maya AI branding/logo
- Ensure icons are square (1:1 aspect ratio)
- Use transparent background
- Icons should be centered with padding
- Test on both light and dark backgrounds

## Quick Generation

You can use online tools like:
- https://realfavicongenerator.net/
- https://www.pwabuilder.com/imageGenerator
- https://favicon.io/

Or create them manually using design tools like:
- Figma
- Adobe Illustrator
- Canva

Once created, place the files in `omega-frontend/public/` and the PWA manifest will automatically reference them.

