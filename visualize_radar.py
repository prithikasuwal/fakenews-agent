import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
csv = 'multi_chat_log_profession.csv'
df = pd.read_csv(csv)
professions = df.columns[1:]

# Define colors for each question (updated)
colors = ['green', 'coral', 'orange', 'blue']

# Define labels for each question from CSV (use row labels)
titles = df['Question'].tolist()

# Individual radar charts with specified colors and labels
for i, row in df.iterrows():
    ratings = []
    for x in row[1:]:
        try:
            val = float(str(x).strip())
            ratings.append(val)
        except Exception:
            ratings.append(np.nan)
    angles = np.linspace(0, 2 * np.pi, len(professions), endpoint=False).tolist()
    ratings += ratings[:1]
    angles += angles[:1]
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, ratings, 'o-', linewidth=2, color=colors[i % len(colors)])
    ax.fill(angles, ratings, alpha=0.25, color=colors[i % len(colors)])
    ax.set_thetagrids(np.degrees(angles[:-1]), professions)
    ax.set_ylim(1, 10)
    plt.title(f'{titles[i].capitalize()}')
    plt.tight_layout()
    plt.savefig(f'multi_chat_log_profession_{titles[i].lower()}.png')
    plt.close()

# --- Combined radar chart with all 4 questions and proper radar format ---
plt.figure(figsize=(10, 10))
ax = plt.subplot(111, polar=True)
angles = np.linspace(0, 2 * np.pi, len(professions), endpoint=False).tolist()
angles += angles[:1]
for i, row in df.iterrows():
    ratings = []
    for x in row[1:]:
        try:
            val = float(str(x).strip())
            ratings.append(val)
        except Exception:
            ratings.append(np.nan)
    ratings += ratings[:1]
    ax.plot(angles, ratings, 'o-', linewidth=2, label=f'{titles[i].capitalize()}', color=colors[i % len(colors)])
    ax.fill(angles, ratings, alpha=0.15, color=colors[i % len(colors)])
ax.set_thetagrids(np.degrees(angles[:-1]), professions)
ax.set_ylim(1, 10)
plt.title('Agent Ratings Across Questions', fontsize=14)
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()
plt.savefig('multi_chat_log_profession_combined.png')
plt.close()
