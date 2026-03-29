import numpy as np
rng = np.random.default_rng(20251002)

prevpts = None
_canvas = None

THRESH = 0.5
POINTS = 80
FADE = 0.5
JITTER = 1.0

# -----------------------------
# Convert RGB to grayscale 0-1
# -----------------------------
def togray01(img):
    return np.clip(
        0.2126 * img[...,0] +
        0.7152 * img[...,1] +
        0.0722 * img[...,2],
        0, 1
    )

# -----------------------------
# Edge detection
# -----------------------------
def _edges(gray, thr):
    mask = (gray > thr).astype(np.uint8)
    up    = np.roll(mask, -1, 0)
    down  = np.roll(mask,  1, 0)
    left  = np.roll(mask,  1, 1)
    right = np.roll(mask, -1, 1)

    edge = (mask & (
        (up != mask) |
        (down != mask) |
        (left != mask) |
        (right != mask)
    )).astype(np.uint8)

    return edge

# -----------------------------
# Draw a line into canvas
# -----------------------------
def draw_line(img, x0, y0, x1, y1, color):
    H, W, _ = img.shape
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= y0 < H and 0 <= x0 < W:
            img[y0, x0] = color

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


# =====================================================
# MAIN FUNCTION
# =====================================================
def onCook(scriptOp):
    global prevpts, _canvas

    inTOP = scriptOp.inputs[0] if scriptOp.inputs else None

    # If no input TOP
    if inTOP is None:
        h, w = 1080, 1920
        if _canvas is None or _canvas.shape[:2] != (h, w):
            _canvas = np.zeros((h, w, 4), dtype=np.float32)
        scriptOp.copyNumpyArray(_canvas)
        return

    arr = inTOP.numpyArray()
    if arr is None:
        return

    H, W = arr.shape[0], arr.shape[1]
    gray = togray01(arr[..., :3].astype(np.float32))

    # Init canvas
    if _canvas is None or _canvas.shape[:2] != (H, W):
        _canvas = np.zeros((H, W, 4), dtype=np.float32)
        prevpts = None

    # Fade effect
    _canvas *= FADE

    # Compute edges
    edges = _edges(gray, THRESH)
    ys, xs = np.nonzero(edges)
    n = ys.size

    if n > 0:
        k = min(POINTS, n)
        idx = rng.choice(n, k, replace=False) if n > k else np.arange(n)

        pts = np.stack([xs[idx], ys[idx]], axis=1)
        pts = pts + rng.normal(0, JITTER, pts.shape).astype(int)

        # Draw line between new points
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            color = (rng.random(), rng.random(), rng.random(), 1.0)
            draw_line(_canvas, x0, y0, x1, y1, color)

        # Draw connection to previous points
        if prevpts is not None:
            L = min(len(pts), len(prevpts))
            for i in range(L):
                x0, y0 = pts[i]
                x1, y1 = prevpts[i]
                color = (rng.random(), rng.random(), rng.random(), 1.0)
                draw_line(_canvas, x0, y0, x1, y1, color)

        prevpts = pts
    else:
        prevpts = None

    scriptOp.copyNumpyArray(np.clip(_canvas, 0, 1))
