import sys

import numpy as np
from PIL import Image, ImageFilter

# Measured from alley.png: road line y = ROAD_SLOPE * x + b; depths are vertical px from the edge line.
ROAD_SLOPE = 0.64
ALLEY_SCALE = 1.22
DASH_PERIOD = 37.0
CLEAN_STRETCH_X = 64.0
ALLEY_EDGE_LINE_B = 22.0
ALLEY_PAVEMENT_DEPTH = -19.8
LANE_SPACING = 30.0
DEPTH_STEP = 0.25
ALONG_STEP = 0.5

OLD_ROAD_SLOPE = 0.6325
OLD_PADLOCK_AREA = (slice(66, 120), slice(55, 130))
OLD_LAMP_AREA = ((96, 138), (30, 74))
OLD_FILL_SHIFTS = [70, -70, 85, -85, 100, -100, 55, -55, 115, -115, -45, 45, -35, 35]

PADLOCK_SCALE = 0.8
PADLOCK_CENTRE = (177, 42)
PADLOCK_CLEARANCE = 3
HATCH_ANGLE_FROM_ROAD = -45.0
HATCH_PERIOD = 24.0
HATCH_WIDTH = 10.0
HATCH_ALPHA = 0.6
HATCH_GAP = 8.0
HATCH_COLOUR = np.array([240, 200, 40], float)


def load(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(float)


def bilinear(img, xs, ys):
    x0 = np.clip(np.floor(xs).astype(int), 0, img.shape[1] - 2)
    y0 = np.clip(np.floor(ys).astype(int), 0, img.shape[0] - 2)
    fx = np.clip(xs - x0, 0, 1)[..., None]
    fy = np.clip(ys - y0, 0, 1)[..., None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def content_box(alpha):
    ys, xs = np.nonzero(alpha > 0)
    box = np.zeros(alpha.shape, bool)
    box[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = True
    return box


def largest_component(mask):
    h, w = mask.shape
    labels = np.zeros(mask.shape, int)
    sizes = {}
    for sy, sx in zip(*np.nonzero(mask)):
        if labels[sy, sx]:
            continue
        n = len(sizes) + 1
        labels[sy, sx] = n
        stack = [(sy, sx)]
        count = 0
        while stack:
            y, x = stack.pop()
            count += 1
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not labels[ny, nx]:
                    labels[ny, nx] = n
                    stack.append((ny, nx))
        sizes[n] = count
    return labels == max(sizes, key=sizes.get)


def pavement_edge_b(reference):
    ref_alpha = reference[..., 3]
    return float(np.median(
        [np.nonzero(ref_alpha[:, x] > 128)[0].min() - ROAD_SLOPE * x for x in range(90, 140)]))


def build_road(alley, reference):
    h, w = reference.shape[:2]
    ref_alpha = reference[..., 3]
    pavement_b = pavement_edge_b(reference)

    depths = np.arange(ALLEY_PAVEMENT_DEPTH - 1, 140, DEPTH_STEP)
    along = np.arange(0, DASH_PERIOD, ALONG_STEP)
    dd, aa = np.meshgrid(depths, along, indexing="ij")
    xs = CLEAN_STRETCH_X + aa
    ys = ROAD_SLOPE * xs + ALLEY_EDGE_LINE_B + dd
    samples = bilinear(alley, xs, ys)
    valid = (ys >= 18) & (ys <= 130) & (samples[..., 3] > 20)
    rgb = samples[..., :3] / np.maximum(samples[..., 3:4] / 255, 1e-3)

    profile = np.zeros((len(depths), 3))
    row_ok = np.zeros(len(depths), bool)
    for i in range(len(depths)):
        v = rgb[i][valid[i]]
        if len(v) < len(along) * 0.9:
            continue
        lum = v.mean(axis=1)
        profile[i] = v[lum <= np.percentile(lum, 60)].mean(axis=0)
        row_ok[i] = True

    detail = rgb - profile[:, None, :]
    for i in np.nonzero(row_ok)[0]:
        lum = detail[i].mean(axis=1)
        base = valid[i] & (lum < np.percentile(lum[valid[i]], 60))
        if base.sum() < 10:
            continue
        for c in range(3):
            slope = np.polyfit(along[base], detail[i, base, c], 1)[0]
            detail[i, :, c] -= slope * (along - along.mean())

    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    depth_out = yy - (ROAD_SLOPE * xx + pavement_b)
    depth_src = depth_out / ALLEY_SCALE + ALLEY_PAVEMENT_DEPTH
    deepest = depths[row_ok].max()
    repeats = np.zeros(depth_src.shape, int)
    while (depth_src > deepest).any():
        repeats += depth_src > deepest
        depth_src = np.where(depth_src > deepest, depth_src - LANE_SPACING, depth_src)

    di = np.clip(np.round((depth_src - depths[0]) / DEPTH_STEP).astype(int), 0, len(depths) - 1)
    ai = np.clip(np.round(np.mod(xx / ALLEY_SCALE, DASH_PERIOD) / ALONG_STEP).astype(int), 0, len(along) - 1)
    road = np.zeros((h, w, 4))
    road[..., :3] = profile[di] + detail[di, ai] * valid[di, ai][..., None]
    solid = profile + np.percentile(np.where(valid[..., None], detail, 0), 90, axis=1)
    marking = depth_src > LANE_SPACING
    road[marking & (repeats == 1), :3] = solid[di[marking & (repeats == 1)]]
    road[marking & (repeats > 1), :3] = profile[di[marking & (repeats > 1)]]
    road[..., 3] = np.where(content_box(ref_alpha), 255 * np.clip(depth_out + 0.5, 0, 1), 0)
    return Image.fromarray(np.clip(road, 0, 255).astype(np.uint8), "RGBA")


def padlock_sprite(player_owned):
    h, w = player_owned.shape[:2]
    lum = player_owned[..., :3].mean(axis=2)
    lane = np.zeros((h, w), bool)
    lane[50:125, 15:130] = True
    core = Image.fromarray((largest_component((lum > 170) & lane) * 255).astype(np.uint8))
    core = core.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    zone = np.asarray(core.filter(ImageFilter.MaxFilter(3))) > 128
    alpha = np.clip((lum - 140) / 90, 0, 1) * zone

    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    # Lane dash leaving the painted padlock's bottom-right corner in player_owned.png.
    alpha[(xx >= 106) & (np.abs(yy - (107.5 + 0.6 * (xx - 106))) < 1.6)] = 0

    colour = np.median(player_owned[..., :3][alpha > 0.95], axis=0)
    ys, xs = np.nonzero(alpha > 0.02)
    crop = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    sprite = np.zeros(alpha[crop].shape + (4,))
    sprite[..., :3] = colour
    sprite[..., 3] = alpha[crop] * 255
    img = Image.fromarray(sprite.astype(np.uint8), "RGBA")
    return img.resize((round(img.width * PADLOCK_SCALE), round(img.height * PADLOCK_SCALE)), Image.LANCZOS)


def clean_old_road(player_owned_old):
    h, w = player_owned_old.shape[:2]
    alpha = player_owned_old[..., 3]
    lum = player_owned_old[..., :3].mean(axis=2)
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    pavement_b = float(np.median(
        [np.nonzero(alpha[:, x] > 128)[0].min() - OLD_ROAD_SLOPE * x for x in range(150, 205)]))
    depth = yy - (OLD_ROAD_SLOPE * xx + pavement_b)
    box = content_box(alpha)
    inside = box & (depth >= 0)

    painted = np.zeros((h, w), bool)
    painted[OLD_PADLOCK_AREA] = lum[OLD_PADLOCK_AREA] > 170
    fill = np.asarray(Image.fromarray((painted * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 128
    (lx0, lx1), (ly0, ly1) = OLD_LAMP_AREA
    fill |= (xx >= lx0) & (xx <= lx1) & (yy >= ly0) & (yy <= ly1) & inside

    patched = player_owned_old.copy()
    todo = fill & inside
    for shift in OLD_FILL_SHIFTS:
        xi = np.round(xx + shift).astype(int)
        yi = np.round(yy + OLD_ROAD_SLOPE * shift).astype(int)
        ok = (xi >= 0) & (xi < w) & (yi >= 0) & (yi < h)
        xi, yi = np.clip(xi, 0, w - 1), np.clip(yi, 0, h - 1)
        use = todo & ok & inside[yi, xi] & ~fill[yi, xi]
        patched[use] = player_owned_old[yi[use], xi[use]]
        todo &= ~use

    soft = np.asarray(Image.fromarray((fill * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))) / 255
    road = player_owned_old * (1 - soft[..., None]) + patched * soft[..., None]
    road[fill] = patched[fill]
    road[..., 3] = np.where(box, 255 * np.clip(depth + 0.5, 0, 1), 0)
    return Image.fromarray(np.clip(road, 0, 255).astype(np.uint8), "RGBA"), pavement_b


def warning_hatch(size, box, slope, pavement_b):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    beyond = (slope * xx + pavement_b) - yy - HATCH_GAP
    zone = np.clip(beyond + 0.5, 0, 1)
    angle = np.arctan(slope) + np.radians(HATCH_ANGLE_FROM_ROAD)
    t = np.mod(xx * -np.sin(angle) + yy * np.cos(angle), HATCH_PERIOD)
    stripe = np.clip(HATCH_WIDTH / 2 + 0.5 - np.abs(t - HATCH_PERIOD / 2), 0, 1)
    hatch = np.zeros((h, w, 4))
    hatch[..., :3] = HATCH_COLOUR
    hatch[..., 3] = 255 * stripe * zone * box * HATCH_ALPHA
    return Image.fromarray(np.clip(hatch, 0, 255).astype(np.uint8), "RGBA")


def main():
    era, road_src_path, player_owned_path, out_path = sys.argv[1:5]
    player_owned = load(player_owned_path)
    h, w = player_owned.shape[:2]
    if era == "new":
        road = build_road(load(road_src_path), player_owned)
        slope, pavement_b = ROAD_SLOPE, pavement_edge_b(player_owned)
    else:
        road, pavement_b = clean_old_road(load(road_src_path))
        slope = OLD_ROAD_SLOPE

    sprite = padlock_sprite(player_owned)
    cx, cy = PADLOCK_CENTRE
    origin = (cx - sprite.width // 2, cy - sprite.height // 2)
    padlock = Image.new("L", (w, h))
    padlock.paste(sprite.getchannel("A"), origin)
    clearance = padlock.filter(ImageFilter.MaxFilter(2 * PADLOCK_CLEARANCE + 1)).filter(ImageFilter.GaussianBlur(0.7))

    hatch = warning_hatch((w, h), content_box(player_owned[..., 3]), slope, pavement_b)
    hatch_alpha = np.asarray(hatch.getchannel("A")).astype(float) * (1 - np.asarray(clearance) / 255)
    hatch.putalpha(Image.fromarray(hatch_alpha.astype(np.uint8)))

    icon = road
    icon.alpha_composite(hatch)
    icon.alpha_composite(sprite, origin)
    icon.save(out_path)


if __name__ == "__main__":
    main()
