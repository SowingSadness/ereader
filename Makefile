test-urls:
	for url in $(shell find ./tests -name '*.html'); do \
	    FILE_URL="file://"$(shell pwd)$$url; \
	    echo $$FILE_URL | sed -e 's#\.##'; \
	done > urls-abs.txt
	
	echo "TEST urls-abs.txt\n"
	for url in $(shell cat urls-abs.txt); do \
	    python runner.py -v 2 --short $$url; \
	    echo $(shell head -c 80 < /dev/zero | tr '\0' '\-'); \
	done

	echo "TEST urls.txt\n"
	for url in $(shell cat urls.txt); do \
	    python runner.py -v 2 --short $$url; \
	    echo $(shell head -c 80 < /dev/zero | tr '\0' '\-'); \
	done
