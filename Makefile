BASENAMES = call-of-cthulhu civil-disobedience

.PHONY: all
all: $(addsuffix .epub, $(BASENAMES)) $(addsuffix .html, $(BASENAMES)) 

# $@: $<

%.unfinishedepub: %.markdown
	pandoc \
		--standalone \
		--epub-chapter-level=2 \
		--epub-metadata=$(basename $<).dcmetadata.xml \
		--epub-embed-font=kingsley.otf \
		--epub-embed-font=alegreya-bolditalic.ttf \
		--epub-embed-font=alegreya-italic.ttf \
		--epub-stylesheet=literature.css \
		-t epub3 \
		-o $@ \
		$<

%.epub: %.unfinishedepub
	unzip -o -d $(basename $<).d $<
	python orthodoxize.py $(basename $<)
	cd $(basename $<).d && \
		zip -X0 $(basename $<).zip mimetype && \
		zip -rDX9 $(basename $<).zip * -x "*.DS_Store" -x mimetype
	mv $(basename $<).d/$(basename $<).zip $@


%.html: %.markdown
	pandoc \
		--standalone \
		--section-divs \
		--css=literature.css \
		--css=webpage.css \
		-t html5 \
		-o $@ \
		$<

.PHONY: clean
clean:
	-rm    $(addsuffix .unfinishedepub,$(BASENAMES))
	-rm -r $(addsuffix .d,$(BASENAMES))
	-rm    $(addsuffix .zip,$(BASENAMES))
	-rm    $(addsuffix .epub,$(BASENAMES))
	-rm    $(addsuffix .html,$(BASENAMES))
	
