library(tidyverse)

games <- read.csv("games.csv")


## Plot rating (points) ----------------------------------
'
outcome_colors <- c("white" = "white", "black" = "black", "draw" = "blue")

# Plot
p1 <- ggplot(games, aes(white_rating, black_rating, color = winner)) +
  geom_point(alpha = 0.2, size = 1) +
  scale_color_manual(values = outcome_colors) +
  geom_abline() +
  # geom_vline(xintercept = line_pos, linetype = "dashed", color = "blue") +
  # geom_hline(yintercept = line_pos, linetype = "dashed", color = "blue") +
  coord_fixed(1) +
  theme_minimal() +
  theme(
    plot.background = element_rect(fill = "grey40")
  )
'


## Plot rating counts (bars) -----------------------------
'
# Combine w/b
combine_game <- games %>%
  pivot_longer(cols = c(white_rating, black_rating), values_to = "rating") %>%
  select(rating)

# Bin
combine_game <- combine_game %>%
  mutate(rating_bin = cut(rating, 
                          breaks = seq(780, 2725, by = 100),
                          include.lowest = TRUE, 
                          right = FALSE))

# Count ratings
game_counts <- combine_game %>%
  count(rating_bin)

# Plot
p2 <- ggplot(game_counts, aes(x = rating_bin, y = n)) +
  geom_col(fill = "steelblue") +
  labs(x = "Rating", y = "Count",
  title = "Distribution of Ratings (Combined Players)") +
  theme_minimal()
'


# Plot rating diffs --------------------------------------
' # nolint
game_diffs <- games %>%
    mutate(diff = abs(white_rating - black_rating))

p <- ggplot(game_diffs, aes(diff)) +
    geom_histogram() +
    theme_minimal()
'


# Plot piece captures ------------------------------------
'
checks <- read.csv("UseableCSV/checks.csv")

p <- ggplot(checks, aes(piece, count)) +
    geom_col() +
    theme_minimal()
'

# Plot rating diffs --------------------------------------
rates <- read.csv("UseableCSV/rating_wins.csv") %>%
          filter(winner == "white")

p <- ggplot(rates, aes(rate_diff, count)) +
        geom_line() +
        theme_bw()

plot(p)