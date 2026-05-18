"""Variable-mass rocket with altitude-dependent gravity, exponential atmosphere,
and quadratic drag. Compares Forward Euler vs RK4 integration.

MAT423E coursework. See README.md for the model derivation.
"""

import matplotlib.pyplot as plt
import numpy as np

# Environment
G0 = 9.80665  # gravity at sea level [m/s^2]
R_E = 6.371e6  # mean Earth radius [m]
RHO0 = 1.225  # air density at sea level [kg/m^3]
H_ATM = 8500.0  # atmospheric scale height [m]

# Rocket (assignment values; Falcon-9-class)
M0 = 500_000.0  # initial total mass [kg]
M_DRY = 50_000.0  # structural / dry mass [kg]
MDOT = 1_500.0  # fuel burn rate [kg/s]
V_EXH = 3_000.0  # effective exhaust velocity [m/s]
C_D = 0.5  # drag coefficient (blunt nose, transonic average)
AREA = 10.75  # cross-sectional area [m^2] (d ≈ 3.7 m)

T_BURN = (M0 - M_DRY) / MDOT  # 300 s
THRUST_0 = MDOT * V_EXH  # 4.5 MN


def gravity(y):
    return G0 * (R_E / (R_E + max(y, 0.0))) ** 2


def air_density(y):
    if y < 0:
        return RHO0
    return RHO0 * np.exp(-y / H_ATM)


def mass(t):
    if t < T_BURN:
        return M0 - MDOT * t
    return M_DRY


def thrust(t):
    return THRUST_0 if t < T_BURN else 0.0


def rhs(t, state):
    """State = [y, v]. Drag uses v·|v| so it always opposes motion.

    The ground-hold gate is essential: with the assignment's MDOT the initial
    T/W is 0.918, so the rocket sits on the pad until enough fuel burns away
    (~27 s). Without the gate, Euler/RK4 would tunnel into negative altitude.
    """
    y, v = state
    m = mass(t)
    g = gravity(y)
    rho = air_density(y)

    drag = 0.5 * rho * C_D * AREA * v * abs(v)
    F_net = thrust(t) - m * g - drag

    if y <= 0.0 and v <= 0.0 and F_net <= 0.0:
        return np.array([0.0, 0.0])
    return np.array([v, F_net / m])


def euler(state0, t0, dt, t_max):
    ts = [t0]
    ys = [state0.copy()]
    t = t0
    s = state0.copy()
    while t < t_max:
        s = s + dt * rhs(t, s)
        t = t + dt
        ts.append(t)
        ys.append(s.copy())
        if s[0] < 0 and t > 1.0:
            break
    return np.array(ts), np.array(ys)


def rk4(state0, t0, dt, t_max):
    ts = [t0]
    ys = [state0.copy()]
    t = t0
    s = state0.copy()
    while t < t_max:
        k1 = rhs(t, s)
        k2 = rhs(t + dt / 2, s + dt / 2 * k1)
        k3 = rhs(t + dt / 2, s + dt / 2 * k2)
        k4 = rhs(t + dt, s + dt * k3)
        s = s + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + dt
        ts.append(t)
        ys.append(s.copy())
        if s[0] < 0 and t > 1.0:
            break
    return np.array(ts), np.array(ys)


def summarize(label, ts, ys):
    y = ys[:, 0]
    v = ys[:, 1]
    apogee_idx = int(np.argmax(y))
    print(
        f"{label:>8}  apogee = {y[apogee_idx] / 1000:8.2f} km "
        f"at t = {ts[apogee_idx]:6.1f} s   "
        f"v_at_cutoff = {np.interp(T_BURN, ts, v):7.1f} m/s   "
        f"t_flight = {ts[-1]:6.1f} s"
    )
    return apogee_idx


def main():
    state0 = np.array([0.0, 0.0])
    t0, t_max = 0.0, 1200.0
    dt = 0.1

    print(f"T/W at t=0 : {THRUST_0 / (M0 * G0):.3f}")
    print(f"Burn time  : {T_BURN:.1f} s\n")

    t_e, s_e = euler(state0, t0, dt, t_max)
    t_r, s_r = rk4(state0, t0, dt, t_max)

    summarize("Euler", t_e, s_e)
    idx_r = summarize("RK4", t_r, s_r)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    axes[0].plot(
        t_e, s_e[:, 0] / 1000, label=f"Forward Euler  (h={dt}s)", linewidth=1.4, alpha=0.85
    )
    axes[0].plot(
        t_r, s_r[:, 0] / 1000, label=f"RK4            (h={dt}s)", linewidth=1.4, linestyle="--"
    )
    axes[0].axvline(
        T_BURN, color="firebrick", linestyle=":", label=f"Engine cutoff (t={T_BURN:.0f}s)"
    )
    axes[0].scatter(
        [t_r[idx_r]], [s_r[idx_r, 0] / 1000], color="black", zorder=5, label="Apogee (RK4)"
    )
    axes[0].set_ylabel("Altitude  [km]")
    axes[0].set_title("Rocket Trajectory  —  Variable-Mass Vertical Launch")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc="best")

    axes[1].plot(t_e, s_e[:, 1], label="Forward Euler", linewidth=1.4, alpha=0.85)
    axes[1].plot(t_r, s_r[:, 1], label="RK4", linewidth=1.4, linestyle="--")
    axes[1].axvline(T_BURN, color="firebrick", linestyle=":")
    axes[1].axhline(0, color="black", linewidth=0.5)
    axes[1].set_xlabel("Time  [s]")
    axes[1].set_ylabel("Velocity  [m/s]")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc="best")

    plt.tight_layout()
    plt.savefig("trajectory.png", dpi=130)
    print("\nSaved trajectory.png")

    print("\nConvergence study (apogee in km):")
    print(f"{'dt [s]':>8}  {'Euler':>10}  {'RK4':>10}")
    for dt_test in [2.0, 1.0, 0.5, 0.1, 0.05, 0.01]:
        _, se = euler(state0, t0, dt_test, t_max)
        _, sr = rk4(state0, t0, dt_test, t_max)
        print(f"{dt_test:>8.3f}  {se[:, 0].max() / 1000:>10.3f}  {sr[:, 0].max() / 1000:>10.3f}")


if __name__ == "__main__":
    main()
