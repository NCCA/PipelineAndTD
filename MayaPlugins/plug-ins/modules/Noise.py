"""
Gradient Perlin noise in Python/NumPy.

Ported from C++ by Jon Macey (Noise.h / Noise.cpp), originally based on:
  - "Computer Graphics with OpenGL" by F.S. Hill
  - "Texturing and Modeling" by Ebert et al.
  - Contributions from Ian Stephenson

This implementation replaces the original value-noise lattice with proper
gradient noise (Ken Perlin, 2002).  Value noise — where a random scalar is
stored at each lattice point — produces the ridge/stripe artefacts visible
when mapped to a mesh, because the hash PERM(i + PERM(j + PERM(k))) does
not decorrelate the three axes well enough at small table sizes.

Gradient noise instead stores a random *unit vector* at every lattice point
and evaluates the dot product of that gradient with the local offset vector.
Because the contribution of each corner depends on position relative to that
corner in all three axes simultaneously, the output is genuinely isotropic.

Public API is identical to the original C++ class:
  noise(scale, p)                         -> float  (remapped to 0 … 1)
  turbulence(scale, p)                    -> float
  complex(steps, persistence, scale, p)  -> float

Usage
-----
    from noise import Noise
    import numpy as np

    n = Noise(seed=42)
    p = np.array([1.2, 3.4, 5.6])

    v = n.noise(scale=2.0, p=p)
    t = n.turbulence(scale=2.0, p=p)
    c = n.complex(steps=4, persistence=2.0, scale=2.0, p=p)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

# ---------------------------------------------------------------------------
# 16 canonical gradient directions on a cube (Perlin 2002).
# Avoiding axis-aligned gradients removes cross-shaped artefacts.
# ---------------------------------------------------------------------------
_GRAD3 = np.array(
    [
        [1, 1, 0],
        [-1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0],
        [1, 0, 1],
        [-1, 0, 1],
        [1, 0, -1],
        [-1, 0, -1],
        [0, 1, 1],
        [0, -1, 1],
        [0, 1, -1],
        [0, -1, -1],
        [1, 1, 0],
        [-1, 1, 0],
        [0, -1, 1],
        [0, -1, -1],
    ],
    dtype=np.float64,
)


class Noise:
    """
    Gradient Perlin noise — faithful port of Jon Macey's C++ Noise class
    with the value-noise core replaced by proper gradient noise.
    """

    def __init__(self, seed: int = 1) -> None:
        self._seed: int = seed
        # Doubled permutation table (512 entries) avoids masking on every lookup.
        self._perm: np.ndarray = np.empty(512, dtype=np.int32)
        self.reset_tables()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value: int) -> None:
        """Equivalent to setSeed(); call reset_tables() afterwards."""
        self._seed = int(value)

    def reset_tables(self) -> None:
        """
        Re-initialise the permutation table using the current seed.
        Equivalent to resetTables() in C++.
        """
        rng = np.random.default_rng(self._seed)
        p = np.arange(256, dtype=np.int32)
        rng.shuffle(p)
        self._perm = np.concatenate([p, p])  # doubled: no wrap needed

    def noise(self, scale: float, p: ArrayLike) -> float:
        """
        Gradient Perlin noise, remapped from [-1, 1] to [0, 1].

        Parameters
        ----------
        scale : float
            Frequency multiplier applied to p before sampling.
        p : array-like, shape (3,)
            3-D sample point [x, y, z].

        Returns
        -------
        float in [0, 1]
        """
        raw = self._gradient_noise(scale, p)
        return float(np.clip(raw * 0.5 + 0.5, 0.0, 1.0))

    def turbulence(self, scale: float, p: ArrayLike) -> float:
        """
        Turbulence: 4-octave sum with decreasing amplitude.
        Equivalent to the C++ turbulence() method.
        """
        val = (
            self._gradient_noise(scale, p) / 2.0
            + self._gradient_noise(2.0 * scale, p) / 4.0
            + self._gradient_noise(4.0 * scale, p) / 8.0
            + self._gradient_noise(8.0 * scale, p) / 16.0
        )
        return float(np.clip(val * 0.5 + 0.5, 0.0, 1.0))

    def complex(
        self,
        steps: int,
        persistence: float,
        scale: float,
        p: ArrayLike,
    ) -> float:
        """
        Fractional Brownian Motion (fBm) / complex noise.
        Equivalent to the C++ complex() method.

        Parameters
        ----------
        steps : int
            Number of octaves.
        persistence : float
            Amplitude fall-off per octave (higher = smoother).
        scale : float
            Base frequency.
        p : array-like
            3-D sample point.
        """
        val = 0.0
        for i in range(1, steps + 1):
            val += self._gradient_noise(i * scale, p) / (persistence**i)
        return float(val)

    # ------------------------------------------------------------------
    # Core gradient noise implementation
    # ------------------------------------------------------------------

    def _gradient_noise(self, scale: float, p: ArrayLike) -> float:
        """
        Raw gradient Perlin noise in approximately [-1, 1].

        Algorithm
        ---------
        For each of the 8 corners of the unit cube surrounding the sample
        point we:
          1. Hash the corner coordinates via the doubled permutation table.
          2. Select a gradient vector from the 16 canonical directions.
          3. Compute the dot product of that gradient with the distance
             vector from the corner to the sample point.
          4. Trilinearly interpolate all 8 contributions using the quintic
             fade curve, ensuring C2-continuous derivatives at boundaries.
        """
        arr = np.asarray(p, dtype=np.float64)[:3]
        px, py, pz = arr * scale

        # Integer cell coords, floored toward -inf (handles negatives correctly)
        X = int(np.floor(px)) & 255
        Y = int(np.floor(py)) & 255
        Z = int(np.floor(pz)) & 255

        # Fractional offsets within the cell
        fx = px - np.floor(px)
        fy = py - np.floor(py)
        fz = pz - np.floor(pz)

        # Quintic fade curves
        u = _fade(fx)
        v = _fade(fy)
        w = _fade(fz)

        # Hash all 8 corners using the doubled perm table
        perm = self._perm
        A = perm[X] + Y
        AA = perm[A] + Z
        AB = perm[A + 1] + Z
        B = perm[X + 1] + Y
        BA = perm[B] + Z
        BB = perm[B + 1] + Z

        # Gradient dot products at each corner
        g000 = _grad(perm[AA], fx, fy, fz)
        g100 = _grad(perm[BA], fx - 1, fy, fz)
        g010 = _grad(perm[AB], fx, fy - 1, fz)
        g110 = _grad(perm[BB], fx - 1, fy - 1, fz)
        g001 = _grad(perm[AA + 1], fx, fy, fz - 1)
        g101 = _grad(perm[BA + 1], fx - 1, fy, fz - 1)
        g011 = _grad(perm[AB + 1], fx, fy - 1, fz - 1)
        g111 = _grad(perm[BB + 1], fx - 1, fy - 1, fz - 1)

        # Trilinear interpolation
        x00 = _lerp(g000, g100, u)
        x10 = _lerp(g010, g110, u)
        x01 = _lerp(g001, g101, u)
        x11 = _lerp(g011, g111, u)

        y0 = _lerp(x00, x10, v)
        y1 = _lerp(x01, x11, v)

        return _lerp(y0, y1, w)


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def _fade(t: float) -> float:
    """Quintic smoothstep: 6t^5 - 15t^4 + 10t^3 (C2-continuous at 0 and 1)."""
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation."""
    return a + (b - a) * t


def _grad(hash_val: int, x: float, y: float, z: float) -> float:
    """
    Pick one of 16 gradient directions via the low 4 bits of hash_val
    and return its dot product with (x, y, z).
    """
    g = _GRAD3[hash_val & 15]
    return float(g[0] * x + g[1] * y + g[2] * z)


# ---------------------------------------------------------------------------
# Quick demo / sanity check
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    n = Noise(seed=42)

    test_points = [
        [0.0, 0.0, 0.0],
        [1.2, 3.4, 5.6],
        [0.5, 0.5, 0.5],
    ]

    print(f"{'Point':<22}  {'noise':>8}  {'turbulence':>10}  {'complex':>8}")
    print("-" * 56)
    for p in test_points:
        v = n.noise(scale=2.0, p=p)
        t = n.turbulence(scale=2.0, p=p)
        c = n.complex(steps=4, persistence=2.0, scale=2.0, p=p)
        print(f"{str(p):<22}  {v:8.5f}  {t:10.5f}  {c:8.5f}")

    # Verify isotropy: each axis must vary independently
    print("\n--- Isotropy check: vary each axis independently (scale=3) ---")
    for axis, label in enumerate("xyz"):
        vals = [
            n.noise(3.0, [(t if axis == 0 else 0.5), (t if axis == 1 else 0.5), (t if axis == 2 else 0.5)])
            for t in np.linspace(0.1, 0.9, 10)
        ]
        spread = max(vals) - min(vals)
        print(f"  {label}-axis spread: {spread:.4f}  {'OK' if spread > 0.05 else 'FLAT - problem!'}")

    # Seed reproducibility
    print("\n--- Seed reproducibility ---")
    n2 = Noise(seed=42)
    p = [1.2, 3.4, 5.6]
    print(f"Same seed match : {n.noise(2.0, p):.6f} == {n2.noise(2.0, p):.6f}")
    n3 = Noise(seed=99)
    print(f"Diff seed differ: {n.noise(2.0, p):.6f} != {n3.noise(2.0, p):.6f}")

    # Cross cell boundaries — smooth and non-linear in all three axes
    print("\n--- Smoothness across cell boundaries ---")
    for axis, label in enumerate("xyz"):
        print(f"  {label}-axis sweep:")
        for t in np.linspace(0.0, 2.0, 12):
            pt = [0.5, 0.5, 0.5]
            pt[axis] = t
            v = n.noise(1.0, pt)
            bar = "█" * int(v * 30)
            print(f"    {label}={t:.2f}  {v:.4f}  {bar}")
