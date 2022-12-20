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

r <- terra::rast(r)
v <- sf::read_sf(v)

custom_mean <- function(values, coverage_fractions) {
  covf <- coverage_fractions[!is.na(values)]
  vals <- values[!is.na(values)]
  try(round(sum(vals * covf) / sum(covf)), silent = TRUE)
}

count_na <- function(values, coverage_fractions) {
  round((sum(as.numeric(!is.na(values)) * coverage_fractions) /
           sum(coverage_fractions)) * 1000)
}

result <- lapply(r, function(x){
  exactextractr::exact_extract(x = x,
                               y = v,
                               fun = custom_mean,
                               append_cols = "gauge_id",
                               progress = F)})

result2 <- lapply(r, function(x){
  exactextractr::exact_extract(x = x,
                               y = v,
                               fun = count_na,
                               append_cols = "gauge_id",
                               progress = F)})

for(i in seq_along(result)){
  if(i == 1){
    base <- result[[i]]
    names(base)[i+1] <- paste0('mean',i)
  }else{
    base <- merge(base,result[[i]],by='gauge_id')
    names(base)[i+1] <- paste0('mean',i)
  }
}

for(i in seq_along(result2)){
  if(i == 1){
    base2 <- result2[[i]]
    names(base2)[i+1] <- paste0('pc',i)
  }else{
    base2 <- merge(base2,result2[[i]],by='gauge_id')
    names(base2)[i+1] <- paste0('pc',i)
  }
}

result <- merge(base,base2,by='gauge_id')

terra::tmpFiles(remove = T)
write.table(x = result, file = out, sep =  ",", row.names = F)