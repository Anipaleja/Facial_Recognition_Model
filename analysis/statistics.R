# R script for statistical analysis of embedding distances

library(ggplot2)

embeddings <- read.csv("../analysis/distances.csv")

# Plot histogram of pairwise distances
ggplot(embeddings, aes(x=distance)) +
  geom_histogram(bins=30, fill="skyblue", color="black") +
  theme_minimal() +
  labs(title="Distribution of Embedding Distances",
       x="Cosine Distance", y="Frequency")