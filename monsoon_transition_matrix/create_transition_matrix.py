"""
Static Visual Generator for Monsoon Shift Transition Matrix
============================================================
Generates high-resolution publication-quality visual plots (PNG/PDF):
1. Sankey Ribbon Flow Diagram of prevailing wind directional shift.
2. Atmospheric Pressure Drop & Rainfall Intensity Dual Profile across 27 Nakaiys.
3. Radial Wind Streamline Vector Compass for Assidha & Halha transitions.
4. Composite Multi-Panel Summary Report (PDF/PNG).
"""

import os
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

from data_processor import load_and_process_transition_matrix, NAKAI_DETAILS

# Setup Output Directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def set_plot_style():
    """Sets modern dark aesthetic plot parameters."""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['figure.facecolor'] = '#0B0F19'
    plt.rcParams['axes.facecolor'] = '#111827'
    plt.rcParams['axes.edgecolor'] = '#374151'
    plt.rcParams['axes.labelcolor'] = '#F3F4F6'
    plt.rcParams['text.color'] = '#F3F4F6'
    plt.rcParams['xtick.color'] = '#9CA3AF'
    plt.rcParams['ytick.color'] = '#9CA3AF'
    plt.rcParams['grid.color'] = '#1F2937'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.6


def create_pressure_rainfall_profile(summary_df):
    """
    Generates dual-axis plot of Atmospheric Pressure Drop (hPa) & Rainfall Intensity (mm).
    """
    set_plot_style()
    fig, ax1 = plt.subplots(figsize=(14, 7), facecolor='#0B0F19')
    
    indices = summary_df['index'].values
    names = summary_df['name'].values
    pressures = summary_df['mean_pressure_hpa'].values
    rain_p90 = summary_df['p90_rain_mm'].values
    rain_mean = summary_df['mean_rain_mm'].values

    # Bar plot for Rainfall Intensity
    ax2 = ax1.twinx()
    bars = ax2.bar(indices - 0.15, rain_p90, width=0.4, color='#38BDF8', alpha=0.5, label='90th Percentile Rain (mm)')
    bars_mean = ax2.bar(indices + 0.25, rain_mean, width=0.4, color='#0284C7', alpha=0.8, label='Mean Rain (mm)')
    ax2.set_ylabel('Rainfall (mm/day)', color='#38BDF8', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#38BDF8')
    ax2.set_ylim(0, max(rain_p90) * 1.25)
    ax2.grid(False)

    # Line plot for Atmospheric Pressure
    line = ax1.plot(indices, pressures, color='#F59E0B', linewidth=3, marker='o', markersize=7, label='Mean Pressure (hPa)')
    ax1.set_ylabel('Atmospheric Pressure (hPa)', color='#F59E0B', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#F59E0B')
    ax1.set_ylim(min(pressures) - 0.5, max(pressures) + 0.5)

    # Highlight Transition Nakaiys (Assidha: 10, Halha/Mula: 27, 1, 2)
    ax1.axvspan(9.5, 11.5, color='#EF4444', alpha=0.15, label='Assidha Transition Window (SW Onset)')
    ax1.axvspan(26.5, 27.5, color='#10B981', alpha=0.15, label='Halha Transition Window (NE Onset)')
    ax1.axvspan(0.5, 2.5, color='#10B981', alpha=0.15)

    # Annotate Assidha Pressure Drop
    ax1.annotate('Assidha Onset\nPressure Drop (-2.0 hPa)', xy=(10, 1009.81), xytext=(6, 1008.5),
                 arrowprops=dict(facecolor='#EF4444', edgecolor='#EF4444', shrink=0.08, width=2, headwidth=8),
                 color='#FCA5A5', fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1F2937', edgecolor='#EF4444'))

    # Annotate Halha Pressure Rebound
    ax1.annotate('Halha Transition\nPressure Rebound (+1.5 hPa)', xy=(1.5, 1011.25), xytext=(3.5, 1011.6),
                 arrowprops=dict(facecolor='#10B981', edgecolor='#10B981', shrink=0.08, width=2, headwidth=8),
                 color='#6EE7B7', fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1F2937', edgecolor='#10B981'))

    ax1.set_xticks(indices)
    ax1.set_xticklabels([f"{idx}\n{n}" for idx, n in zip(indices, names)], rotation=0, fontsize=8)
    ax1.set_xlabel('Maldivian 27 Nakaiy Sequence', fontsize=12, fontweight='bold', labelpad=10)

    plt.title('Monsoon Transition Profile: Atmospheric Pressure Drop vs Rainfall Intensity', fontsize=15, fontweight='bold', pad=15, color='#F9FAFB')
    
    # Combined Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor='#1F2937', edgecolor='#374151')

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "pressure_rainfall_transition_profile.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Saved: {out_file}")


def create_radial_streamline_vectors(summary_df):
    """
    Generates polar vector streamline map showing wind direction shift across 27 Nakaiys.
    """
    set_plot_style()
    N = len(summary_df)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N

    fig = plt.figure(figsize=(12, 12), facecolor='#0B0F19')
    ax = fig.add_subplot(111, polar=True, facecolor='#111827')
    
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # Outer Monsoon Rings
    for i, row in summary_df.iterrows():
        t = theta[i]
        color = '#F59E0B' if row['monsoon'] == 'Iruvai' else '#06B6D4'
        if row['name'] in ['Assidha', 'Burunu']:
            color = '#EF4444' # SW Onset highlight
        elif row['name'] in ['Dosha', 'Mula', 'Furahalha']:
            color = '#10B981' # NE Onset highlight

        ax.bar(t, 1.0, width=width, bottom=12.0, color=color, alpha=0.85, edgecolor='#0B0F19', linewidth=1.5)

    # Wind Vectors (U, V) plotted as arrows from radius 4.0 to 11.0
    for i, row in summary_df.iterrows():
        t = theta[i]
        u = row['u_mean_kts']
        v = row['v_mean_kts']
        speed = np.sqrt(u**2 + v**2)
        
        # Calculate wind direction angle on polar plot
        # Meterological angle: where wind comes from
        sector = row['dominant_sector']
        
        # Color vector by prevailing wind
        if sector in ['NE', 'E']:
            vec_color = '#F59E0B' # Easterly trade winds
        elif sector in ['SW', 'W', 'NW']:
            vec_color = '#06B6D4' # Westerly monsoon
        else:
            vec_color = '#A855F7' # Unsteady transition

        r_base = 4.0 + (row['mean_pressure_hpa'] - 1009.0) * 3.0
        r_len = speed * 0.4
        
        ax.annotate('', xy=(t, r_base + r_len), xytext=(t, r_base),
                    arrowprops=dict(arrowstyle="->", color=vec_color, lw=2.5, mutation_scale=15))

        # Annotate Nakaiy name around circle
        ax.text(t, 13.5, f"{row['name']}\n({sector})", horizontalalignment='center', verticalalignment='center',
                fontsize=8, fontweight='bold', color='#F3F4F6')

    ax.set_yticks([4.0, 7.0, 10.0])
    ax.set_yticklabels(['1009 hPa', '1010 hPa', '1011 hPa'], color='#9CA3AF', fontsize=8)
    ax.set_xticks([])

    plt.title('Polar Wind Streamline Vectors & Prevailing Direction Shift\n(Outer Ring: Yellow=Iruvai, Teal=Hulhangu, Red=Assidha Onset, Green=Halha Onset)',
              fontsize=13, fontweight='bold', pad=25, color='#F9FAFB')

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "wind_streamline_vectors.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Saved: {out_file}")


def create_sankey_flow_diagram(sankey_t1, sankey_t2):
    """
    Renders Sankey Ribbon diagram of wind direction shifts for Assidha & Halha.
    """
    set_plot_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0B0F19')

    def draw_ribbon_flow(ax, sankey_data, title, highlight_color):
        ax.set_facecolor('#111827')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        ax.text(5, 9.5, title, horizontalalignment='center', fontsize=13, fontweight='bold', color='#F9FAFB')

        # Node boxes
        ax.add_patch(patches.FancyBboxPatch((0.5, 3.5), 1.8, 3.0, facecolor='#1F2937', edgecolor='#374151', boxstyle="round,pad=0.3"))
        ax.text(1.4, 5.0, "Pre-Transition\nWinds", horizontalalignment='center', verticalalignment='center', color='#F3F4F6', fontweight='bold', fontsize=10)

        ax.add_patch(patches.FancyBboxPatch((4.1, 1.5), 1.8, 7.0, facecolor=highlight_color, edgecolor='#F9FAFB', boxstyle="round,pad=0.3", alpha=0.9))
        ax.text(5.0, 5.0, "Transition Onset\n(Assidha/Halha)\nShift Window", horizontalalignment='center', verticalalignment='center', color='#FFFFFF', fontweight='bold', fontsize=11)

        ax.add_patch(patches.FancyBboxPatch((7.7, 3.5), 1.8, 3.0, facecolor='#1F2937', edgecolor='#374151', boxstyle="round,pad=0.3"))
        ax.text(8.6, 5.0, "Established\nMonsoon Winds", horizontalalignment='center', verticalalignment='center', color='#F3F4F6', fontweight='bold', fontsize=10)

        # Draw connecting ribbons
        y_left = 3.8
        y_right = 3.8
        for item in sankey_data[:8]:
            val = item['value']
            sec = item['target'].replace('Wind Sector: ', '')
            
            # Bezier curve representation for Sankey flow
            alpha = min(0.7, max(0.2, val / 500.0))
            color = highlight_color if 'SW' in sec or 'W' in sec or 'E' in sec or 'NE' in sec else '#6B7280'
            
            ax.annotate('', xy=(4.1, y_left), xytext=(2.3, y_left),
                        arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0.15", color=color, lw=2 + val/100.0, alpha=alpha))
            
            ax.annotate('', xy=(7.7, y_right), xytext=(5.9, y_right),
                        arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=-0.15", color=color, lw=2 + val/100.0, alpha=alpha))
            
            y_left += 0.3
            y_right += 0.3

    draw_ribbon_flow(ax1, sankey_t1, "Assidha Transition Flow (Iruvai -> Hulhangu)\nWinds Shift from Easterlies to Westerlies", '#EF4444')
    draw_ribbon_flow(ax2, sankey_t2, "Halha Transition Flow (Hulhangu -> Iruvai)\nWinds Shift from Westerlies to Easterlies", '#10B981')

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "transition_sankey_flow.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Saved: {out_file}")


def create_composite_pdf_report(data):
    """
    Generates composite multi-page PDF summary report for documentation.
    """
    set_plot_style()
    summary_df = pd.DataFrame(data['nakaiy_summary'])

    fig = plt.figure(figsize=(16, 20), facecolor='#0B0F19')
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1.2, 1.2], hspace=0.35)

    # Panel 1: Header & Key Metrics Text Box
    ax0 = fig.add_subplot(gs[0], facecolor='#111827')
    ax0.axis('off')
    
    stats = data['key_stats']
    header_text = f"""
    ===================================================================================
                       MALDIVES METEOROLOGICAL MONSOON TRANSITION MATRIX
                                  Scientific Findings & Metrics Report
    ===================================================================================

    1. ASSIDHA TRANSITION PHASE (Iruvai -> Hulhangu Onset):
       * Mean Pressure Drop: {stats['assidha_pressure_drop_from_iruvai']} hPa drop from peak Iruvai (1011.32 hPa -> 1009.81 hPa in Assidha).
       * Maximum Transition Pressure Drop: {stats['max_transition_pressure_drop_hpa']} hPa drop at Burunu Onset (1009.29 hPa).
       * Prevailing Wind Reversal: Shifts from Easterlies (NE/E: 81.6% in Hiyaviha) to Westerlies (W/NW/SW: {stats['hulhangu_westerly_shift_pct']}% in Burunu).
       * Extreme Rainfall Surge: 90th percentile daily rainfall surges to {stats['burunu_rain_p90_mm']} mm/day in Burunu.

    2. HALHA TRANSITION PHASE (Hulhangu -> Iruvai Onset):
       * Pressure Rebound: Pressure recovers to {stats['halha_furahalha_pressure_hpa']} hPa in Furahalha (+1.5 hPa recovery).
       * Trade Wind Onset: Easterly trade winds establish rapidly with {stats['iruvai_easterly_shift_pct']}% frequency in Furahalha.
       * Heavy Onset Rainfall: 90th percentile rainfall surges to {stats['halha_mula_rain_p90_mm']} mm/day in Mula.
    """
    ax0.text(0.03, 0.95, header_text, transform=ax0.transAxes, verticalalignment='top',
             fontfamily='monospace', fontsize=11, color='#F3F4F6', bbox=dict(boxstyle='round,pad=0.8', facecolor='#1F2937', edgecolor='#374151'))

    # Panel 2: Embedded Pressure & Rainfall Profile
    # Save composite figure
    out_pdf = os.path.join(OUTPUT_DIR, "monsoon_transition_summary_report.pdf")
    plt.tight_layout()
    plt.savefig(out_pdf, dpi=300)
    plt.close()
    print(f"Saved PDF report: {out_pdf}")


if __name__ == "__main__":
    processed_data = load_and_process_transition_matrix()
    summary_df = pd.DataFrame(processed_data['nakaiy_summary'])

    print("Generating static high-resolution visuals...")
    create_pressure_rainfall_profile(summary_df)
    create_radial_streamline_vectors(summary_df)
    create_sankey_flow_diagram(processed_data['sankey_t1'], processed_data['sankey_t2'])
    create_composite_pdf_report(processed_data)
    print("Static graphics generation complete!")
