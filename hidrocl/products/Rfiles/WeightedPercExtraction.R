#! /usr/bin/Rscript
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Aldo Tapia.
#
# ATTENTION!
# This script was made for extracting the weighted mean of pixels
# using a vector file with THE SAME CRS THAN THE RASTER FILE. The
# vector reprojection is skipped here in order to keep the memory
# usage as low as possible. Be aware than the field used for appending
# ID column to value column here is `gauge_id`

options(warn = -1)

f_args <- commandArgs(trailingOnly = TRUE)
v <- f_args[1] # polygon for extraction
r <- f_args[2] # raster for extraction
out <- f_args[3] # output file

custom_sum <- function(values, coverage_fractions) {
  totalPre <- sum(coverage_fractions)
  coverage_fractions <- coverage_fractions[values == 1]
  values <- values[values == 1]
  total <- 0
  if(length(values)>0){
    total <- sum(values*coverage_fractions,na.rm = T)
    total <- round(100*total/totalPre)
  }
  return(total)
}

count_na <- function(values, coverage_fractions) {
  round((sum(!is.na(values) * coverage_fractions) / sum(coverage_fractions)) * 1000)
}

result <- try({
  exactextractr::exact_extract(x = terra::rast(r),
  y = sf::read_sf(v),
  fun = custom_sum,
  append_cols = "gauge_id",
  progress = F)}, silent = TRUE)

result2 <- try({
  exactextractr::exact_extract(x = terra::rast(r),
  y = sf::read_sf(v),
  fun = count_na,
  append_cols = "gauge_id",
  progress = F)}, silent = TRUE)

result <- cbind(result, result2[, 2])

names(result) <- c("gauge_id", "sum", "pc")

terra::tmpFiles(remove = T)
write.table(x = result, file = out, sep =  ",", row.names = F)