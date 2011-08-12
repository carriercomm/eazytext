develop :
	rm -rf eazytext-env
	virtualenv eazytext-env --no-site-packages
	bash -c "source eazytext-env/bin/activate ; python ./setup.py develop"

test :
	cd eazytext/test; teststd.py;
	cd eazytext/test; testmixchar.py;
	cd eazytext/test; testmixline.py;

bdist_egg :
	python ./setup.py bdist_egg

sdist :
	python ./setup.py sdist

upload : 
	python ./setup.py sdist register upload --show-response 
	
vimplugin :
	rm -rf ./vim-plugin/vim-eazytext.tar.gz
	cd ./vim-plugin; tar cvfz ./vim-eazytext.tar.gz *

cleanall : clean
	rm -rf eazytext-env

clean :
	rm distribute-0.6.10.tar.gz
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
