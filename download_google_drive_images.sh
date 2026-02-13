#!/bin/bash

# Script to download Google Drive images and update portfolio files
# Run this script to complete the Google Drive image migration

set -e

echo "=========================================="
echo "Google Drive Image Download Script"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Image 1: Four-Basis Decomposition
echo "Downloading image 1: Four-Basis Decomposition..."
FILE_ID_1="1-UBssFIO30e81ujw4MMupXAeVrwwlKKM"
wget --no-check-certificate "https://drive.google.com/uc?export=download&id=${FILE_ID_1}" -O images/4_bases_decomposition.png
echo "✓ Saved to images/4_bases_decomposition.png"
echo ""

# Image 2: Ensemble-Consistent GP
echo "Downloading image 2: Ensemble-Consistent GP..."
FILE_ID_2="1Gsu6ynyQlAiy7Ob4CUXf4cE_cfxRVsUU"
wget --no-check-certificate "https://drive.google.com/uc?export=download&id=${FILE_ID_2}" -O images/ensemble_gp.png
echo "✓ Saved to images/ensemble_gp.png"
echo ""

# Check if downloads were successful
if [ ! -f "images/4_bases_decomposition.png" ] || [ ! -s "images/4_bases_decomposition.png" ]; then
    echo "❌ Error: Failed to download 4_bases_decomposition.png"
    exit 1
fi

if [ ! -f "images/ensemble_gp.png" ] || [ ! -s "images/ensemble_gp.png" ]; then
    echo "❌ Error: Failed to download ensemble_gp.png"
    exit 1
fi

echo "✓ Both images downloaded successfully!"
echo ""

# Update portfolio files
echo "Updating portfolio files to use local images..."
echo ""

# Update 100_4_bases.html
echo "Updating _portfolio/100_4_bases.html..."
sed -i "s|https://drive.google.com/uc?export=download&id=1-UBssFIO30e81ujw4MMupXAeVrwwlKKM|/images/4_bases_decomposition.png|g" _portfolio/100_4_bases.html
echo "✓ Updated 100_4_bases.html"

# Update 200_ensemble_conditional_gp.html
echo "Updating _portfolio/200_ensemble_conditional_gp.html..."
sed -i "s|https://drive.google.com/uc?export=download&id=1Gsu6ynyQlAiy7Ob4CUXf4cE_cfxRVsUU|/images/ensemble_gp.png|g" _portfolio/200_ensemble_conditional_gp.html
echo "✓ Updated 200_ensemble_conditional_gp.html"

echo ""
echo "=========================================="
echo "✅ Migration Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Verify the images look correct:"
echo "   - Check images/4_bases_decomposition.png"
echo "   - Check images/ensemble_gp.png"
echo "2. Test the portfolio page locally"
echo "3. Commit and push the changes:"
echo "   git add images/*.png _portfolio/*.html"
echo "   git commit -m 'Replace Google Drive links with local images'"
echo "   git push"
echo ""
