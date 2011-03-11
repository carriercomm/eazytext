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

bdist_egg :
	python ./setup.py bdist_egg

upload : 
	python ./setup.py bdist_egg register upload --show-response 
	
sdist :
	python ./setup.py sdist

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

