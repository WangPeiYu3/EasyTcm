#!/usr/bin/env Rscript

# 基因富集分析完整脚本（处理一对多映射版）
# 输入: Symbol.txt (每行一个基因Symbol)
# 输出: GO和KEGG富集结果及可视化

# 1. 安装必要包 ------------------------------------------------------------
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

required_packages <- c("clusterProfiler", "org.Hs.eg.db", "DOSE",
                       "enrichplot", "ggplot2", "pathview", "dplyr")
for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE)) {
    BiocManager::install(pkg)
    library(pkg, character.only = TRUE)
  }
}

# 2. 读取输入文件 ---------------------------------------------------------
read_genes <- function(file) {
  if (!file.exists(file)) {
    stop("输入文件不存在，请确保Symbol.txt在当前目录")
  }
  
  tryCatch({
    genes <- scan(file, what = "character", quiet = TRUE)
    genes <- trimws(genes)
    genes <- genes[genes != ""]  # 移除空行和空白字符
    if (length(genes) == 0) stop("输入文件没有有效的基因符号")
    return(unique(genes))  # 去除重复基因
  }, error = function(e) {
    stop(paste("读取基因文件失败:", e$message))
  })
}

gene_symbols <- read_genes("Symbol.txt")
cat("输入基因数量:", length(gene_symbols), "\n")

# 3. 基因ID转换（处理一对多映射）------------------------------------------
gene_mapping <- tryCatch({
  suppressMessages(
    bitr(gene_symbols,
         fromType = "SYMBOL",
         toType = c("ENTREZID", "ENSEMBL"),
         OrgDb = org.Hs.eg.db)
  )
}, error = function(e) {
  stop(paste("基因ID转换失败:", e$message))
})

# 检查并处理一对多映射
multi_mapped <- gene_mapping %>%
  group_by(SYMBOL) %>%
  filter(n() > 1) %>%
  arrange(SYMBOL)

if (nrow(multi_mapped) > 0) {
  cat("\n发现", nrow(multi_mapped), "个一对多映射关系，涉及",
      n_distinct(multi_mapped$SYMBOL), "个基因Symbol:\n")
  print(as.data.frame(multi_mapped))
  
  # 保存完整映射关系
  write.csv(gene_mapping, "results/gene_mapping_full.csv", row.names = FALSE)
  
  # 策略1：保留所有映射（推荐用于全面分析）
  #   gene_list <- gene_mapping$ENTREZID
  
  # 策略2：或者选择保留第一个映射（取消下面注释）
  gene_mapping <- gene_mapping[!duplicated(gene_mapping$SYMBOL), ]
  gene_list <- gene_mapping$ENTREZID
  # 再保存策略后的映射关系
  write.csv(gene_mapping, "results/gene_mapping_strategy1.csv", row.names = FALSE)
  cat("\n采用策略：保留所有ENTREZID映射（共", length(gene_list), "个）\n")
} else {
  gene_list <- gene_mapping$ENTREZID
  cat("所有基因均为一对一映射\n")
}

# 检查未映射基因
unmapped <- setdiff(gene_symbols, gene_mapping$SYMBOL)
if (length(unmapped) > 0) {
  cat("\n警告：", length(unmapped), "个基因未能成功映射:\n")
  write.table(unmapped, "results/unmapped_genes.txt", row.names = FALSE, quote = FALSE)
  print(head(unmapped, 10))
  if (length(unmapped) > 10) cat("... (更多见results/unmapped_genes.txt)\n")
}

cat("\n最终使用", length(gene_list), "个ENTREZID进行富集分析\n")
if (length(gene_list) < 5) {
  warning("基因数量较少，可能影响富集分析结果")
}

# 4. GO富集分析 ----------------------------------------------------------
perform_go <- function(ont) {
  cat("\n正在进行GO", ont, "富集分析...\n")
  suppressMessages(
    enrichGO(gene          = gene_list,
             OrgDb         = org.Hs.eg.db,
             ont           = ont,
             pAdjustMethod = "BH",
             pvalueCutoff  = 0.05,
             qvalueCutoff  = 0.2,
             readable      = TRUE)
  )
}

go_results <- list(
  BP = perform_go("BP"),  # 生物过程
  MF = perform_go("MF"),  # 分子功能
  CC = perform_go("CC")   # 细胞组分
)

# 5. KEGG富集分析 --------------------------------------------------------
cat("\n正在进行KEGG富集分析...\n")
kegg_result <- tryCatch({
  suppressMessages(
    enrichKEGG(gene         = gene_list,
               organism     = 'hsa',
               pvalueCutoff = 0.05,
               qvalueCutoff = 0.2)
  )
}, error = function(e) {
  message("KEGG分析失败: ", e$message)
  return(NULL)
})

# 如果KEGG结果不为空，转换为可读格式
if (!is.null(kegg_result) && nrow(kegg_result) > 0) {
  kegg_result <- setReadable(kegg_result, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")
}

# 6. 结果保存和可视化 ---------------------------------------------------
results_dir <- "results"
if (!dir.exists(results_dir)) {
  dir.create(results_dir, recursive = TRUE)
}

# GO结果输出
for (ont in c("BP", "MF", "CC")) {
  res <- go_results[[ont]]
  if (!is.null(res) && nrow(res) > 0) {
    write.csv(as.data.frame(res),
              file = file.path(results_dir, paste0("GO_", ont, ".csv")),
              row.names = FALSE)
    
    tryCatch({
      pdf(file.path(results_dir, paste0("GO_", ont, "_dotplot.pdf")),
          width = 10, height = 14)
      print(dotplot(res, showCategory = 15, title = paste("GO", ont)))
      dev.off()
    }, error = function(e) {
      message("绘制GO ", ont, " 点图失败: ", e$message)
    })
  } else {
    cat("GO", ont, "没有显著富集结果\n")
  }
}



# KEGG结果输出
if (!is.null(kegg_result) && nrow(kegg_result) > 0) {
  write.csv(as.data.frame(kegg_result),
            file = file.path(results_dir, "KEGG.csv"),
            row.names = FALSE)
  
  tryCatch({
    pdf(file.path(results_dir, "KEGG_dotplot.pdf"), width = 10, height = 10)
    print(dotplot(kegg_result, showCategory = 15, title = "KEGG Pathways"))
    dev.off()
  }, error = function(e) {
    message("绘制KEGG点图失败: ", e$message)
  })
  
  # 绘制top3通路图
  top_kegg <- head(kegg_result$ID, 10)
  for (pid in top_kegg) {
    tryCatch({
      pathview(gene.data  = gene_list,
               pathway.id = pid,
               species    = "hsa",
               out.suffix = "pathview",
               kegg.dir   = results_dir)
    }, error = function(e) {
      message("绘制KEGG通路图 ", pid, " 失败: ", e$message)
    })
  }
} else {
  cat("没有显著的KEGG通路富集结果\n")
}

cat("\n分析完成！结果已保存到", results_dir, "文件夹\n")