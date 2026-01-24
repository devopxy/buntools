#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  python3 \
  python3-venv \
  python3-pip \
  pdftk \
  tesseract-ocr \
  tesseract-ocr-eng \
  tesseract-ocr-fra \
  tesseract-ocr-deu \
  ghostscript \
  build-essential \
  libqpdf-dev

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ System dependencies installed and Python packages set up."
