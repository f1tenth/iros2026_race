#!/usr/bin/env bash
# Serves the Jekyll site locally at http://localhost:4000
#
# Prerequisites (one-time setup if not already installed):
#   1. Install Ruby dev headers:
#        Debian/Ubuntu:  sudo apt install ruby-dev
#        Arch:           sudo pacman -S ruby
#   2. Install Jekyll to your user gem directory:
#        gem install jekyll bundler --user-install
#
# The gem bin directory is derived from the running Ruby, so this works
# regardless of which Ruby version is installed.

set -e

cd "$(dirname "$0")/.."

# Put the user gem bin dir on PATH (e.g. ~/.local/share/gem/ruby/3.4.0/bin).
GEM_BIN="$(ruby -e 'print Gem.user_dir')/bin"
export PATH="$GEM_BIN:$PATH"

if ! command -v jekyll >/dev/null 2>&1; then
	echo "jekyll not found on PATH (looked in $GEM_BIN)." >&2
	echo "Install it with:  gem install jekyll bundler --user-install" >&2
	exit 1
fi

# rules.md and competition_rules.md include the roboracer_rules submodule and
# the build hard-fails without it.
if [ ! -f _includes/roboracer_rules/rules_v3.md ]; then
	echo "Initialising the roboracer_rules submodule..."
	git submodule update --init --recursive
fi

# LiveReload defaults to port 35729. If anything else already holds it, the
# reactor thread dies on bind and takes the whole server down with it, so pick
# the first free port instead. Ruby does the probing because it is already a
# prerequisite and TCPServer.new fails exactly where the reactor would.
LIVERELOAD=(--livereload)
case " $* " in
*" --livereload-port"*)
	: # the caller pinned a port; respect it
	;;
*)
	for port in {35729..35759}; do
		if ruby -rsocket -e 'TCPServer.new("127.0.0.1", ARGV[0].to_i).close' "$port" 2>/dev/null; then
			LIVERELOAD+=(--livereload-port "$port")
			if [ "$port" -ne 35729 ]; then
				echo "LiveReload port 35729 is in use; falling back to $port."
			fi
			break
		fi
	done
	if [ "${#LIVERELOAD[@]}" -eq 1 ]; then
		echo "No free LiveReload port in 35729-35759; serving without live reload." >&2
		LIVERELOAD=()
	fi
	;;
esac

# Use Bundler only when the project actually pins its gems; this repo gitignores
# Gemfile/Gemfile.lock, so the plain jekyll binary is the normal path.
if [ -f Gemfile ]; then
	bundle config set --local path vendor/bundle
	bundle install
	exec bundle exec jekyll serve "${LIVERELOAD[@]}" "$@"
fi

exec jekyll serve "${LIVERELOAD[@]}" "$@"
