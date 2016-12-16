# This R script calculates Fleiss Kappa for the inter-annotator agreement
# the data file is ratings.txt, it consists of one column per rater, separated by \table
# and containing only the ratings.

install.packages(c("irr"))

library(irr)
help("kappam.fleiss")

ratings_file = "ratings.txt"
ratings = read.table(ratings_file)
#ratings

kappam.fleiss(ratings)