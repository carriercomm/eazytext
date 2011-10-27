develop :
	rm -rf eazytext-env
	virtualenv eazytext-env --no-site-packages
	bash -c "source eazytext-env/bin/activate ; python ./setup.py develop"

test :
	cd eazytext/test; teststd.py;
	cd eazytext/test; testmixchar.py;
	cd eazytext/test; testmixline.py;
	cd eazytext/test; testcmd.py;

bdist_egg :
	cp CHANGELOG docs/CHANGELOG
	cp LICENSE docs/LICENSE
	cp README docs/README
	cp ROADMAP docs/ROADMAP
	python ./setup.py bdist_egg

sdist :
	cp CHANGELOG docs/CHANGELOG
	cp LICENSE docs/LICENSE
	cp README docs/README
	cp ROADMAP docs/ROADMAP
	python ./setup.py sdist

upload : 
	cp CHANGELOG docs/CHANGELOG
	cp LICENSE docs/LICENSE
	cp README docs/README
	cp ROADMAP docs/ROADMAP
	python ./setup.py sdist register -r http://www.python.org/pypi upload -r http://www.python.org/pypi --show-response 
	
vimplugin :
	rm -rf ./vim-plugin/vim-eazytext.tar.gz
	cd ./vim-plugin; tar cvfz ./vim-eazytext.tar.gz *

cleanall : clean
	rm -rf eazytext-env

clean :
	rm -rf distribute-0.6.10.tar.gz
	rm -rf build;
	rm -rf dist;
	rm -rf zwiki.egg-info;
	rm -rf zwiki_zeta.egg-info/;
	rm -rf eazytext.egg-info;
	rm -rf eazytext.egg-info/;
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;
	rm -rf eazytext/test/stdfiles/*.etx.py;
	rm -rf eazytext/test/stdfiles/*.html;
	rm -rf eazytext/test/mixchar.*;
	rm -rf eazytext/test/mixline.*;
