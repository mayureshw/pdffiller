# pdffiller

Fill pdfs by overlaying text on them using latex

# What does it do

This is year 2022... Wish all establishments had stopped issuing pesky PDF
forms, worse scans of their print versions. They should have switched to web
forms or at least fillable pdfs. I mean it makes no sense to convert a soft
form into print, fill it and convert into data again.

But the world is not perfect. Looks like we'll have to live with those pesky
non fillable PDF forms.

Worse are, those boxed forms with '1 letter per box', legacy of the computing
systems of the 1980s that continues to be lurking around just due to the
lethargy of the makers of such systems today.

If you would like to fill such forms as a soft copy and then print them, you
could possibly use a WYSWYG tool. I suggest flpsed, but there are other tools
as well.

But there are situations when a WYSWYG solution is not what you'll like. For
example:

- You have boxed forms (mentioned above)
- You have many copies of a form to fill with different data
- You just dislike WYSWYG. For example you'd like the text to be nicely aligned

In these situations you may like to try this tool out.

# System requirements

- Python3

- pdflatex

- latex package textpos

# Usage

Make sure fillpdf.py is in your path.

For every form you process, you need to create a 'metadata json file', which
gives names to various fields in the form.

If the same field is repeated in the form - for example, for whatever reason
they make you write your name at more than one places - use same name for it.
When you fill the data in the next step, you'll have to provide the value of
such fields only once.

For each copy of the form you fill, you need to provide values against the
fields identified in the metadata json in a 'data json file'.

Once you have these files ready just run

    filepdf.py <metadata json> <data json> > filled.tex
    pdflatex filled.tex

## How to get the locations of fields as x,y pairs

You can use tools like gimp or gv that show you the coordinates of a given
point in the pdf when you hold your cursor at a given field. Let's call it a
'grid tool' for further reference.

Different tools may use different scales to show the position. We just
normalize it, so the absolute number doesn't matter. Just note down the largest
x and y axis values in the respective tool.

Some tools (e.g. gimp) use top left corner as the point 0,0 (origin) while some
(e.g. gv) use the bottom left corner. We can specify this as we'll describe
below.

## Fields in Metadata json

### Fields that have internal defaults (see filepdf.py), which you may override if needed

    xoffset, yoffset:   Due to differences in the way your grid tool and latex
                        see the document layout a slight fixed adjustment may
                        be needed in the coordinates you capture. Defaults are
                        based on what worked for the sample example attached,
                        but you may override these values in youe metadata json
                        if you need.

    ypitchfactor:       If you find that a little scaling of vertical pitch is
                        needed you may override this value. (E.g. your fields
                        get placed properly at the top of the page, but start
                        swaying towards the bottom of the page.) It should
                        usually be very close to 1.

### Other mandatory fields common for all fields

    pdf:        Name of the pdf file this metadata is of

    origin:     TL if the point 0,0 is on top left, BL if it is at the bottom
                left

    xmax, ymax: Maximum values on x and y axis for normalization purpose

### Documentation fields (not mandatory, not used in the tool, for your own reference)

Suggested fields that may serve as a documentation of the metadata:

    source:     where did you get the PDF from, possibly a URL

    sourcedate: date of getting this pdf

    gridtool:   which tool was used to populate the x,y coordinates (e.g. gimp,
                gv)

You can of course add some arbitrary fields if you need for your own reference.

### Page and field details

    pgspec: Page spec with page number (1 onwards) being the key

    For each page a dictionary may contain the following fields

    at:     [x,y] pair as per your grid tool, depicting location of the field
            to be filled

    fld:    name of the field at this position

    pitch:  Do not specify for 'non boxed' forms. For boxed form this depicts
            the distance between adjacent boxes as per your grid tool.

## Fields in the data json

See sample file included 'data.json'. It's pretty straightforward. Just enter
the values against the fields as shown.

