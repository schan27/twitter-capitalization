  # sink("capspos_output.txt", append=FALSE, split=FALSE) # write output to file
  
  significance <- function(p_val) {
    if (p_val < 0.001) {
      return('***')
    } else if (p_val < 0.01) {
      return('**')
    } else if (p_val < 0.05) {
      return('*')
    } else {
      return('') # not significant
    }
  }
  
  
  run_t_test <- function(d1, d2, col_name) {
    d1 <- d1[,c(col_name)]
    d2 <- d2[,c(col_name)]
    test_result <- t.test(d1, d2)
    # print(test_result)
    p_val <- test_result$p.value
    # print(p_val)
    conf_int <- test_result$conf.int
    result <- c(p_val, mean(d1), mean(d2))
    return(result)
  }
  
  
  format_num <- function(num) {
    return(format(round(num, 4), nsmall = 4))
  }
  
  
  get_row <- function(d1, d2, label1, label2, col_name) {
    result <- run_t_test(d1, d2, col_name)
    means <- paste(label1, '(', format_num(result[2]), ')', label2, '(', format_num(result[3]), ')')
    row <- list(means, result[1], significance(result[1]))
    return(row)
  }
  
  
  show_results <- function(filename, col_name) {
    df <- read.csv(filename)
    df <- na.omit(df)
    
    male <- df[which(df$gender == 'Male'),]
    female <- df[which(df$gender == 'Female'),]
    
    positive <- df[which(df$sentiment == 'positive'),]
    negative <- df[which(df$sentiment == 'negative'),]
    
    male_positive <- df[which(df$gender == 'Male' & df$sentiment == 'positive'),]
    male_negative <- df[which(df$gender == 'Male' & df$sentiment == 'negative'),]
    female_positive <- df[which(df$gender == 'Female' & df$sentiment == 'positive'),]
    female_negative <- df[which(df$gender == 'Female' & df$sentiment == 'negative'),]
    
    n <- 6
    tb <- data.frame(means=rep("", n), p_val=rep(NA, n), sig=rep("", n), stringsAsFactors=FALSE)
    # fill in the results
    tb[1,] <- get_row(male, female, 'M', 'F', col_name)
    tb[2,] <- get_row(positive, negative, '+', '-', col_name)
    tb[3,] <- get_row(male_positive, male_negative, 'M+', 'M-', col_name)
    tb[4,] <- get_row(female_positive, female_negative, 'F+', 'F-', col_name)
    tb[5,] <- get_row(male_positive, female_positive, 'M+', 'F+', col_name)
    tb[6,] <- get_row(male_negative, female_negative, 'M-', 'F-', col_name)
    
    print(tb)
    
  }
  
  process_categories <- function(filename, categoryfile) {
    conn <- file(categories, open='r')
    linn <- readLines(conn)
    for (i in 1:length(linn)) {
      line <- trimws(linn[i])
      cat(paste(line, '\n\n'))
      show_results(filename, line)
      cat('\n\n')
    }
  }
  
  # setwd('pos')
  process_colnames <- function(filename) {
    df <- read.csv(filename)
    columns <- tail(colnames(df), 10)
    for (i in 1:10) {
      col <- trimws(columns[i])
      cat(paste(col, '\n\n'))
      show_results(filename, col)
      cat('\n\n')
    }
  }
  
  # filename <- '1M_capspos_top10.csv'
  # process_colnames(filename)
  
  filename <- '1M_sentiment_gender_joined.csv'
  show_results(filename, 'count')
  show_results(filename, 'seq')
  show_results(filename, 'percent')
