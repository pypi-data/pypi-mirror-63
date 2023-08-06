# Gemfeed

Gemfeed is a simple tool for generating Atom feeds for directories of
text/gemini files.  It may not be adequate for large, complicated
Gemini sites, but if you have, for example, a gemlog which is just a
single directory full of .gmi files, each of which corresponds to one
post, then the idea is that you can call gemfeed from a regular
cronjob (or by hand after you write each post, if you like!) and
maintain an Atom feed for your gemlog with very little extra effort.

Basically, when run Gemfeed will find all world-readable `.gmi` or
`.gemini` files in the current directory and add the 10 most recently
created ones to an Atom feed it will save to the file `atom.xml`.

* Each file's creation time will be used as the corresponding entry's
  update time.
* The first heading line in each file (i.e. the first line encountered
  which begins with `#`, `##` or `###`) will be used as the
  corresponding entry's title.  If your file contains no heading line,
  the filename will be used as a title instead, with its extension
  removed.
* If an `index.gmi` or `index.gemini` file is found, it won't be
  included as an entry in the feed, but the first heading line in the
  index file will be used as the title for the feed.  If your index
  file contains no heading line, you'll get the dorky default "Just
  another Gemini feed".

The only information you *need* to provide to make this happen is a
base URL (with `-b` or `--base`).  If you provide a base URL of
`gemini://example.org/my-gemlog/` then Gemfeed will assume that a
file it finds named `my-first-post.gmi` is accessible via the URL
`gemini://example.org/my-gemlog/my-first-post.gmi`, and that the file
it produces will be accessible via the URL
`gemini://example.org/my-gemlog/atom.xml`.  Basically, you should
provide the URL which will your server will map to the directory
you're trying to generate a feed for.

If you want to, you can provide additional information above and
beyond the base URL:

* You can specify a directory other than the present working directory
  with `-d` or `--directory`.
* You can specify a number of posts other than 10 with `-n`
* You can change the output filename with `-o` or `--output`.
* You can specify your own feed title and subtitle with `-t` or
  `--title` and `-s` or `--subtitle`, respectively.  If you specify a
  title, it will override any heading line in your index file.
* You can specify an author name for the feed with `-a` or `--author`
  and/or an author email address for the feed with `-e` or `--email`.
* If you specify `-q` or `--quiet`, Gemfeed will write nothing to
  stdout unless there's a problem - ideal for cron jobs!
