VIRTUAL_ENV=/home/ec2-user/env
BUNDLE=~/lambda/bundle.zip


help:
	@echo
	@echo "Possible commands"
	@echo
	@echo "  clean           Cleans up the bundle.zip file"
	@echo "  bundle.zip      Generates the bundle.zip file"
	@echo "  update          Updates the aws lambda function"
	@echo


clean:
	if [ -a $(BUNDLE) ]; then rm $(BUNDLE); fi


bundle.zip: handler.py worker.py
	cd ~/lambda
	zip -9 bundle.zip handler.py
	zip -r9 bundle.zip worker.py
	zip --symlinks -r9 bundle.zip local/lib/*.so*
	cd $(VIRTUAL_ENV)/lib/python2.7/site-packages; zip -r9 ~/lambda/bundle.zip *
	cd $(VIRTUAL_ENV)/lib64/python2.7/site-packages; zip -r9 ~/lambda/bundle.zip *

update: bundle.zip
	aws lambda update-function-code --function-name handler --zip-file fileb:///home/ec2-user/lambda/bundle.zip
