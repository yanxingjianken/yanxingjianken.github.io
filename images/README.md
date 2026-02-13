# Images Directory

This directory contains images used throughout the website, including portfolio images, profile pictures, and other visual assets.

## Uploading Images

When uploading new images to this directory:

1. **File Size Limits**: GitHub has a file size limit of 100MB per file. Keep images under this limit.
2. **Recommended Image Sizes**: 
   - Portfolio images: 800-1200px width
   - Profile images: 400-600px width
   - Thumbnails: 200-300px width
3. **Supported Formats**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`
4. **File Naming**: Use lowercase letters, numbers, and underscores/hyphens. Avoid spaces and special characters.

## Using Images in Portfolio Items

To use an image in your portfolio item, add it to the excerpt in the frontmatter:

```markdown
---
title: "Your Project Title"
excerpt: "Brief description<br/><img src='/images/your-image.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
---
```

## Troubleshooting Upload Issues

If you encounter errors when uploading files through GitHub's web interface:

1. **Check file size**: Ensure the file is under 100MB
2. **Verify file format**: Use standard image formats (JPG, PNG, GIF)
3. **Check filename**: Remove spaces and special characters from filenames
4. **Try uploading via Git CLI**: Use `git add`, `git commit`, and `git push` commands
5. **Clear browser cache**: Sometimes browser issues can prevent uploads

## Placeholder Images

Some images in this directory are placeholders (grayscale images):
- `4_bases_decomposition.png` - Placeholder for Four-Basis Decomposition project
- `ensemble_gp.png` - Placeholder for Ensemble-Consistent GP project

To replace these with actual images:
1. Download the real images from the original source (see MANUAL_IMAGE_DOWNLOAD.md)
2. Replace the placeholder files with the downloaded images
3. Commit and push the changes

## Current Images

This directory contains:
- Portfolio project images
- Profile pictures
- Icon and favicon files
- Background images for various sections
- Placeholder images (to be replaced with actual images)

