# Photos folder

Organized by primary category — this is just for YOUR convenience while
sorting files, the website code does not care which folder a file sits in.

  photos/
    architecture/
    fashion/
    wedding/

## One photo, several tags
Put the file in whichever folder makes sense to you (e.g. its main category),
then reference it in index.html and list ALL its tags separated by spaces:

  <div class="proj__frame" style="background-image:url('photos/fashion/look-04.jpg')"></div>
  ...
  <article class="proj" data-type="commercial" data-category="fashion wedding">

That photo will now appear under both the Fashion and the Weddings filters.
Same idea works for data-type="personal commercial" if a photo genuinely
belongs to both.

## New category later
1. Add a folder here (e.g. photos/portrait/).
2. Add a filter button in index.html's Category row.
3. Use data-category="portrait" (alone or combined with others) on your photos.

Keep files compressed for web (roughly 500KB–1MB each, JPEG) so the site stays fast.
