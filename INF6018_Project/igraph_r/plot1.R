#For this example credit goes to
#https://stackoverflow.com/questions/24684931/improving-layout-and-resolution-of-a-network-graph-in-r


library(igraph)

set.seed(20)
wt2 = data.frame(X1=sample(1:100,200,replace=TRUE), X2=sample(1:100,200,replace=TRUE))
gg7 <- graph.edgelist(cbind(as.character(wt2$X1), as.character(wt2$X2)), 
                      directed=F)       

plot_file="/home/erin/INF6018_Project/plot1.pdf"
pdf(plot_file,10,10)
igraph.options(plot.layout=layout.circle, vertex.size=5)
plot(gg7)
dev.off()

plot_file="/home/erin/INF6018_Project/plot2.pdf"
pdf(plot_file,10,10)
igraph.options(plot.layout=layout.graphopt, vertex.size=7)
plot(gg7)
dev.off()