# Portfolio Image Issues - Google Drive Links

## Issue

Two portfolio items currently use Google Drive links for images:
1. `100_4_bases.html` - Four-Basis Decomposition project
2. `200_ensemble_conditional_gp.html` - Ensemble-Consistent GP project

## Current Solution

The Google Drive links have been converted from view links to direct download format:
- Old: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- New: `https://drive.google.com/uc?export=download&id=FILE_ID`

## Known Limitations

Google Drive direct download links may:
1. Not work reliably for embedding in web pages
2. Be blocked by some browsers or privacy extensions
3. Require authentication in some cases
4. Have rate limiting or download quotas

## Recommended Solution

For best reliability and performance, download the images from Google Drive and add them to the `/images` directory:

### For 100_4_bases.html
1. Download the image from: `https://drive.google.com/file/d/1-UBssFIO30e81ujw4MMupXAeVrwwlKKM/view?usp=sharing`
2. Save it as `/images/4_bases_decomposition.png` (or appropriate name)
3. Update the excerpt in `_portfolio/100_4_bases.html` to use `/images/4_bases_decomposition.png`

### For 200_ensemble_conditional_gp.html
1. Download the image from: `https://drive.google.com/file/d/1Gsu6ynyQlAiy7Ob4CUXf4cE_cfxRVsUU/view?usp=sharing`
2. Save it as `/images/ensemble_gp.png` (or appropriate name)
3. Update the excerpt in `_portfolio/200_ensemble_conditional_gp.html` to use `/images/ensemble_gp.png`

## Testing

After the images are uploaded to the `/images` directory:
1. The portfolio page should display thumbnails correctly
2. Images should load quickly without external dependencies
3. No authentication or rate limiting issues

## Alternative: Use Imgur or GitHub Releases

If you prefer not to store large images in the repository:
1. **Imgur**: Upload to Imgur and use the direct link (e.g., `https://i.imgur.com/xxxxx.png`)
2. **GitHub Releases**: Attach images to a GitHub release and use the asset URL
3. **GitHub Issues**: Upload images to a GitHub issue and copy the generated URL

All of these options provide reliable direct image URLs suitable for web embedding.
