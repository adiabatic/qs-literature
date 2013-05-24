BASENAMES = call-of-cthulhu civil-disobedience
ASSETS = Makefile \
			jankyjson.py \
			fixup.py \
			workinfo.py \
			generate-dcmetadata.py \
			literature.css \
			kingsley.otf
ASSETS_EPUB = TEMPLATE.epub3.html
ASSETS_HTML = TEMPLATE.html webpage.css

.PHONY: all
all: $(addsuffix .epub, $(BASENAMES)) $(addsuffix .html, $(BASENAMES)) 

# $@: $<

%.unfinishedepub: %.markdown $(ASSETS) $(ASSETS_EPUB)
	python generate-dcmetadata.py $(basename $<)
	pandoc \
		--epub-chapter-level=2 \
		--epub-metadata=$(basename $<).dcmetadata.xml \
		--epub-embed-font=kingsley.otf \
		--epub-stylesheet=literature.css \
		--variable='title:$(shell python jankyjson.py $(basename $<).json "titles-qs[0]")' \
		--variable='author:$(shell python jankyjson.py $(basename $<).json "author-qs")' \
		-t epub3 \
		-o $@ \
		$<

%.epub: %.unfinishedepub
	unzip -o -d $(basename $<).d $<
	python fixup.py $(basename $<)
	cd $(basename $<).d && \
		zip -X0 $(basename $<).zip mimetype && \
		zip -rDX9 $(basename $<).zip * -x "*.DS_Store" -x mimetype
	mv $(basename $<).d/$(basename $<).zip $@


%.html: %.markdown $(ASSETS) $(ASSETS_HTML)
	pandoc \
		--template=TEMPLATE.html \
		--variable='title:$(shell python jankyjson.py $(basename $<).json "titles-qs[0]")' \
		--variable='pagetitle:$(shell python jankyjson.py $(basename $<).json "titles[0]")' \
		--variable='author:$(shell python jankyjson.py $(basename $<).json "author-qs")' \
		--section-divs \
		--css=literature.css \
		--css=webpage.css \
		-t html5 \
		-o $@ \
		$<

.PHONY: clean
clean:
	-rm    $(addsuffix .dcmetadata.xml,$(BASENAMES))
	-rm    $(addsuffix .unfinishedepub,$(BASENAMES))
	-rm -r $(addsuffix .d,$(BASENAMES))
	-rm    $(addsuffix .zip,$(BASENAMES))
	-rm    $(addsuffix .epub,$(BASENAMES))
	-rm    $(addsuffix .html,$(BASENAMES))
	
