import numpy as np

# --------------------------------------
# GLOBALS
# --------------------------------------
rng = np.random.default_rng(20251002)

prevgray = None
canvas = None
char_i = 0

THRESH = 0.5
RATE = 60
SCALE = 1
FADE = 0.90
JITTER = 2.0

TEXT = "CALX WRITES THE MOTION "

# --------------------------------------
# LETTER BITMAPS
# --------------------------------------
_ALPHA = {
    'A': np.array([
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ], dtype=np.uint8),

    'B': np.array([
        [1,1,1,0,0],
        [1,0,0,1,0],
        [1,0,0,1,0],
        [1,1,1,0,0],
        [1,0,0,1,0],
        [1,0,0,1,0],
        [1,1,1,0,0]
    ], dtype=np.uint8),

    # ... (ALL OTHER LETTERS) ...

    ' ': np.zeros((7, 5), dtype=np.uint8)
}

# --------------------------------------
# FUNCTIONS
# --------------------------------------

def togray01(img):
    """Convert RGBA to grayscale float 0–1."""
    rgb = img[..., :3].astype(np.float32)
    r, g, b = rgb[...,0], rgb[...,1], rgb[...,2]
    return np.clip(0.2126*r + 0.7152*g + 0.0722*b, 0, 1)


def edges_from_thresh(gray, thr):
    """Detect edges based on threshold."""
    mask = (gray >= thr).astype(np.uint8)

    up    = np.roll(mask, -1, 0)
    down  = np.roll(mask,  1, 0)
    left  = np.roll(mask,  1, 1)
    right = np.roll(mask, -1, 1)

    edge = mask & ((up != mask) | (down != mask) |
                   (left != mask) | (right != mask))

    return edge.astype(np.uint8)


def draw_letter_rgba(canvas, ch, cx, cy, s=2, color=(1,1,1,1)):
    """Draw a 5×7 letter onto RGBA canvas."""
    H, W, _ = canvas.shape
    bmp = _ALPHA.get(ch, _ALPHA[' '])

    h7, w5 = bmp.shape
    x0 = int(cx - (w5 * s) // 2)
    y0 = int(cy - (h7 * s) // 2)

    for yy in range(h7):
        for xx in range(w5):
            if bmp[yy, xx]:
                ys = y0 + yy * s
                xs = x0 + xx * s
                ys2 = min(H, ys + s)
                xs2 = min(W, xs + s)
                if 0 <= ys < H and 0 <= xs < W:
                    canvas[ys:ys2, xs:xs2, :] = color


# --------------------------------------
# MAIN CALLBACK
# --------------------------------------

def onCook(scriptOp):
    global prevgray, canvas, char_i

    # Input TOP
    inTOP = scriptOp.inputs[0] if scriptOp.inputs else None
    if inTOP is None:
        h, w = 480, 640
        if canvas is None or canvas.shape[:2] != (h, w):
            canvas = np.zeros((h, w, 4), dtype=np.float32)
        scriptOp.copyNumpyArray(canvas)
        return

    arr = inTOP.numpyArray()
    if arr is None:
        return

    H, W = arr.shape[:2]
    gray = togray01(arr)

    # Reset canvas if size changed
    if canvas is None or canvas.shape[0] != H or canvas.shape[1] != W:
        canvas = np.zeros((H, W, 4), dtype=np.float32)
        prevgray = None
        char_i = 0

    # Fade old content
    canvas[:] = canvas * FADE

    # Edge detection
    edges = edges_from_thresh(gray, THRESH)
    ys, xs = np.nonzero(edges)
    n = ys.size

    if n > 0:
        k = min(RATE, n)
        idx = rng.choice(n, k, replace=False) if n > k else np.arange(n)

        L = len(TEXT)

        for i in idx:
            y, x = int(ys[i]), int(xs[i])

            # Add jitter
            jx = int(rng.normal(0, JITTER))
            jy = int(rng.normal(0, JITTER))

            # Pick character
            ch = TEXT[char_i % L].upper()

            # Draw on canvas
            draw_letter_rgba(
                canvas,
                ch,
                x + jx,
                y + jy,
                s=SCALE,
                color=(1, 1, 1, 1)
            )

            char_i += 1

    # Output
    scriptOp.copyNumpyArray(np.clip(canvas, 0, 1))
