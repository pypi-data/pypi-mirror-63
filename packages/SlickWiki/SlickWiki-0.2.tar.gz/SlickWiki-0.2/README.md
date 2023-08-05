SlickWiki
======================================================================

SlickWiki is a personal wiki tool that allows you to write your
thoughts in Markdown in your favorite editor, organizing them as you
like.

Quick start
----------------------------------------------------------------------

### Installation

To install SlickWiki, do from a terminal as root: `pip3 install
slickwiki`.

### Creating a wiki

To initialize a new wiki, create a directory (say, /home/guest/wiki).
Then do `slick --init /home/guest/wiki`.

### Starting the wiki
To serve the wiki on the default port (8080), do `slick
/home/guest/wiki`.  Point a browser to `localhost:8080`, and you will
see your wiki.

### Editing pages

To edit a page, follow a link to a page that does not exist or click
'Edit this page' at the bottom of an existent page.  SlickWiki will
open the Markdown source of the page in a text editor.  By default,
this is the default terminal text editor (usually `vi` or `nano`) in
the default terminal emulator.

#### Configuring the editor

Since that's almost never what the user would prefer, you should
probably edit `cfg.json` in your wiki directory (in the example above,
that's /home/guest/wiki/cfg.json).  Change the value for the key
`"editorCommand"` to one of the following values:

 - **Emacs**: `"emacs \"{{path}}\""`
 - **vi**: `"x-terminal-emulator -e vi \"{{path}}\""`
 - **Emacs (using emacsclient)**: `"emacsclient -a emacs \"{{path\""`
 
In general, the command for any editor command is `"_editor_
\"{{path}}\""`, where _editor_ is the command to launch the editor
(e.g. `gedit`, `gvim`, `leafpad`).  The pattern "{{path}}" is replaced
by the path to the file to be edited.

### Altering the wiki's appearance

Each page of your wiki is wrapped in an HTML template.  To change what
the template contains, edit `wrapper.html` in the wiki directory.  Be
sure to leave the `{{{content}}}` tag in the body; it is replaced by
the content of the page.  It is also wise to keep the `Edit page` link
in there somewhere.

Each page is also styled by CSS contained in the file `css` in the
wiki directory; the default is basic but not unattractive, and you can
alter it as you please.

### Inserting images in wiki pages

Images (and other non-markdown files) can be put in the `static`
subdirectory of the wiki directory.  For example, if you put an image
named `happy.jpg` in the `static` directory, you can reference it in a
wiki page as:

    ![Happy face](/static/happy.jpg "A happy face")
	
There really is no natural way to reference an image in plain text;
you may wish to use plain HTML instead:

    <img alt="A happy face" src="/static/happy.jpg" />

License
----------------------------------------------------------------------

SlickWiki is released under the terms of the MIT license, which is
included.
