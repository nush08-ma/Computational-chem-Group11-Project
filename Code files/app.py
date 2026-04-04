import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="VIT Bhopal | Quantum Chemistry Suite",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── INJECT FRONTEND FILES ────────────────────────────────────────────────────
try:
    with open("frontend.html", "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=0, scrolling=False)
except FileNotFoundError:
    pass

try:
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ─── COLOR PALETTE  (stroke hex, fill rgba — pre-computed, no string hacks) ──
COLORS = [
    ("#38bdf8", "rgba(56,189,248,0.28)"),
    ("#34d399", "rgba(52,211,153,0.28)"),
    ("#fbbf24", "rgba(251,191,36,0.28)"),
    ("#f472b6", "rgba(244,114,182,0.28)"),
    ("#a78bfa", "rgba(167,139,250,0.28)"),
    ("#fb923c", "rgba(251,146,60,0.28)"),
    ("#4ade80", "rgba(74,222,128,0.28)"),
    ("#e879f9", "rgba(232,121,249,0.28)"),
    ("#f87171", "rgba(248,113,113,0.28)"),
    ("#c084fc", "rgba(192,132,252,0.28)"),
]

PLOT_BG  = "#0a1628"
PAPER_BG = "#111f38"
GRID_COL = "#1e3a5f"
TICK_COL = "#4a6fa5"
TEXT_COL = "#94a3b8"


def plot_defaults(height=520):
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COL, family="Space Mono, monospace"),
        height=height,
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(bgcolor=PLOT_BG, font=dict(color="#cbd5e1"),
                    bordercolor=GRID_COL, borderwidth=1),
    )


def axis_style(title="", **kw):
    return dict(title=title, gridcolor=GRID_COL, zeroline=False,
                tickfont=dict(color=TICK_COL),
                title_font=dict(color=TEXT_COL), **kw)


# ─── QUANTUM PHYSICS BACKEND ──────────────────────────────────────────────────

def bohr_energy(n, Z=1):
    """En = -13.6 Z²/n²  eV"""
    return -13.6 * (Z ** 2) / (n ** 2)


def bohr_radius(n, Z=1):
    """rn = 0.529 n²/Z  Å"""
    return 0.529 * (n ** 2) / Z


def pib_wavefunction(n, L=10.0, pts=600):
    x = np.linspace(0, L, pts)
    psi = np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)
    return x, psi


def pib_energy(n, L_m, mass=9.109e-31):
    """Energy eigenvalue in eV"""
    hbar = 1.0546e-34
    return (n ** 2 * np.pi ** 2 * hbar ** 2) / (2 * mass * L_m ** 2 * 1.602e-19)


def orbital_cloud(n, num=6000):
    """Monte Carlo electron positions for hydrogen-like orbital"""
    r     = np.random.gamma(n + 2, 1.5 * n, num)
    theta = np.random.uniform(0, np.pi, num)
    phi   = np.random.uniform(0, 2 * np.pi, num)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z, r


def wave_packet(x, t, k0=2.0, sigma=1.5, v=0.5):
    x0 = v * t
    return np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) * np.cos(k0 * (x - x0))


# ─── PAGE HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="suite-header">
  <div class="header-glow"></div>
  <div class="orbit-ring r1"></div>
  <div class="orbit-ring r2"></div>
  <div class="orbit-ring r3"></div>
  <div class="header-content">
    <div class="vit-badge">⚛ VIT BHOPAL UNIVERSITY</div>
    <h1 class="suite-title">QUANTUM CHEMISTRY <span class="accent">SUITE</span></h1>
    <p class="suite-subtitle">Computational Visualization · Module 2 · v18.0</p>
    <div class="header-meta">
      <span class="meta-pill">👨‍🏫 Dr. Saurav Prasad</span>
      <span class="meta-pill">🗓 Slot C11+C12+C13</span>
      <span class="meta-pill">🧪 Intro to Computational Chemistry</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "⚡ Overview",
    "🌀 Bohr's Model",
    "🔬 Quantum Foundations",
    "📊 1D Particle Analysis",
    "🌊 Wave Motion",
    "🧊 3D Orbital Lab",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 0 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="tab-body">', unsafe_allow_html=True)
    c1, c2 = st.columns([2.2, 0.85])

    with c1:
        st.markdown("""
        <div class="info-card glow-blue">
          <div class="card-label">PROJECT DESCRIPTION</div>
          <p class="card-text">
            This computational tool simulates the <strong>historical and mathematical evolution</strong>
            of atomic theory — from classical Bohr orbits to de&nbsp;Broglie wave-particle duality,
            Schrödinger's Equation, and real-time Monte Carlo electron density clouds.
          </p>
          <div class="formula-row">
            <span class="formula-chip">Ĥψ = Eψ</span>
            <span class="formula-chip">λ = h/mv</span>
            <span class="formula-chip">Δx·Δp ≥ ℏ/2</span>
            <span class="formula-chip">En = −13.6/n² eV</span>
          </div>
        </div>

        <div class="overview-stats">
          <div class="ov-stat"><div class="ov-val">5</div><div class="ov-label">Modules</div></div>
          <div class="ov-stat"><div class="ov-val">3D</div><div class="ov-label">Orbital Viz</div></div>
          <div class="ov-stat"><div class="ov-val">MC</div><div class="ov-label">Monte Carlo</div></div>
          <div class="ov-stat"><div class="ov-val">v18</div><div class="ov-label">Version</div></div>
        </div>

        <div class="section-label">MODULES</div>
        <div class="module-grid">
          <div class="module-card" data-tab="1">
            <div class="module-num">01</div>
            <div class="module-text">
              <div class="module-name">Bohr's Model</div>
              <div class="module-desc">Quantized orbits &amp; emission spectra</div>
            </div>
            <div class="module-arrow">→</div>
          </div>
          <div class="module-card" data-tab="2">
            <div class="module-num">02</div>
            <div class="module-text">
              <div class="module-name">Quantum Foundations</div>
              <div class="module-desc">de Broglie · Heisenberg · Schrödinger</div>
            </div>
            <div class="module-arrow">→</div>
          </div>
          <div class="module-card" data-tab="3">
            <div class="module-num">03</div>
            <div class="module-text">
              <div class="module-name">Particle in Box</div>
              <div class="module-desc">Energy eigenstates &amp; probability density</div>
            </div>
            <div class="module-arrow">→</div>
          </div>
          <div class="module-card" data-tab="4">
            <div class="module-num">04</div>
            <div class="module-text">
              <div class="module-name">Wave Dynamics</div>
              <div class="module-desc">Time-evolution of quantum wave packets</div>
            </div>
            <div class="module-arrow">→</div>
          </div>
          <div class="module-card" data-tab="5">
            <div class="module-num">05</div>
            <div class="module-text">
              <div class="module-name">3D Orbital Lab</div>
              <div class="module-desc">Monte Carlo electron cloud simulation</div>
            </div>
            <div class="module-arrow">→</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="team-card">
          <div class="team-header">👥 PROJECT TEAM</div>
          <div class="team-member">
            <div class="member-avatar">N</div>
            <div class="member-info">
              <div class="member-name">Nilanjana</div>
              <div class="member-id">25BCE11181</div>
            </div>
          </div>
          <div class="team-member">
            <div class="member-avatar">B</div>
            <div class="member-info">
              <div class="member-name">Bhavishya</div>
              <div class="member-id">25BCE10893</div>
            </div>
          </div>
          <div class="team-member">
            <div class="member-avatar">H</div>
            <div class="member-info">
              <div class="member-name">Harshvardhan Tailor</div>
              <div class="member-id">25BCE10948</div>
            </div>
          </div>
          <div class="team-member">
            <div class="member-avatar">A</div>
            <div class="member-info">
              <div class="member-name">Anushka Mathur</div>
              <div class="member-id">25BCE10039</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — BOHR'S MODEL
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="tab-body">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.7])

    with c1:
        st.markdown("""
        <div class="info-card glow-yellow">
          <div class="card-label">BOHR'S ATOMIC MODEL (1913)</div>
          <p class="card-text">Electrons orbit the nucleus in
          <strong>discrete, circular energy levels</strong>.
          Energy is quantized — only specific orbits n = 1, 2, 3 … are allowed.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("### ⚙️ Parameters")
        Z     = st.slider("Atomic Number (Z)", 1, 10, 1)
        n_max = st.slider("Show orbits up to n", 1, 7, 4)

        st.markdown("### 📐 Key Equations")
        st.latex(r"E_n = -13.6\,\frac{Z^2}{n^2}\ \mathrm{eV}")
        st.latex(r"r_n = 0.529\,\frac{n^2}{Z}\ \mathrm{\AA}")
        st.latex(r"mvr = \frac{nh}{2\pi}")

        st.markdown("### 📊 Energy Table")
        st.dataframe(
            {
                "n":           list(range(1, n_max + 1)),
                "Energy (eV)": [f"{bohr_energy(n, Z):.4f}" for n in range(1, n_max + 1)],
                "Radius (Å)":  [f"{bohr_radius(n, Z):.4f}"  for n in range(1, n_max + 1)],
            },
            use_container_width=True, hide_index=True,
        )
        st.markdown("""
        <div class="limitation-card">
          <div class="card-label" style="color:#f87171">⚠️ LIMITATION</div>
          <p class="card-text">Violated Heisenberg's Uncertainty Principle by assuming
          fixed, deterministic electron paths.</p>
        </div>""", unsafe_allow_html=True)

    with c2:
        orb_cols = ["#f97316", "#38bdf8", "#34d399", "#fbbf24",
                    "#f472b6", "#a78bfa", "#fb923c", "#4ade80"]
        fig_bohr = go.Figure()

        # Nucleus
        fig_bohr.add_trace(go.Scatter(
            x=[0], y=[0], mode="markers+text",
            marker=dict(size=30, color="#f97316",
                        line=dict(color="#fed7aa", width=3)),
            text=[f"Z={Z}"], textposition="middle center",
            textfont=dict(color="white", size=10, family="Space Mono"),
            name="Nucleus",
            hovertemplate=f"Nucleus Z={Z}<extra></extra>",
        ))

        for n in range(1, n_max + 1):
            r   = bohr_radius(n, Z)
            col = orb_cols[n % len(orb_cols)]
            th  = np.linspace(0, 2 * np.pi, 360)

            fig_bohr.add_trace(go.Scatter(
                x=r * np.cos(th), y=r * np.sin(th),
                mode="lines",
                line=dict(color=col, width=1.4, dash="dot"),
                name=f"n={n}", showlegend=True, hoverinfo="skip",
            ))
            ang = np.pi / 3 * n
            fig_bohr.add_trace(go.Scatter(
                x=[r * np.cos(ang)], y=[r * np.sin(ang)],
                mode="markers",
                marker=dict(size=14, color=col,
                            line=dict(color="white", width=2)),
                name=f"e⁻ n={n}",
                hovertemplate=(f"n={n}<br>"
                               f"E = {bohr_energy(n, Z):.3f} eV<br>"
                               f"r = {r:.3f} Å<extra></extra>"),
            ))

        mr = bohr_radius(n_max, Z) * 1.3
        fig_bohr.update_layout(
            **plot_defaults(520),
            title=dict(text=f"Bohr Model — Z={Z}, n up to {n_max}",
                       font=dict(color="#fbbf24", size=14), x=0.5),
            xaxis=dict(**axis_style("x (Å)"), range=[-mr, mr]),
            yaxis=dict(**axis_style("y (Å)"), range=[-mr, mr], scaleanchor="x"),
        )
        st.plotly_chart(fig_bohr, use_container_width=True)

        # Energy level diagram
        fig_el = go.Figure()
        for n in range(1, n_max + 1):
            E   = bohr_energy(n, Z)
            col = orb_cols[n % len(orb_cols)]
            fig_el.add_shape(type="line", x0=0.15, x1=0.85, y0=E, y1=E,
                             line=dict(color=col, width=2))
            fig_el.add_annotation(
                x=0.88, y=E,
                text=f"n={n}: {E:.2f} eV",
                font=dict(color=col, size=10, family="Space Mono"),
                showarrow=False, xanchor="left",
            )
        fig_el.add_shape(type="line", x0=0, x1=1, y0=0, y1=0,
                         line=dict(color="#f87171", width=1, dash="dash"))
        fig_el.add_annotation(x=0.5, y=0.5, text="E = 0 (Ionization)",
                              font=dict(color="#f87171", size=9), showarrow=False)
        _el_layout = plot_defaults(290)
        _el_layout["margin"] = dict(l=20, r=130, t=45, b=20)
        fig_el.update_layout(
            **_el_layout,
            title=dict(text="Energy Level Diagram",
                       font=dict(color="#38bdf8", size=12), x=0.5),
            xaxis=dict(visible=False),
            yaxis=dict(**axis_style("Energy (eV)"),
                       range=[bohr_energy(n_max, Z) - 2, 2]),
            showlegend=False,
        )
        st.plotly_chart(fig_el, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — QUANTUM FOUNDATIONS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="tab-body">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="foundation-card glow-blue">
          <div class="f-number">01</div>
          <div class="f-name">de Broglie<br>Wave-Particle Duality</div>
          <div class="f-year">1924</div>
        </div>""", unsafe_allow_html=True)
        st.latex(r"\lambda = \frac{h}{mv}")
        st.markdown("""
        <div class="info-card">
          <p class="card-text">Matter behaves as waves. An electron moving at velocity v has
          wavelength λ, explaining quantized Bohr orbits via standing-wave condition
          <strong>2πr = nλ</strong>.</p>
        </div>""", unsafe_allow_html=True)
        m_v = st.number_input("Mass (kg)", value=9.109e-31, format="%.3e", key="db_m")
        v_v = st.number_input("Velocity (m/s)", value=2.18e6, format="%.3e", key="db_v")
        lam = 6.626e-34 / (m_v * v_v) if m_v * v_v != 0 else 0.0
        st.metric("de Broglie λ", f"{lam:.4e} m")

    with c2:
        st.markdown("""
        <div class="foundation-card glow-yellow">
          <div class="f-number">02</div>
          <div class="f-name">Heisenberg<br>Uncertainty Principle</div>
          <div class="f-year">1927</div>
        </div>""", unsafe_allow_html=True)
        st.latex(r"\Delta x \cdot \Delta p \geq \frac{\hbar}{2}")
        st.markdown("""
        <div class="info-card">
          <p class="card-text">Position and momentum <strong>cannot both be precisely known</strong>
          simultaneously. This fundamentally invalidates Bohr's fixed-orbit model.</p>
        </div>""", unsafe_allow_html=True)
        dx     = st.slider("Δx (position, nm)", 0.01, 2.0, 0.1, key="heis")
        min_dp = 1.0546e-34 / (2 * dx * 1e-9)
        st.metric("Min Δp (kg·m/s)", f"{min_dp:.3e}")
        st.metric("Min Δv for e⁻ (m/s)", f"{min_dp / 9.109e-31:.3e}")

    with c3:
        st.markdown("""
        <div class="foundation-card glow-pink">
          <div class="f-number">03</div>
          <div class="f-name">Schrödinger<br>Wave Equation</div>
          <div class="f-year">1926</div>
        </div>""", unsafe_allow_html=True)
        st.latex(r"\hat{H}\psi = E\psi")
        st.markdown("""
        <div class="info-card">
          <p class="card-text">The wavefunction ψ encodes <strong>all quantum information</strong>.
          |ψ|² is the probability density — likelihood of finding the particle at a given point.</p>
        </div>""", unsafe_allow_html=True)
        st.latex(r"-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2}+V\psi=E\psi")

    # Timeline
    st.markdown("---")
    st.markdown("### 📅 Historical Timeline of Quantum Theory")
    events = [
        (1900, "Planck Quantum Hypothesis", "#38bdf8"),
        (1905, "Einstein Photoelectric",    "#34d399"),
        (1913, "Bohr Atomic Model",         "#fbbf24"),
        (1924, "de Broglie Duality",        "#f472b6"),
        (1925, "Heisenberg Matrix QM",      "#a78bfa"),
        (1926, "Schrödinger Equation",      "#fb923c"),
        (1927, "Uncertainty Principle",     "#4ade80"),
        (1932, "Dirac Relativistic QM",     "#e879f9"),
    ]
    fig_tl = go.Figure()
    for i, (yr, label, col) in enumerate(events):
        fig_tl.add_trace(go.Scatter(
            x=[yr], y=[0], mode="markers",
            marker=dict(size=16, color=col, line=dict(color="white", width=2)),
            hovertemplate=f"<b>{yr}</b><br>{label}<extra></extra>",
            showlegend=False,
        ))
        fig_tl.add_annotation(
            x=yr, y=0.07 if i % 2 == 0 else -0.07,
            text=f"<b>{yr}</b><br>{label.split()[0]}",
            font=dict(color=col, size=9), showarrow=False,
        )
    fig_tl.add_shape(type="line", x0=1898, x1=1934, y0=0, y1=0,
                     line=dict(color=GRID_COL, width=2))
    _tl_layout = plot_defaults(190)
    _tl_layout["margin"] = dict(l=10, r=10, t=10, b=10)
    fig_tl.update_layout(
        **_tl_layout,
        xaxis=dict(range=[1897, 1935], showgrid=False,
                   tickfont=dict(color=TICK_COL)),
        yaxis=dict(visible=False, range=[-0.22, 0.22]),
    )
    st.plotly_chart(fig_tl, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — 1D PARTICLE IN A BOX
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="tab-body">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.9])

    with c1:
        st.markdown("""
        <div class="info-card glow-yellow">
          <div class="card-label">1D PARTICLE IN A BOX</div>
          <p class="card-text">A particle confined in an infinite potential well.
          Boundary conditions force <strong>standing waves</strong>, yielding
          discrete energy levels.</p>
        </div>""", unsafe_allow_html=True)
        st.latex(r"E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}")
        st.latex(r"\psi_n(x)=\sqrt{\frac{2}{L}}\sin\!\left(\frac{n\pi x}{L}\right)")

        st.markdown("### ⚙️ Parameters")
        n_pib = st.slider("Quantum Number (n)", 1, 10, 1)
        L_pib = st.slider("Box Length L (Å)", 1.0, 20.0, 10.0)
        multi = st.checkbox("Overlay multiple states", False)
        if multi:
            n_list = st.multiselect("Select states", list(range(1, 11)),
                                    default=[1, 2, 3])
        else:
            n_list = [n_pib]

        st.markdown("### 📊 Energy Levels")
        for n in range(1, min(n_pib + 1, 7)):
            E    = pib_energy(n, L_pib * 1e-10)
            mark = " ← selected" if n == n_pib else ""
            col  = "#fbbf24" if n == n_pib else "#4a6fa5"
            st.markdown(
                f'<div style="color:{col};font-family:Space Mono,monospace;'
                f'font-size:12px;padding:2px 0">n={n}: {E:.4f} eV{mark}</div>',
                unsafe_allow_html=True,
            )

        E1 = pib_energy(1,     L_pib * 1e-10)
        En = pib_energy(n_pib, L_pib * 1e-10)
        st.metric("Eₙ / E₁ ratio", f"{En / E1:.2f}")
        st.metric("Nodes in ψ", n_pib - 1)

    with c2:
        fig_pib = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.08,
                                row_heights=[0.5, 0.5])

        for idx, n in enumerate(n_list):
            stroke, fill = COLORS[idx % len(COLORS)]
            x, psi = pib_wavefunction(n, L_pib)

            # Wavefunction row
            fig_pib.add_trace(go.Scatter(
                x=x, y=psi, mode="lines", name=f"ψ n={n}",
                line=dict(color=stroke, width=2.5),
                hovertemplate=f"n={n} | x=%.2f Å | ψ=%.4f<extra></extra>",
            ), row=1, col=1)

            # Probability density row — fill uses the pre-made rgba string
            fig_pib.add_trace(go.Scatter(
                x=x, y=psi ** 2, mode="lines", name=f"|ψ|² n={n}",
                line=dict(color=stroke, width=1.5),
                fill="tozeroy",
                fillcolor=fill,          # proper rgba string, no hex mangling
                showlegend=False,
                hovertemplate=f"n={n} | x=%.2f Å | |ψ|²=%.4f<extra></extra>",
            ), row=2, col=1)

        # Potential walls via shapes (avoids add_vline row-scoping issues)
        for xv in [0, L_pib]:
            fig_pib.add_shape(
                type="line", x0=xv, x1=xv, y0=-2, y1=2,
                line=dict(color="#f87171", width=3),
                xref="x", yref="y",
            )
            fig_pib.add_shape(
                type="line", x0=xv, x1=xv, y0=-0.1, y1=0.6,
                line=dict(color="#f87171", width=3),
                xref="x2", yref="y2",
            )

        fig_pib.update_layout(
            **plot_defaults(630),
            title=dict(
                text=f"Particle in Box — n={n_pib}, L={L_pib:.1f} Å",
                font=dict(color="#fbbf24", size=14), x=0.5,
            ),
            xaxis2=dict(**axis_style("x (Å)"), range=[-0.3, L_pib + 0.3]),
            yaxis=dict(**axis_style("ψ(x)")),
            yaxis2=dict(**axis_style("|ψ(x)|²")),
        )
        st.plotly_chart(fig_pib, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — WAVE MOTION
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="tab-body">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.9])

    with c1:
        st.markdown("""
        <div class="info-card glow-pink">
          <div class="card-label">WAVE DYNAMICS &amp; TIME EVOLUTION</div>
          <p class="card-text">Visualizes time evolution of quantum wave packets.
          For stationary states |ψ|² is constant; superpositions produce
          interference patterns that evolve in time.</p>
        </div>""", unsafe_allow_html=True)
        st.latex(r"\Psi(x,t)=\psi(x)\,e^{-iEt/\hbar}")

        mode  = st.selectbox("Mode",
                             ["Stationary State", "Gaussian Wave Packet",
                              "Superposition"])
        t_val = st.slider("Time t (fs)", 0.0, 100.0, 0.0, 0.5)
        n1    = st.slider("State n₁", 1, 8, 1)
        n2    = st.slider("State n₂", 1, 8, 3) if mode == "Superposition" else 3
        k0    = (st.slider("k₀", 0.5, 5.0, 2.0)
                 if mode == "Gaussian Wave Packet" else 2.0)
        sig   = (st.slider("σ (width)", 0.5, 4.0, 1.5)
                 if mode == "Gaussian Wave Packet" else 1.5)

    with c2:
        xw = np.linspace(0, 10, 600)
        L  = 10.0
        tt = t_val * 1e-15

        if mode == "Stationary State":
            om    = pib_energy(n1, L * 1e-10) * 1.602e-19 / 1.0546e-34
            psi_r = np.sqrt(2 / L) * np.sin(n1 * np.pi * xw / L) * np.cos(om * tt)
            psi_i = -np.sqrt(2 / L) * np.sin(n1 * np.pi * xw / L) * np.sin(om * tt)
        elif mode == "Gaussian Wave Packet":
            psi_r = wave_packet(xw, t_val * 0.1, k0, sig)
            psi_i = np.zeros_like(psi_r)
        else:
            p1    = np.sqrt(2 / L) * np.sin(n1 * np.pi * xw / L)
            p2    = np.sqrt(2 / L) * np.sin(n2 * np.pi * xw / L)
            E1r   = pib_energy(n1, L * 1e-10) * 1.602e-19 / 1.0546e-34
            E2r   = pib_energy(n2, L * 1e-10) * 1.602e-19 / 1.0546e-34
            psi_r = (p1 * np.cos(E1r * tt) + p2 * np.cos(E2r * tt)) / np.sqrt(2)
            psi_i = -(p1 * np.sin(E1r * tt) + p2 * np.sin(E2r * tt)) / np.sqrt(2)

        prob = psi_r ** 2 + psi_i ** 2

        fig_dyn = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.08)
        fig_dyn.add_trace(go.Scatter(
            x=xw, y=psi_r, mode="lines", name="Re(ψ)",
            line=dict(color="#38bdf8", width=2.5),
        ), row=1, col=1)
        if np.any(psi_i != 0):
            fig_dyn.add_trace(go.Scatter(
                x=xw, y=psi_i, mode="lines", name="Im(ψ)",
                line=dict(color="#f472b6", width=2, dash="dash"),
            ), row=1, col=1)
        fig_dyn.add_trace(go.Scatter(
            x=xw, y=prob, mode="lines", name="|ψ|²",
            line=dict(color="#fbbf24", width=1),
            fill="tozeroy",
            fillcolor="rgba(251,191,36,0.25)",
        ), row=2, col=1)

        fig_dyn.update_layout(
            **plot_defaults(630),
            title=dict(
                text=f"{mode} — t = {t_val:.1f} fs",
                font=dict(color="#f472b6", size=14), x=0.5,
            ),
            xaxis2=dict(**axis_style("x (Å)")),
            yaxis=dict(**axis_style("ψ(x,t)")),
            yaxis2=dict(**axis_style("|ψ(x,t)|²")),
        )
        st.plotly_chart(fig_dyn, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — 3D ORBITAL LAB
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="tab-body">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.9])

    with c1:
        st.markdown("""
        <div class="info-card glow-blue">
          <div class="card-label">3D ELECTRON CLOUD LAB</div>
          <p class="card-text">Monte Carlo sampling generates a 3D
          <strong>electron probability cloud</strong>. Points within boundary
          radius r are highlighted to compute radial probability.</p>
        </div>""", unsafe_allow_html=True)

        n_3d    = st.selectbox("Principal Quantum Number (n)", [1, 2, 3, 4])
        r_bound = st.slider("Boundary Radius (Bohr)", 1.0, 30.0,
                            float(n_3d * 4))
        n_pts   = st.select_slider("Sample Points",
                                   [2000, 4000, 6000, 10000], value=4000)
        cmap    = st.selectbox("Color Map",
                               ["Plasma", "Viridis", "Turbo",
                                "Inferno", "Spectral"])
        st.button("🔄 Regenerate Cloud", use_container_width=True)

        x3, y3, z3, r3 = orbital_cloud(n_3d, n_pts)
        inside = r3 <= r_bound
        prob_p = float(np.sum(inside)) / n_pts * 100

        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-val" style="color:#38bdf8">{prob_p:.1f}%</div>
            <div class="stat-label">Inside radius</div>
          </div>
          <div class="stat-box">
            <div class="stat-val" style="color:#34d399">{int(np.sum(inside))}</div>
            <div class="stat-label">Points in</div>
          </div>
          <div class="stat-box">
            <div class="stat-val" style="color:#fbbf24">{n_pts - int(np.sum(inside))}</div>
            <div class="stat-label">Points out</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Radial distribution curve
        r_line = np.linspace(0, 30, 300)
        scale  = n_3d * 0.529 * 2
        P_r    = r_line ** 2 * np.exp(-2 * r_line / scale)
        P_r   /= P_r.max()

        fig_rd = go.Figure()
        fig_rd.add_trace(go.Scatter(
            x=r_line, y=P_r,
            fill="tozeroy",
            fillcolor="rgba(56,189,248,0.18)",
            line=dict(color="#38bdf8", width=2),
        ))
        fig_rd.add_vline(x=r_bound,
                         line=dict(color="#fbbf24", dash="dash", width=2))
        _rd_layout = plot_defaults(190)
        _rd_layout["margin"] = dict(l=20, r=20, t=20, b=40)
        fig_rd.update_layout(
            **_rd_layout,
            xaxis=dict(**axis_style("r (Bohr)")),
            yaxis=dict(**axis_style("P(r) norm.")),
            showlegend=False,
        )
        st.plotly_chart(fig_rd, use_container_width=True)

    with c2:
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=x3, y=y3, z=z3,
            mode="markers",
            marker=dict(
                size=2,
                color=r3,
                colorscale=cmap,
                opacity=0.45,
                colorbar=dict(
                    title="r (a.u.)",
                    title_font=dict(color="white"),
                    tickfont=dict(color="white"),
                ),
            ),
            hovertemplate="x=%.2f<br>y=%.2f<br>z=%.2f<br>r=%.2f<extra></extra>",
        )])

        # Boundary sphere wireframe
        u  = np.linspace(0, 2 * np.pi, 24)
        v  = np.linspace(0, np.pi, 24)
        xs = r_bound * np.outer(np.cos(u), np.sin(v))
        ys = r_bound * np.outer(np.sin(u), np.sin(v))
        zs = r_bound * np.outer(np.ones(24), np.cos(v))
        fig_3d.add_surface(
            x=xs, y=ys, z=zs,
            opacity=0.06,
            colorscale=[[0, "#38bdf8"], [1, "#38bdf8"]],
            showscale=False,
        )

        fig_3d.update_layout(
            paper_bgcolor=PLOT_BG,
            scene=dict(
                bgcolor=PLOT_BG,
                xaxis=dict(backgroundcolor=PLOT_BG, gridcolor=GRID_COL,
                           title="x", title_font=dict(color="white"),
                           tickfont=dict(color=TICK_COL)),
                yaxis=dict(backgroundcolor=PLOT_BG, gridcolor=GRID_COL,
                           title="y", title_font=dict(color="white"),
                           tickfont=dict(color=TICK_COL)),
                zaxis=dict(backgroundcolor=PLOT_BG, gridcolor=GRID_COL,
                           title="z", title_font=dict(color="white"),
                           tickfont=dict(color=TICK_COL)),
            ),
            title=dict(
                text=f"n={n_3d} Orbital Cloud — {prob_p:.1f}% within r={r_bound:.1f}",
                font=dict(color="#38bdf8", size=14), x=0.5,
            ),
            height=680,
            margin=dict(l=0, r=0, t=55, b=0),
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="suite-footer">
  <span>VIT Bhopal University</span><span class="sep">·</span>
  <span>Quantum Chemistry Suite v18.0</span><span class="sep">·</span>
  <span>Faculty: Dr. Saurav Prasad</span><span class="sep">·</span>
  <span>Slot C11+C12+C13</span>
</div>
""", unsafe_allow_html=True)
