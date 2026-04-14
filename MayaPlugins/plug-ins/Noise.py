"""
Perlin noise implementation in Python/NumPy.

Ported from C++ by Jon Macey (Noise.h / Noise.cpp), originally based on:
  - "Computer Graphics with OpenGL" by F.S. Hill
  - "Texturing and Modeling" by Ebert et al.
  - Contributions from Ian Stephenson

Usage
-----
    from noise import Noise
    import numpy as np

    n = Noise(seed=42)

    p = np.array([1.2, 3.4, 5.6])          # 3-D point (x, y, z)

    v  = n.noise(scale=2.0, p=p)            # basic Perlin noise  -> float in [0, 1)
    t  = n.turbulance(scale=2.0, p=p)       # turbulence          -> float
    c  = n.complex(steps=4,                 # fBm / complex noise -> float
                   persistence=2.0,
                   scale=2.0,
                   p=p)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


class Noise:
    """Simple Perlin-style noise, mirroring the C++ Noise class."""

    # ------------------------------------------------------------------
    # Construction / table management
    # ------------------------------------------------------------------

    def __init__(self, seed: int = 1) -> None:
        """
        Parameters
        ----------
        seed:
            RNG seed (equivalent to ``setSeed`` + ``resetTables`` in C++).
        """
        self._seed: int = seed
        # Tables are populated by reset_tables().
        self._noise_table: np.ndarray = np.empty(256, dtype=np.float32)
        self._index: np.ndarray = np.arange(256, dtype=np.uint8)
        self.reset_tables()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value: int) -> None:
        """Equivalent to ``setSeed``; call ``reset_tables`` afterwards."""
        self._seed = int(value)

    def reset_tables(self) -> None:
        """
        Re-initialise the noise and index tables using the current seed.
        Equivalent to ``resetTables()`` in C++.
        """
        rng = np.random.default_rng(self._seed)  # Mersenne Twister

        # Shuffle the index table (matches std::shuffle)
        self._index = np.arange(256, dtype=np.uint8)
        rng.shuffle(self._index)

        # Fill noise table with uniform floats in [0, 1)
        self._noise_table = rng.random(256).astype(np.float32)

    def noise(self, scale: float, p: ArrayLike) -> float:
        """
        Trilinearly-interpolated lattice noise.

        Parameters
        ----------
        scale:
            Frequency multiplier applied to *p* before sampling.
        p:
            3-D point as any sequence ``[x, y, z]``.

        Returns
        -------
        float
            Noise value (approximately in [0, 1)).
        """
        px, py, pz = np.asarray(p, dtype=np.float64)[:3]
        px *= scale
        py *= scale
        pz *= scale

        # Floor toward -inf (matches C behaviour for negative coords too)
        ix, iy, iz = int(np.floor(px)), int(np.floor(py)), int(np.floor(pz))
        tx = px - ix
        ty = py - iy
        tz = pz - iz

        # Quintic fade (Perlin 2002): 6t^5 - 15t^4 + 10t^3
        # Removes the linear banding visible with a raw lerp.
        tx = _fade(tx)
        ty = _fade(ty)
        tz = _fade(tz)

        # Sample the 2x2x2 neighbourhood
        d = np.empty((2, 2, 2), dtype=np.float32)
        for k in range(2):
            for j in range(2):
                for i in range(2):
                    d[k, j, i] = self._lattice_noise(ix + i, iy + j, iz + k)

        # Trilinear interpolation (matches C++ lerp chain)
        x0 = _lerp(d[0, 0, 0], d[0, 0, 1], tx)
        x1 = _lerp(d[0, 1, 0], d[0, 1, 1], tx)
        x2 = _lerp(d[1, 0, 0], d[1, 0, 1], tx)
        x3 = _lerp(d[1, 1, 0], d[1, 1, 1], tx)

        y0 = _lerp(x0, x1, ty)
        y1 = _lerp(x2, x3, ty)

        return float(_lerp(y0, y1, tz))

    def turbulence(self, scale: float, p: ArrayLike) -> float:
        """
        Turbulence: sum of noise at increasing frequencies with decreasing
        amplitude (4 octaves).

        Parameters
        ----------
        scale:
            Base frequency.
        p:
            3-D point.

        Returns
        -------
        float
            Turbulence value.
        """
        val = (
            self.noise(scale, p) / 2.0
            + self.noise(2.0 * scale, p) / 4.0
            + self.noise(4.0 * scale, p) / 8.0
            + self.noise(8.0 * scale, p) / 16.0
        )
        return float(val)

    def complex(
        self,
        steps: int,
        persistence: float,
        scale: float,
        p: ArrayLike,
    ) -> float:
        """
        Fractional Brownian Motion (fBm) / complex noise.

        Based on http://freespace.virgin.net/hugo.elias/models/m_perlin.htm

        Parameters
        ----------
        steps:
            Number of octaves.
        persistence:
            Controls how quickly amplitude falls off per octave.
            Higher → smoother; lower → rougher.
        scale:
            Base frequency.
        p:
            3-D point.

        Returns
        -------
        float
            Accumulated noise value.
        """
        val = 0.0
        for i in range(1, steps + 1):
            val += self.noise(i * scale, p) / (persistence**i)
        return float(val)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _perm(self, x: int) -> int:
        """Wrap x into [0, 255] and look up the permutation table."""
        return int(self._index[x & 255])

    def _lattice_noise(self, i: int, j: int, k: int) -> float:
        """
        Equivalent to the C++ ``INDEX`` / ``PERM`` macros:
            PERM(i + PERM(j + PERM(k)))
        """
        idx = self._perm(i + self._perm(j + self._perm(k)))
        return float(self._noise_table[idx])


# ---------------------------------------------------------------------------
# Module-level helper (matches the C++ template lerp)
# ---------------------------------------------------------------------------


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation: a + (b - a) * t."""
    return a + (b - a) * t


def _fade(t: float) -> float:
    """
    Quintic smoothstep fade (Ken Perlin, 2002): 6t^5 - 15t^4 + 10t^3.
    Maps [0,1] -> [0,1] with zero first- and second-derivatives at the
    endpoints, eliminating the linear banding produced by a plain lerp.
    """
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


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

    print(f"{'Point':<22}  {'noise':>8}  {'turbulance':>10}  {'complex':>8}")
    print("-" * 56)
    for p in test_points:
        v = n.noise(scale=2.0, p=p)
        t = n.turbulance(scale=2.0, p=p)
        c = n.complex(steps=4, persistence=2.0, scale=2.0, p=p)
        print(f"{str(p):<22}  {v:8.5f}  {t:10.5f}  {c:8.5f}")

    # Demonstrate seed reproducibility
    print("\n--- Seed reproducibility ---")
    n2 = Noise(seed=42)
    p = [1.2, 3.4, 5.6]
    print(f"Same seed → noise values match: {n.noise(2.0, p):.6f} == {n2.noise(2.0, p):.6f}")

    n3 = Noise(seed=99)
    print(f"Different seed → values differ: {n.noise(2.0, p):.6f} != {n3.noise(2.0, p):.6f}")
