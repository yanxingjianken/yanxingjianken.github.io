# Manual Image Download Instructions

Since the automated script cannot access Google Drive from this environment, please follow these manual steps to complete the image migration:

## Option 1: Download via Browser (Recommended)

### Step 1: Download the Images

Download these two images from Google Drive:

1. **Four-Basis Decomposition Image**
   - URL: https://drive.google.com/file/d/1-UBssFIO30e81ujw4MMupXAeVrwwlKKM/view?usp=sharing
   - Click "Download" or right-click → "Save image as..."
   - Save as: `4_bases_decomposition.png`

2. **Ensemble-Consistent GP Image**
   - URL: https://drive.google.com/file/d/1Gsu6ynyQlAiy7Ob4CUXf4cE_cfxRVsUU/view?usp=sharing
   - Click "Download" or right-click → "Save image as..."
   - Save as: `ensemble_gp.png`

### Step 2: Upload to GitHub

#### Via GitHub Web Interface:
1. Go to https://github.com/yanxingjianken/yanxingjianken.github.io/tree/copilot/fix-image-upload-issues/images
2. Click "Add file" → "Upload files"
3. Drag and drop both `4_bases_decomposition.png` and `ensemble_gp.png`
4. Commit with message: "Add Google Drive images to local repository"

#### Via Git Command Line:
```bash
# Copy the downloaded images to the repository
cp /path/to/downloads/4_bases_decomposition.png images/
cp /path/to/downloads/ensemble_gp.png images/

# Add and commit
git add images/4_bases_decomposition.png images/ensemble_gp.png
git commit -m "Add Google Drive images to local repository"
git push
```

### Step 3: Update Portfolio Files

After uploading the images, the portfolio files have already been updated in this PR to reference the local images:
- `_portfolio/100_4_bases.html` → `/images/4_bases_decomposition.png`
- `_portfolio/200_ensemble_conditional_gp.html` → `/images/ensemble_gp.png`

## Option 2: Use Automated Script (If You Have Internet Access)

If you're running this from a machine with internet access:

```bash
chmod +x download_google_drive_images.sh
./download_google_drive_images.sh
```

This will download the images and update all files automatically.

## Verification

After completing the above steps, verify:
1. Images are in the `/images` folder
2. Portfolio files reference `/images/4_bases_decomposition.png` and `/images/ensemble_gp.png`
3. Portfolio page displays images correctly at your GitHub Pages site

## What's Already Done

The following files have already been updated to use local image paths:
- ✅ `_portfolio/100_4_bases.html` - Updated to use `/images/4_bases_decomposition.png`
- ✅ `_portfolio/200_ensemble_conditional_gp.html` - Updated to use `/images/ensemble_gp.png`

You only need to download and upload the actual image files.
