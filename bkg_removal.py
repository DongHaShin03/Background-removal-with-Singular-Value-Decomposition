import moviepy.editor as mpe
import numpy as np
import skimage.transform
import matplotlib.pyplot as plt
import time

def create_data_matrix_from_video(clip, dims):
    '''
    A method to transform the video into a numpy matrix, we also downscale 
    the video to reduce the computational cost of applying the SVD. 
    We can unroll a frame into a single tall column. 
    So instead of having a 2D picture, we have a column. 
    '''
    number_of_frames = int(clip.fps * clip.duration)
    flatten_gray_frames = []
    for i in range(number_of_frames): 
        frame = clip.get_frame(i / clip.fps) # VideoClip.get_frame(t) returns an numpy.ndarray that represents the RGB picture of the clip at time t or (mono/stereo) value for a sound clip
        gray_frame = np.mean(frame[..., :3], axis = -1).astype(int)
        small_gray_frame = skimage.transform.resize(gray_frame, dims)
        flatten_gray_frames.append(small_gray_frame.flatten())
    return np.vstack(flatten_gray_frames).T

def rSVD(A, k): 
    n = A.shape[1]
    P = np.random.rand(n, k)
    Y = A @ P
    Q = np.linalg.qr(Y)[0]
    B = Q.T @ A
    Uy, s, VT = np.linalg.svd(B, full_matrices = False)
    return Q @ Uy, s, VT

video = mpe.VideoFileClip("./Video_003/Video_003.avi")
scale = 0.50
width, height = video.size
dims = (int(height*scale), int(width*scale))
A = create_data_matrix_from_video(video, dims)
print("frame size: ", dims)
print("video matrix size: ", A.shape)

plt.figure(figsize=(12, 6))
img2 = plt.imshow(A, cmap = "gray", aspect="auto")
plt.savefig("./aspect_of_A.png")

k = 10
# Application of standard SVD
t0_1 = time.time()
U1, s1, VT1 = np.linalg.svd(A, full_matrices = False)
print(f"Standard SVD elapsed time {time.time() - t0_1: .2f} seconds.")
print("SVD decomposition: ", U1.shape, s1.shape, VT1.shape)

n_singular_values = 1
r = n_singular_values
bkg1 = (U1[:, :r] @ np.diag(s1[:r]) @ VT1[:r, :])
plt.figure(figsize=(12, 6))
standard_SVD_A = plt.imshow(bkg1, cmap = "gray", aspect="auto")
plt.savefig("./standard_SVD_bkg.png")

# Application of randomized SVD
t0_2 = time.time()
k = 10
U2, s2, VT2 = rSVD(A, k)
print(f"Randomized SVD elapsed time {time.time() - t0_2: .2f} seconds.")
print("SVD decomposition: ", U2.shape, s2.shape, VT2.shape)

bkg2 = (U2[:, :r] @ np.diag(s2[:r]) @ VT2[:r, :])
plt.figure(figsize=(12, 6))
randomized_SVD_A = plt.imshow(bkg2, cmap = "gray", aspect="auto")
plt.savefig("./randomized_SVD_bkg.png")

def plot_frames(A, background, time_ids, dims, out_path="frames_grid.png", dpi=200):
    fig, axs = plt.subplots(len(time_ids), 3, figsize=(12, 4 * len(time_ids)))
    for i, t_id in enumerate(time_ids):
        axs[i, 0].imshow(np.reshape(A[:, t_id], dims), cmap="gray")
        axs[i, 1].imshow(np.reshape(background[:, t_id], dims), cmap="gray")
        axs[i, 2].imshow(np.reshape(A[:, t_id] - background[:, t_id], dims), cmap="gray")
        axs[i, 0].set_ylabel(f"Frame {t_id}")
        if i == 0:
            axs[0, 0].set_title("Original video")
            axs[0, 1].set_title("Background")
            axs[0, 2].set_title("Foreground")

        for j in range(3):
            axs[i, j].axis("off")

    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)  # libera memoria

# uso
time_ids = [0, 150, 300, 450]
plot_frames(A, bkg1, time_ids, dims, out_path="standard.png")
plot_frames(A, bkg2, time_ids, dims, out_path="randomized.png")
