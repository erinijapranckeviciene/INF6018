library(igraph)

# Example with real migration net
nw_undirected<-read_graph("migration_total_undirected.pajek", format=c("pajek"))
plot_file="/home/erin/INF6018_Project/communitybyedgebetweenness.pdf"

# directed
nw_directed<-read_graph("migration_total_directed.pajek", format=c("pajek"))
plot_file2="/home/erin/INF6018_Project/communitybyedgebetweenness2.pdf"


eb <- cluster_edge_betweenness(nw_undirected)
print(eb)

pdf(plot_file,30,30)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(eb, nw_undirected)
dev.off()

# Draw communities on directed
pdf(plot_file2,30,30)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(eb, nw_directed)
dev.off()


# How to extract community information 
print(eb$membership)

