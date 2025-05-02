import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('multi_chat_log_profession.csv')
professions = df.columns[1:]
colors = ['green', 'coral', 'orange', 'blue']
titles = df['Question'].tolist()

# --- Regenerate Fake Radar Chart ---
fake_idx = df['Question'].str.lower().tolist().index('fake')
row = df.iloc[fake_idx]
ratings = [float(str(x).strip()) for x in row[1:]]
ratings += ratings[:1]
angles = np.linspace(0, 2 * np.pi, len(professions), endpoint=False).tolist()
angles += angles[:1]
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
ax.plot(angles, ratings, 'o-', linewidth=2, color=colors[1])
ax.fill(angles, ratings, alpha=0.25, color=colors[1])
ax.set_thetagrids(np.degrees(angles[:-1]), professions)
ax.set_ylim(1, 10)
plt.title('Fake')
plt.tight_layout()
plt.savefig('multi_chat_log_profession_fake.png')
plt.close()

# --- Regenerate Combined Radar Chart ---
plt.figure(figsize=(10, 10))
ax = plt.subplot(111, polar=True)
angles = np.linspace(0, 2 * np.pi, len(professions), endpoint=False).tolist()
angles += angles[:1]
for i, row in df.iterrows():
    ratings = [float(str(x).strip()) for x in row[1:]]
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
