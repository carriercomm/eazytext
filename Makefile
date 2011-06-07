develop :
	rm -rf eazytext-env
	virtualenv eazytext-env --no-site-packages
	bash -c "source eazytext-env/bin/activate ; python ./setup.py develop"

testall :
	cd eazytext/test/; nosetests -x -s testlex;
	cd eazytext/test/; nosetests -x -s testparse;
	cd eazytext/test/; nosetests -x -s testmacros;
	cd eazytext/test/; nosetests -x -s testextn;
	cd eazytext/test/; nosetests -x -s testwiki;
	cd eazytext/test/; nosetests -x -s testdocs;

bdist_egg :
	python ./setup.py bdist_egg

sdist :
	python ./setup.py sdist

upload : 
	python ./setup.py bdist_egg register upload --show-response 
	
vimplugin :
	rm -rf ./vim-plugin/vim-eazytext.tar.gz
	cd ./vim-plugin; tar cvfz ./vim-eazytext.tar.gz *

cleanall : clean
	rm -rf eazytext-env

clean :
	rm -rf build;
	rm -rf dist;
	rm -rf zwiki.egg-info;
	rm -rf zwiki_zeta.egg-info/;
	rm -rf eazytext.egg-info;
	rm -rf eazytext.egg-info/;
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;

