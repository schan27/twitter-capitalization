# http://www.cs.uni.edu/~jacobson/4772/week3/errorBarChart.html

library(ggplot2)
library(reshape)
library(Hmisc)
library(ggsignif)

filename <- "1M_sentiment_gender_joined.csv"
df <- read.csv(filename)
# df <- df[,c('count', 'sentiment', 'gender')]

# cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

ggplot(df, aes(gender, seq, fill=sentiment)) +
  stat_summary(fun.y=mean, geom='bar', position='dodge') +
  stat_summary(fun.data=mean_se, geom='errorbar', position=position_dodge(width=0.9), width=0.2) +
  coord_cartesian(ylim=c(0.1, 0.26)) +
  geom_signif(y_position=c(0.24, 0.25), xmin=c(0.8, 1.8), xmax=c(1.2, 2.2),
              annotation=c("NS", "***"), tip_length=0) 


ggplot(df, aes(gender, count, fill=sentiment)) +
  stat_summary(fun.y=mean, geom='bar', position='dodge') +
  stat_summary(fun.data=mean_se, geom='errorbar', position=position_dodge(width=0.9), width=0.2) +
  coord_cartesian(ylim=c(0.05, 0.3)) +
  geom_signif(y_position=c(0.26, 0.27), xmin=c(0.8, 1.8), xmax=c(1.2, 2.2),
              annotation=c("NS", "***"), tip_length=0) 


ggplot(df, aes(gender, percent, fill=sentiment)) +
  stat_summary(fun.y=mean, geom='bar', position='dodge') +
  stat_summary(fun.data=mean_se, geom='errorbar', position=position_dodge(width=0.9), width=0.2) +
  coord_cartesian(ylim=c(0.5, 3)) +
  geom_signif(y_position=c(2.8, 2.6), xmin=c(0.8, 1.8), xmax=c(1.2, 2.2),
              annotation=c("**", "**"), tip_length=0) 

  
# plot main effect
# ggplot(df, aes(gender, count)) +
  # stat_summary(fun.y=mean, geom='bar', position='dodge') + 
  # stat_summary(fun.data=mean_se, geom='errorbar', position=position_dodge(width=0.9), width=0.2)
