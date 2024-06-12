# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from graspologic.embed import ClassicalMDS
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from scipy.stats import ks_2samp

SAVE_FIGS = True
out_path = Path("../talks/docs/slides/croissants/images/")

responses = pd.read_csv("lamination-evaluation/data/responses.csv")

responses["name"] = responses["name"].str.capitalize().str.strip()
responses["vote"] = responses["vote"].str.title()
responses["vote"] = responses["vote"].replace(
    {"Rosellini'S": "Rosellini's", "Coyle'S": "Coyle's"}
)

responses["name"].unique()


# %%

bakeries = np.sort(responses["vote"].unique())
bakeries_to_codes = {b: i for i, b in enumerate(bakeries)}
responses["vote_code"] = responses["vote"].map(bakeries_to_codes)

# %%
responses_wide = responses.pivot(index="name", columns="week", values="vote_code")

attendance = responses.groupby("name").size().sort_values(ascending=False)

responses_wide = responses_wide.loc[attendance.index].astype("Int64")

# %%


custom_cmap = sns.color_palette("tab20", n_colors=20)
# TODO add a color map

sns.set_context("talk")

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    responses_wide.astype(float), cmap=custom_cmap, cbar=False, ax=ax, yticklabels=True
)
ax.set(ylabel="Name", xlabel="Week", title="Votes by week")

if SAVE_FIGS:
    plt.savefig(out_path / "votemap.svg")

# %%

frequent_attendees = attendance[attendance > 5].index

# %%
responses_wide = responses_wide.loc[frequent_attendees]

# %%
tallies = responses.groupby(["week", "vote"]).size().rename("vote_count")

# %%
winners_by_week = (
    tallies.reset_index().set_index("vote").groupby("week").idxmax().reset_index()
)
winners_by_week.rename(columns={"vote_count": "winner"}, inplace=True)
winners_by_week["vote_code"] = winners_by_week["winner"].map(bakeries_to_codes)
# %%
was_correct = (responses_wide == winners_by_week.set_index("week")["vote_code"]).astype(
    float
)
was_correct[responses_wide.isna()] = np.nan
# %%
was_correct.mean(axis=1).sort_values(ascending=False)

# %%
# compute pairwise overlap scores between attendees


def compute_agreements(responses_wide):
    agreements = np.ones((len(responses_wide), len(responses_wide)))
    for i, name1 in enumerate(responses_wide.index):
        for j, name2 in enumerate(responses_wide.index):
            if i < j:
                responses1 = responses_wide.loc[name1].dropna()
                responses2 = responses_wide.loc[name2].dropna()
                # select weeks both were there
                index_intersection = responses1.index.intersection(responses2.index)
                responses1 = responses1.loc[index_intersection]
                responses2 = responses2.loc[index_intersection]
                agreement = (responses1 == responses2).mean()
                if pd.isna(agreement):
                    agreement = 0.0
                agreements[i, j] = agreement
                agreements[j, i] = agreement

    agreements = pd.DataFrame(
        agreements, index=responses_wide.index, columns=responses_wide.index
    )

    return agreements


agreements = compute_agreements(responses_wide)
disagreements = 1 - agreements
# %%
agreements_w_others = agreements.copy()
agreements_w_others -= np.eye(len(agreements_w_others))
besties = agreements_w_others.idxmax(axis=1)
for name, bestie in besties.items():
    agreement = agreements_w_others.loc[name, bestie]
    print(f"{name}'s bestie is {bestie} (agreement {agreement:.2f})")

# %%

method = "average"
links = linkage(squareform(disagreements), method=method)
cgrid = sns.clustermap(
    agreements,
    cmap="Reds",
    row_linkage=links,
    col_linkage=links,
    cbar_pos=(0.02, 0.85, 0.05, 0.13),
)
cgrid.ax_heatmap.set(xlabel="", ylabel="")
cgrid.ax_cbar.set(ylabel="Agreement")
plt.savefig(out_path / "agreements.svg")
cgrid.ax_heatmap.set(xticks=[], yticks=[])

if SAVE_FIGS:
    plt.savefig(out_path / "agreements_no_labels.svg")

# %%

classical_mds = ClassicalMDS(n_components=2, dissimilarity="precomputed")
embedding = classical_mds.fit_transform(disagreements.values)

fig, ax = plt.subplots(figsize=(8, 8))
sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1])
for i, name in enumerate(agreements.index):
    plt.text(embedding[i, 0], embedding[i, 1], name)
ax.set(xlabel="MDS 1", ylabel="MDS 2", xticks=[], yticks=[])
ax.spines[["top", "right"]].set_visible(False)

if SAVE_FIGS:
    plt.savefig(out_path / "mds.svg")

# %%


def randomize_votes(responses_wide):
    null_responses = pd.DataFrame(
        index=responses_wide.index, columns=responses_wide.columns, dtype="Int64"
    )

    for week in responses_wide.columns:
        week_responses = responses_wide[week].dropna()
        null_week_responses = pd.Series(
            index=week_responses.index, data=np.random.permutation(week_responses)
        )
        null_responses[week] = null_week_responses

    return null_responses


indices = np.triu_indices_from(agreements, k=1)

method = "average"

vals = []
for i in range(1000):
    null_responses = randomize_votes(responses_wide)
    null_agreements = compute_agreements(null_responses)
    null_agreements.index.name = ""
    null_agreements.columns.name = ""
    if i < 10:
        links = linkage(squareform(disagreements), method=method)
        sns.clustermap(
            null_agreements,
            cmap="Reds",
            row_linkage=links,
            col_linkage=links,
            xticklabels=False,
            yticklabels=False,
        )

        plt.savefig(out_path / "null_{i}.svg")

    vals.extend(null_agreements.values[indices])

# %%
fig, ax = plt.subplots(figsize=(8, 6))
sns.histplot(vals, stat="density", bins=np.arange(0, 1.0, 0.05), label="Null")
sns.histplot(
    agreements.values[indices],
    color="red",
    stat="density",
    bins=np.arange(0, 1.0, 0.05),
    label="Observed",
)
ax.legend()
ax.spines[["top", "right", "left"]].set_visible(False)
ax.set(xlabel="Agreement", ylabel="", yticks=[])

print(ks_2samp(agreements.values[indices], vals))

if SAVE_FIGS:
    plt.savefig(out_path / "agreement_histogram.svg")

