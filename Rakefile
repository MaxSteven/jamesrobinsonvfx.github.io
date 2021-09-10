# Thanks David Lyons @ https://www.sitepoint.com/jekyll-plugins-github/ for the tips
GH_PAGES_DIR = "/tmp/compiled_site"

desc "Build Jekyll site and copy files"
task :deploy do
  # Work on <develop> branch
  system "git checkout develop"

  # Scrape Gist Feed
  system "./fetch_gist_snippets.py _data/gist_snippets.json"

  # Build Site
  system "jekyll build"

  # Copy to temp location
  puts "Creating temp site build directory"
  system "mkdir #{GH_PAGES_DIR}"
  system "rm -r #{GH_PAGES_DIR}/*" unless Dir['#{GH_PAGES_DIR}/*'].empty?
  puts "Copying site to temp"
  system "cp -r _site/* #{GH_PAGES_DIR}/"

  # Move to <main> for deployment
  puts "Stashing changes"
  system "git stash"

  puts "Switching to <main>"
  system "git checkout main"
  system "git pull origin main"

  puts "Removing directories"
  system "rm -rf *"
  system "rm -rf .jekyll-cache"

  puts "Copying temp site build"
  system "cp -r #{GH_PAGES_DIR}/* ."
  system "touch .nojekyll"
  system "git add . && git commit -m 'Push local build update (see develop branch)'"
  system "git push origin main"
  puts "Switching back to <develop>"
  system "git checkout develop"

  puts "Reapplying stash"
  system "git stash apply"
end
