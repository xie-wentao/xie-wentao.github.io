#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Prefer a supported Ruby; macOS's system Ruby is too old for this template.
for ruby_bin in \
  /opt/homebrew/opt/ruby/bin/ruby \
  /usr/local/opt/ruby/bin/ruby \
  /usr/local/Homebrew/Library/Homebrew/vendor/portable-ruby/current/bin/ruby \
  /opt/homebrew/Library/Homebrew/vendor/portable-ruby/current/bin/ruby \
  "$(command -v ruby || true)"; do
  if [ -x "$ruby_bin" ] && "$ruby_bin" -e 'exit(Gem::Version.new(RUBY_VERSION) >= Gem::Version.new("3.2") ? 0 : 1)' 2>/dev/null; then
    export PATH="$(dirname "$ruby_bin"):$PATH"
    break
  fi
done
ruby -e 'abort "Ruby 3.2+ is required. Install it before running this script." if Gem::Version.new(RUBY_VERSION) < Gem::Version.new("3.2")'
export BUNDLE_PATH=vendor/bundle
export BUNDLE_APP_CONFIG=.bundle

case "${1:-serve}" in
  setup) bundle install ;;
  build) JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter ;;
  serve) bundle exec jekyll serve --host 127.0.0.1 --port "${PORT:-4000}" ;;
  *) echo "Usage: ./scripts/site.sh [setup|build|serve]"; exit 1 ;;
esac
