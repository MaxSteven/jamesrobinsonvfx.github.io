# Personal Blog

Based on [Poole](https://getpoole.com/) by [@mdo](https://markdotto.com/)

## Notes to Future Self
### Building

GitHub is [still using Jekyll3.9.0](https://www.sitepoint.com/jekyll-plugins-github), whereas my local verison is `4.2.0`.
We can build locally and push the contents of `_site` to the main branch on GitHub manually.


1. Switch to `<develop>` branch
2. Run `rake deploy` (Read the `Rakefile` to see exactly what it does)


> I suppose maybe in the future I could just switch the branch to something like
> `<deploy>` and point the **Pages** branch to that... that way `<main>` keeps
> the history more clear... doesn't really matter I guess?


[This Guy](https://www.sitepoint.com/jekyll-plugins-github/) helped quite a bit.

If switching back to GitHub's automatic building, don't forget to remove the
`.nojekyll` file, and move the contents of `<develop>` to `<main>` (or whichever
branch GitHub Pages is using to build the site from)

### Posting
1. Run `./create_post.py post` for a quick wizard. For new projects use
   `./create_post.py project`.