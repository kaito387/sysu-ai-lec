#!/bin/bash
# 快速生成 PDF 的脚本
# 使用方法: ./md2pdf.sh report.md

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <markdown文件>"
    echo "示例: $0 lab1.md"
    exit 1
fi

INPUT="$1"
OUTPUT="${INPUT%.md}.pdf"

# 获取脚本所在目录（用于找到配置文件）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG="$SCRIPT_DIR/pandoc-template.yaml"

echo "正在生成 PDF: $INPUT -> $OUTPUT"

pandoc "$INPUT" -o "$OUTPUT" \
    --pdf-engine=xelatex \
    --metadata-file="$CONFIG"

if [ $? -eq 0 ]; then
    echo "✓ PDF 生成成功: $OUTPUT"
    ls -lh "$OUTPUT"
else
    echo "✗ PDF 生成失败"
    exit 1
fi
