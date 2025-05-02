import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

def plot_combined_radar(selected: List[str], csv_path: str, save_path: str):
    """
    Plots a combined radar chart for the selected question types and saves it as a PNG.
    Args:
        selected: List of question types (e.g., ['Real', 'Fake'])
        csv_path: Path to the CSV data file
        save_path: Path to save the generated PNG
    """
    df = pd.read_csv(csv_path)
    professions = df.columns[1:]
    colors_dict = {
        'Real': 'green',
        'Fake': 'coral',
        'Fact': 'orange',
        'Opinion': 'blue',
    }
    # Filter only selected questions, preserving order
    selected_rows = [df[df['Question'].str.lower() == q.lower()] for q in selected]
    if not any([not r.empty for r in selected_rows]):
        return  # nothing to plot
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)
    angles = np.linspace(0, 2 * np.pi, len(professions), endpoint=False).tolist()
    angles += angles[:1]
    for i, q in enumerate(selected):
        row = df[df['Question'].str.lower() == q.lower()]
        if row.empty:
            continue
        ratings = [float(str(x).strip()) for x in row.iloc[0, 1:]]
        ratings += ratings[:1]
        ax.plot(angles, ratings, 'o-', linewidth=2, label=q, color=colors_dict[q])
        ax.fill(angles, ratings, alpha=0.15, color=colors_dict[q])
    ax.set_thetagrids(np.degrees(angles[:-1]), professions)
    ax.set_ylim(1, 10)
    plt.title(f"Combined Radar Chart: {', '.join(selected)}", fontsize=14)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
