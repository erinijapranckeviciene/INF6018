library(igraph)

nw_undirected<-read_graph("migration_total_undirected.pajek", format=c("pajek"))
nw_directed<-read_graph("migration_total_directed.pajek", format=c("pajek"))

plot_file="/home/erin/INF6018_Project/plotundirected.pdf"
pdf(plot_file,30,30)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(nw_undirected)
dev.off()

plot_file="/home/erin/INF6018_Project/plotdirected.pdf"
pdf(plot_file,30,30)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(nw_directed)
dev.off()
