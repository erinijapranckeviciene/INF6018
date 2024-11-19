library(igraph)

# Example with real migration net
# directed
nw_directed<-read_graph("migration_total_directed.pajek", format=c("pajek"))
plot_file="/home/erin/INF6018_Project/communitybylabelprop.pdf"

lp <- cluster_label_prop(nw_directed, mode="out")
print(lp)

pdf(plot_file,30,30)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(lp, nw_directed)
dev.off()
