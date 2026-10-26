# LJT-Homepage

Junteng Liu's personal academic homepage, forked from [AcademicPages](https://github.com/academicpages/academicpages.github.io).

## Content

Personal information is limited to the supplied memory. The existing About page contains the biography, research interests, education, internships, all six publications, honor, and contact information. The existing Publications page reuses the publication data recorded in About's front matter.

No additional content pages are created. Upstream sample pages, posts, publications, teaching, talks, portfolio items, example documents, and the talk map are excluded from the generated site. No skills proficiency, photograph, paper URL, repository URL, or exact publication date is inferred when absent from memory. Research interests are not relabeled as technical skills.

The repository owner is the hosting account; the personal GitHub contact remains `Vicent0205` as supplied in memory.

## Build

```sh
bundle install
npm install -g uglify-js
uglifyjs assets/js/plugins/jquery.greedy-navigation.js assets/js/_main.js assets/js/theme.js -c -m -o assets/js/main.min.js
JEKYLL_ENV=production bundle exec jekyll build
python3 scripts/check_homepage.py
```

The check requires exactly the About and Publications HTML pages, all six publications on each page, the supplied contact links, no template identity placeholders, and valid internal links under `/LJT-Homepage`.

## Deployment

The workflow in `.github/workflows/jekyll.yml` builds, checks, and deploys the site with GitHub Pages. It attempts to enable Pages automatically. If repository permissions prevent automatic enablement, set **Settings → Pages → Source → GitHub Actions** and rerun the workflow. Forked workflows may also need to be enabled in the Actions tab.

Configured site URL: `https://spanellisnikolaos564-max.github.io/LJT-Homepage/`.

The upstream MIT license is retained in `LICENSE`.
