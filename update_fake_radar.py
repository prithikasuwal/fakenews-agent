import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('multi_chat_log_profession.csv')
professions = df.columns[1:]
colors = ['lightcoral']  # 'Fake' question color

# Find the index for the 'Fake' question (case-insensitive)
fake_idx = df['Question'].str.lower().tolist().index('fake')
row = df.iloc[fake_idx]
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
ax.plot(angles, ratings, 'o-', linewidth=2, color=colors[0])
ax.fill(angles, ratings, alpha=0.25, color=colors[0])
ax.set_thetagrids(np.degrees(angles[:-1]), professions)
ax.set_ylim(1, 10)
plt.title('Fake')
plt.tight_layout()
plt.savefig('multi_chat_log_profession_fake.png')
plt.close()
