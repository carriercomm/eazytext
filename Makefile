develop :
	rm -rf zwiki-env
	virtualenv zwiki-env --no-site-packages
	bash -c "source zwiki-env/bin/activate ; python ./setup.py develop"

bdist_egg :
	python ./setup.py bdist_egg

sdist :
	python ./setup.py sdist

test :

clean :
	rm -rf build;
	rm -rf dist;
	rm -rf zwiki.egg-info;
	rm -rf zwiki_zeta.egg-info/;
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;

cleanall : clean
	rm -rf zwiki-env
