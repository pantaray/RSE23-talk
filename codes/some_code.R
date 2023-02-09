sample_stats <- function(d_mu, d_sd) {
    samp <- rnorm(10^6, d_mu, d_sd)
    c(s_mu = mean(samp), s_sd = sd(samp))
}
