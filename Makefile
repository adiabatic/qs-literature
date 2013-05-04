NAME=call-of-cthulhu

all: epub directory webpage fixes book
	
epub:
	pandoc \
		--standalone \
		--epub-chapter-level=2 \
		--epub-metadata=dublin-core-metadata.xml \
		--epub-embed-font=kingsley.otf \
		--epub-embed-font=alegreya-bolditalic.ttf \
		--epub-embed-font=alegreya-italic.ttf \
		--epub-stylesheet=literature.css \
		-t epub3 \
		-o ${NAME}.epub \
		${NAME}.markdown

directory:
	cp ${NAME}.epub ${NAME}.zip
	unzip -o -d ${NAME}.d ${NAME}.zip
	rm ${NAME}.zip
	
fixes:
	python orthodoxize.py

book:
	cd $(NAME).d && zip -X0 "$(NAME)" mimetype && zip -rDX9 "$(NAME)" * -x "*.DS_Store" -x mimetype
	mv $(NAME).d/$(NAME).zip $(NAME).epub

webpage:
	pandoc \
		--standalone \
		--section-divs \
		--css=literature.css \
		--css=webpage.css \
		-t html5 \
		-o ${NAME}.html \
		${NAME}.markdown
		

clean:
	-rm    ${NAME}.epub
	-rm -r ${NAME}.d
	-rm    ${NAME}.zip
	-rm    ${NAME}.html
	
