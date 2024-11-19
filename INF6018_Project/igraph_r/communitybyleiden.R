library(igraph)

# Example with made network
g <- make_graph("Zachary")
# By default CPM is used
r <- quantile(strength(g))[2] / (gorder(g) - 1)
# Set seed for sake of reproducibility
set.seed(1)
ldc <- cluster_leiden(g, resolution = r)
print(ldc)
plot(ldc, g)

# Example with real migration net
nw_undirected<-read_graph("migration_total_undirected.pajek", format=c("pajek"))
plot_file="/home/erin/INF6018_Project/communitybyleiden.pdf"

# Quantiles 25% 2,  50% 3, 75% 4
r <- quantile(strength(nw_undirected))[2] / (gorder(nw_undirected) - 1)

# What is resolution
print("resolution")
print(r)

# Set seed for sake of reproducibility
set.seed(1)
ldc <- cluster_leiden(nw_undirected, resolution = r)
print(ldc)

pdf(plot_file,30,30)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(ldc, nw_undirected)
dev.off()

# How to extract community information 
print(ldc$membership)

