"""Lay 25 ft tubes along the track walls, sharing one line where passes touch."""
import json
import os
import sys
import numpy as np
from scipy.interpolate import Akima1DInterpolator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle

TUBE_M = 25.0 * 0.3048          # 7.62 m
GAP = 0.50                      # two walls this close share one line of tubes
MIN_SEP = 4.0                   # ...only if they are different parts of the lap
N = 6000

BG = 'Utils/tracks/floorplans/IROS_Floorplan_+_Indianapolis.png'

def newest_track():
    """The most recently written design: an export, or the live autosave."""
    import glob, pathlib
    cands = (glob.glob('Utils/tracks/generated/*.json')
             + glob.glob('Utils/track_designer/*.json')
             + glob.glob('*.json')
             + glob.glob(str(pathlib.Path.home() / '.track_designer' / 'autosave.json')))
    cands = [c for c in cands if 'points' in json.load(open(c))]
    if not cands:
        raise SystemExit("no track project found - pass one as an argument")
    return max(cands, key=lambda c: pathlib.Path(c).stat().st_mtime)

SRC = sys.argv[1] if len(sys.argv) > 1 else newest_track()
OUT = ('Utils/tracks/tube_layout_'
       + os.path.splitext(os.path.basename(SRC))[0] + '.png')
print(f"track:  {SRC}")

d = json.load(open(SRC))
if d.get('background_path') and os.path.exists(d['background_path']):
    BG = d['background_path']
pts = np.array(d['points'], float)
pw = np.array(d['point_widths'], float)
RW, RH = d['real_width'], d['real_height']

t_pts = np.linspace(0, 1, len(pts))
t = np.linspace(0, 1, N)
x = Akima1DInterpolator(t_pts, pts[:, 0])(t)
y = Akima1DInterpolator(t_pts, pts[:, 1])(t)
lw = np.interp(t, t_pts, pw[:, 0])
rw = np.interp(t, t_pts, pw[:, 1])
s = np.concatenate([[0], np.cumsum(np.hypot(np.diff(x), np.diff(y)))])
total_s = s[-1]

dx, dy = np.gradient(x), np.gradient(y)
nn = np.hypot(dx, dy); nn[nn == 0] = 1e-9
dx, dy = dx / nn, dy / nn
left = np.column_stack([x - dy * lw, y + dx * lw])
right = np.column_stack([x + dy * rw, y - dx * rw])

walls = np.vstack([left, right])
wall_s = np.concatenate([s, s])
wall_id = np.concatenate([np.zeros(len(left), int), np.ones(len(right), int)])

# ── keep one line where two passes touch ────────────────────────────────────
# Greedy: walk every wall sample; skip it if a sample already kept, from a
# different part of the lap, is within GAP. A uniform grid keeps this linear.
cell = GAP
grid = {}
keep = np.zeros(len(walls), bool)
for i, (px, py) in enumerate(walls):
    cx, cy = int(px / cell), int(py / cell)
    covered = False
    for a in (cx-1, cx, cx+1):
        for b in (cy-1, cy, cy+1):
            for j in grid.get((a, b), ()):
                ds = abs(wall_s[i] - wall_s[j])
                ds = min(ds, total_s - ds)
                if ds > MIN_SEP and np.hypot(px - walls[j][0], py - walls[j][1]) < GAP:
                    covered = True
                    break
            if covered: break
        if covered: break
    if not covered:
        keep[i] = True
        grid.setdefault((cx, cy), []).append(i)

# ── kept samples become continuous runs of wall to build ────────────────────
def run_len_raw(p):
    return float(np.hypot(*np.diff(p, axis=0).T).sum())
run_len = run_len_raw

runs = []
for wid in (0, 1):
    idx = np.flatnonzero(keep & (wall_id == wid))
    if len(idx) == 0:
        continue
    split = np.flatnonzero(np.diff(idx) != 1) + 1
    for part in np.split(idx, split):
        if len(part) >= 2:
            r = walls[part]
            if run_len_raw(r) >= 0.5:      # slivers are dedupe noise, not wall
                runs.append(r)

run_lengths = [run_len(r) for r in runs]
build_len = sum(run_lengths)
both_walls = run_len(left) + run_len(right)

# ── cut each run into tubes ─────────────────────────────────────────────────
def cut(p, step):
    """Split a polyline into pieces of `step` metres (last piece may be short)."""
    seg = np.hypot(*np.diff(p, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    out, start = [], 0.0
    while start < cum[-1] - 1e-9:
        end = min(start + step, cum[-1])
        m = (cum >= start) & (cum <= end)
        piece = p[m]
        # exact endpoints
        def at(dist):
            k = np.searchsorted(cum, dist) - 1
            k = int(np.clip(k, 0, len(seg) - 1))
            f = (dist - cum[k]) / max(seg[k], 1e-9)
            return p[k] + (p[k+1] - p[k]) * f
        piece = np.vstack([at(start), piece, at(end)]) if len(piece) else np.vstack([at(start), at(end)])
        out.append(piece)
        start = end
    return out

tubes = []
for r in runs:
    tubes.extend(cut(r, TUBE_M))

full = sum(1 for tb in tubes if run_len(tb) > TUBE_M - 0.05)
partial = len(tubes) - full
offcut = sum(TUBE_M - run_len(tb) for tb in tubes if run_len(tb) <= TUBE_M - 0.05)

print(f"walls if nothing shared     {both_walls:7.1f} m  ->{both_walls/TUBE_M:6.1f} tube lengths")
print(f"wall to build after sharing {build_len:7.1f} m  ->{build_len/TUBE_M:6.1f} tube lengths")
print(f"saved by sharing            {both_walls-build_len:7.1f} m  ({(both_walls-build_len)/both_walls*100:.0f}%)")
print(f"\nseparate wall runs: {len(runs)}  (lengths {min(run_lengths):.1f}..{max(run_lengths):.1f} m)")
print(f"tubes if offcuts are reused : {int(np.ceil(build_len/TUBE_M)):3d}")
print(f"tubes if each run starts new: {len(tubes):3d}  ({full} full, {partial} part-used, {offcut:.1f} m offcut)")

# ── draw ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(RW/2.6, RH/2.6), dpi=200)
try:
    bg = plt.imread(BG)
    ax.imshow(bg, extent=[0, RW, RH, 0], alpha=0.30, zorder=0)
except Exception as e:
    print("no floor plan:", e)

# track surface
surface = np.vstack([left, right[::-1]])
ax.add_patch(MplPolygon(surface, closed=True, facecolor='#e9edf2',
                        edgecolor='none', alpha=0.85, zorder=1))
ax.plot(x, y, color='#9aa6b2', lw=0.7, ls=(0, (6, 4)), zorder=2)
for ox, oy, r in d['obstacles']:
    ax.add_patch(Circle((ox, oy), r, facecolor='#8a94a0', edgecolor='#333',
                        lw=0.5, alpha=0.9, zorder=3))

def ribbon(p, w=0.26):
    """A thin quad following the polyline — a rectangle where the wall is straight."""
    q = np.asarray(p, float)
    dxx, dyy = np.gradient(q[:, 0]), np.gradient(q[:, 1])
    m = np.hypot(dxx, dyy); m[m == 0] = 1e-9
    dxx, dyy = dxx/m, dyy/m
    a = np.column_stack([q[:, 0] - dyy*w/2, q[:, 1] + dxx*w/2])
    b = np.column_stack([q[:, 0] + dyy*w/2, q[:, 1] - dxx*w/2])
    return np.vstack([a, b[::-1]])

for k, tb in enumerate(tubes):
    ax.add_patch(MplPolygon(ribbon(tb), closed=True, facecolor='#ffd21e',
                            alpha=0.45, edgecolor='black', lw=0.8, zorder=4))
    mid = tb[len(tb)//2]
    ax.annotate(str(k+1), mid, fontsize=5.0, ha='center', va='center',
                color='#222', zorder=5,
                bbox=dict(boxstyle='round,pad=0.10', fc='white', ec='none', alpha=0.65))

ax.set_xlim(0, RW); ax.set_ylim(RH, 0); ax.set_aspect('equal')
ax.set_xlabel('metres'); ax.set_ylabel('metres')
ax.set_title(f"Tube layout — {len(tubes)} tubes of 25 ft  "
             f"({build_len:.0f} m of wall, {both_walls-build_len:.0f} m saved by sharing)",
             fontsize=9)
ax.grid(alpha=0.15, lw=0.4)
fig.tight_layout()
fig.savefig(OUT, bbox_inches='tight')
print("\nper wall run:")
for i, r in enumerate(sorted(runs, key=run_len, reverse=True), 1):
    L = run_len(r)
    print(f"  run {i:2d}: {L:6.1f} m -> {int(np.ceil(L/TUBE_M)):2d} tubes"
          f" ({L/TUBE_M:.2f} lengths)")
print("\nwrote", OUT)
