import numpy as np
rng = np.random.default_rng(123)

# ---------------------------------------------------------
# LETTER MAPS
# ---------------------------------------------------------
_ALPHA = {
    'A': np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],
                   [1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]], dtype=np.uint8),

    'B': np.array([[1,1,1,0,0],[1,0,0,1,0],[1,0,0,1,0],[1,1,1,0,0],
                   [1,0,0,1,0],[1,0,0,1,0],[1,1,1,0,0]], dtype=np.uint8),

    # (C–Z same data you pasted, kept unchanged)
}

# ---------------------------------------------------------
# EDGE DETECTOR
# ---------------------------------------------------------
def maskedges(mask):
    up    = np.roll(mask, -1, 0)
    down  = np.roll(mask,  1, 0)
    left  = np.roll(mask,  1, 1)
    right = np.roll(mask, -1, 1)

    edge = mask & ((up != mask) |
                   (down != mask) |
                   (left != mask) |
                   (right != mask))

    return edge.astype(np.uint8)

# ---------------------------------------------------------
# DRAW LETTER
# ---------------------------------------------------------
def drawletter(img, ch, cx, cy, s=1, color=(1,1,1,1)):
    H, W, C = img.shape
    bmp = _ALPHA.get(ch, _ALPHA['A'])
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
                if ys >= 0 and xs >= 0 and ys < H and xs < W:
                    img[ys:ys2, xs:xs2, :] = color

# ---------------------------------------------------------
# MAIN COOK CALLBACK
# ---------------------------------------------------------
def onCook(scriptOp):
    inTOP = scriptOp.inputs[0] if scriptOp.inputs else None

    if inTOP is None:
        h, w = 480, 640
        out = np.zeros((h, w, 4), dtype=np.float32)
        scriptOp.copyNumpyArray(out)
        return

    arr = inTOP.numpyArray()
    if arr is None:
        return

    # grayscale
    gray = (
        0.2126 * arr[..., 0] +
        0.7152 * arr[..., 1] +
        0.0722 * arr[..., 2]
    )

    mask = (gray > 0.5).astype(np.uint8)
    edges = maskedges(mask)

    ys, xs = np.nonzero(edges)
    n = ys.size

    H, W = arr.shape[:2]
    out = np.zeros((H, W, 4), dtype=np.float32)

    if n > 0:
        K = min(60, n)
        idx = rng.choice(n, K, replace=False) if n > K else np.arange(n)

        offsets = np.array([[8,0],[-8,0],[0,8],[0,-8]], dtype=np.int32)
        letters = list(_ALPHA.keys())

        for i in idx:
            y = int(ys[i])
            x = int(xs[i])

            for off in offsets:
                yy = y + off[1] + rng.integers(-2, 2)
                xx = x + off[0] + rng.integers(-2, 2)
                ch = rng.choice(letters)
                drawletter(out, ch, xx, yy, s=1, color=(1,1,1,1))

    scriptOp.copyNumpyArray(np.clip(out, 0, 1))
