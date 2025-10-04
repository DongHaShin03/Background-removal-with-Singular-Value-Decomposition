# Background/Foreground Separation from Video using SVD

This repository demonstrates how to estimate the background of a video and isolate the foreground using Singular Value Decomposition (SVD) and randomized SVD (rSVD). The pipeline converts a video into a 2‑D data matrix, applies SVD/rSVD, and exports comparison figures and frame grids.

# Input
- Place your input video at a path such as ./Video_003/Video_003.avi.
- Frames are downscaled by the scale parameter to reduce computation.

# Outputs
- The script saves the following files in the working directory:
- aspect_of_A.png — visualization of matrix A (frames on x‑axis, pixels on y‑axis).
- standard_SVD_bkg.png — background estimated with standard SVD (rank‑1).
- randomized_SVD_bkg.png — background estimated with rSVD (rank‑1).
- standard.png — grid of original / background / foreground for selected frames (standard SVD).
- randomized.png — grid of original / background / foreground for selected frames (rSVD).

Titles in the grids emphasize Original video, Background, and Foreground; axes are hidden for readability.

# Method Overview
1.   Data matrix construction: each frame is converted to grayscale, resized, flattened, and stacked into matrix A with shape (n_pixels, n_frames).
2.   Standard SVD: A = U Σ Vᵀ. The background (rank‑1) is reconstructed as U[:, :r] Σ[:r, :r] Vᵀ[:r, :] with r = 1.
3.   Randomized SVD (rSVD): projects A into a random subspace of dimension k to approximate the dominant singular subspace more efficiently.
4.   Foreground: computed as A − background.

# Limitations and Tips
- The low‑rank background assumption is most valid with a static camera.
- Strong illumination changes or hard shadows may degrade separation quality.
- Increasing k can improve rSVD accuracy at the cost of extra computation.
- For cleaner foregrounds, consider post‑processing (thresholding or morphology).



# Aspect of the matrix A, in which each column is a single frame of the clip


![alt text](https://github.com/DongHaShin03/Background-removal-with-Singular-Value-Decomposition/blob/main/aspect_of_A.png?raw=true)

# Aspect of A after SVD reconstruction


![alt text](https://github.com/DongHaShin03/Background-removal-with-Singular-Value-Decomposition/blob/main/randomized_SVD_bkg.png?raw=true)

# Grid of images that represent the split between background and foreground of the frame


![alt text](https://github.com/DongHaShin03/Background-removal-with-Singular-Value-Decomposition/blob/main/randomized.png?raw=true)



